@auth_bp.route('/ask-mode', methods=['GET', 'POST'])
@login_required
def ask_mode():
    from ask_mode_agent import generate_trade_plan
    from auth.models import Strategy
    from flask_login import current_user

    plan = None
    if request.method == 'POST':
        symbol = request.form.get('symbol', 'EURUSD')
        balance = float(request.form.get('balance', 1000))
        risk = float(request.form.get('risk', 1))
        plan = generate_trade_plan(symbol, balance, risk)

        # Save plan to database
        new_plan = Strategy(user_id=current_user.id, symbol=symbol, plan_text=plan)
        db.session.add(new_plan)
        db.session.commit()

    return render_template('ask_mode.html', plan=plan)
