import os
import argparse
import pyperclip
import requests

from structure_parser import get_market_context
from risk_calculator import calculate_lot_size

DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
USE_MOCK = os.getenv("USE_MOCK_RESPONSE", "false").lower() == "true"


def generate_trade_plan(market_context, balance=None, risk_percent=None):
    if USE_MOCK:
        response_text = """📊 Generated Trade Plan:

- Pair: EURUSD
- Direction: Buy
- Entry: 1.0850
- Stop Loss: 1.0820
- Take Profit: 1.0910
- RR: 1:2
- Lot Size: 0.02
- Reason: BOS confirmed on 1H, price returning to bullish order block, liquidity above equal highs."""
    else:
        url = "https://api.deepseek.com/chat/completions"
        headers = {
            "Authorization": f"Bearer {DEEPSEEK_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek-chat",
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are a professional forex trading assistant. Based on market context, generate a trade plan "
                        "with this format:\n\n"
                        "- Pair: \n- Direction: \n- Entry: \n- Stop Loss: \n- Take Profit: \n"
                        "- RR: \n- Lot Size: \n- Reason: "
                    )
                },
                {"role": "user", "content": market_context}
            ]
        }
        try:
            res = requests.post(url, headers=headers, json=payload, timeout=15)
            res.raise_for_status()
            response_text = res.json()["choices"][0]["message"]["content"]
        except Exception as e:
            return f"❌ Error calling DeepSeek API: {e}"

    if balance and risk_percent:
        try:
            # extract entry & SL prices
            entry_line = next(line for line in response_text.splitlines() if "Entry" in line)
            sl_line = next(line for line in response_text.splitlines() if "Stop Loss" in line)

            entry = float(entry_line.split(":")[1].strip())
            stop_loss = float(sl_line.split(":")[1].strip())
            stop_loss_pips = abs(entry - stop_loss) * 10000  # EURUSD pip conversion

            lot_size = calculate_lot_size(balance, risk_percent, stop_loss_pips)
            response_text = update_lot_size(response_text, lot_size)
        except Exception as e:
            print(f"⚠️ Error calculating lot size: {e}")

    return response_text


def update_lot_size(plan, lot_size):
    lines = plan.splitlines()
    updated = []
    for line in lines:
        if line.strip().startswith("Lot Size:"):
            updated.append(f"- Lot Size: {lot_size:.2f}")
        else:
            updated.append(line)
    return "\n".join(updated)


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("--balance", type=float, help="Account balance (e.g. 2000)")
    parser.add_argument("--risk", type=float, help="Risk percent per trade (e.g. 1 for 1%)")
    return parser.parse_args()


if __name__ == "__main__":
    args = parse_args()
    balance = args.balance
    risk_percent = args.risk

    market_context = get_market_context()
    print("\n📈 Market Context:\n")
    print(market_context)

    plan = generate_trade_plan(market_context, balance, risk_percent)
    print("\n📊 Generated Trade Plan:\n")
    print(plan)

    # Save to file and copy to clipboard
    try:
        with open("trade_plan.txt", "w", encoding="utf-8") as f:
            f.write(plan)
        pyperclip.copy(plan)
        print("\n✅ Trade plan saved to trade_plan.txt")
        print("📋 Trade plan copied to clipboard!")
    except Exception as e:
        print(f"❌ Error saving or copying plan: {e}")
