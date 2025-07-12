def calculate_lot_size(balance, risk_percent, stop_loss_pips, pip_value=10):
    """
    Calculate lot size based on balance, risk %, and SL in pips.
    pip_value: $10 per pip for 1.00 lot on most USD pairs
    """
    risk_dollars = (risk_percent / 100) * balance
    lot_size = risk_dollars / (stop_loss_pips * pip_value)
    return round(lot_size, 2)
