from flask import Blueprint, redirect, url_for, flash

agent_bp = Blueprint('agent_bp', __name__)

@agent_bp.route('/agent/place_trade', methods=['POST'])
def place_trade():
    # Placeholder: In real usage, connect to MT5 Python API here.
    flash("Trade has been successfully executed!")
    return redirect(url_for('ask_bp.ask'))
