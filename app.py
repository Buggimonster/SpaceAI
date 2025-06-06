# ERSTAT HELE DENNE FUNKTION I DIN KODE
def calculate_income(initial_capital, days, daily_rate_pct, bonus_pct, reinvest, fixed_daily_addition, apply_fee):
    daily_rate = daily_rate_pct / 100
    bonus_rate = bonus_pct / 100
    
    total_earned_income = 0
    total_fixed_additions = 0
    total_fees = 0
    total_bonuses = 0
    current_capital = initial_capital
    reinvestment_pool = 0
    daily_results = []

    for day in range(1, days + 1):
        # --- Beregninger (uændret) ---
        base_daily_income = current_capital * daily_rate
        fee_amount = base_daily_income * 0.05 if apply_fee else 0
        bonus_amount = base_daily_income * bonus_rate
        daily_earned_income_net = base_daily_income - fee_amount + bonus_amount
        
        total_earned_income += daily_earned_income_net
        total_fees += fee_amount
        total_bonuses += bonus_amount
        total_fixed_additions += fixed_daily_addition
        
        total_added_to_pool = daily_earned_income_net + fixed_daily_addition
        
        # --- Rettet logik for reinvestering ---
        if reinvest:
            reinvestment_pool += total_added_to_pool
            if reinvestment_pool >= 50:
                num_reinvestments = int(reinvestment_pool / 50)
                reinvest_amount = num_reinvestments * 50
                current_capital += reinvest_amount
                reinvestment_pool -= reinvest_amount
        
        # Denne append-del er nu garanteret at have alle variable defineret
        daily_results.append({
            "day": day, "raw_income": base_daily_income, "fee": fee_amount, "bonus": bonus_amount,
            "net_income": daily_earned_income_net, "fixed_add": fixed_daily_addition,
            "total_pool": total_added_to_pool, "reinvest_pool": reinvestment_pool,
            "final_capital": current_capital
        })

    return total_earned_income, total_fixed_additions, total_fees, total_bonuses, current_capital, daily_results
