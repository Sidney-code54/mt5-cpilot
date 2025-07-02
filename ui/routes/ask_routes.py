from flask import Blueprint, render_template, request, redirect, url_for, flash
from ask_mode.gpt_planner import generate_trade_plan
from ask_mode.structure_parser import get_market_context

ask_bp = Blueprint('ask', __name__)

@ask_bp.route("/", methods=["GET", "POST"])
def index():
    trade_plan = None
    if request.method == "POST":
        balance = request.form.get("balance")
        risk = request.form.get("risk")

        try:
            balance = float(balance) if balance else None
            risk = float(risk) if risk else None

            market_context = get_market_context()
            trade_plan = generate_trade_plan(market_context, balance, risk)
        except Exception as e:
            flash(f"❌ Error: {e}", "error")

    return render_template("index.html", trade_plan=trade_plan)
