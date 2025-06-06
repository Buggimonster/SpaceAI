import streamlit as st
import pandas as pd

def calculate_income(initial_capital, days, daily_rate_pct, bonus_pct, reinvest, fixed_daily_addition, apply_fee):
    """
    Beregner afkast med den korrekte rækkefølge og beregning for gebyr og bonus.
    """
    # Grundlæggende rater
    daily_rate = daily_rate_pct / 100
    # Her konverteres bonusprocenten (f.eks. 10) til en rate (0.10)
    bonus_rate = bonus_pct / 100
    
    total_earned_income = 0
    total_fixed_additions = 0
    total_fees = 0
    total_bonuses = 0
    current_capital = initial_capital
    reinvestment_pool = 0

    daily_results = []

    for day in range(1, days + 1):
        # 1. Beregn det "rå" daglige afkast (uden bonus)
        base_daily_income = current_capital * daily_rate
        
        # 2. Beregn gebyr ud fra rå-afkastet (hvis valgt)
        fee_amount = 0
        if apply_fee:
            fee_amount = base_daily_income * 0.05
        
        # 3. Beregn bonus ud fra rå-afkastet
        bonus_amount = base_daily_income * bonus_rate
        
        # 4. Beregn dagens endelige netto-afkast
        daily_earned_income_net = base_daily_income - fee_amount + bonus_amount
        
        # Opdater totaler for hele perioden
        total_earned_income += daily_earned_income_net
        total_fees += fee_amount
        total_bonuses += bonus_amount
        total_fixed_additions += fixed_daily_addition
        
        # Læg netto-afkast og det faste tillæg sammen
        total_added_to_pool = daily_earned_income_net + fixed_daily_addition
        
        # Håndter geninvesteringspuljen
        if reinvest:
            reinvestment_pool += total_added_to_pool
            if reinvestment_pool >= 50:
                num_reinvestments = int(reinvestment_pool / 50)
                reinvest_amount = num_reinvestments * 50
                
                current_capital += reinvest_amount
                reinvestment_pool -= reinvest_amount
        
        daily_results.append({
            "Dag": day,
            "Rå-afkast ($)": base_daily_income,
            "Gebyr (5%) ($)": fee_amount,
            "Bonus ($)": bonus_amount,
            "Netto Afkast ($)": daily_earned_income_net,
            "Fast Tillæg ($)": fixed_daily_addition,
            "Total til Pulje ($)": total_added_to_pool,
            "Reinvest Pulje ($)": reinvestment_pool,
            "Kapital ved Dagens Slut ($)": current_capital
        })

    return total_earned_income, total_fixed_additions, total_fees, total_bonuses, current_capital, daily_results


# --- Streamlit Brugerflade ---
st.title("Avanceret Investeringsberegner")

# Input-felter
st.sidebar.header("Indtast dine værdier")
initial_capital = st.sidebar.number_input("Startkapital ($)", min_value=0.0, value=1000.0, step=100.0)
days = st.sidebar.number_input("Antal dage (d)", min_value=1, value=30, step=1)
daily_rate_pct = st.sidebar.number_input("Gennemsnitlig daglig indkomst (%)", min_value=0.0, value=1.5, step=0.1)
fixed_daily_addition = st.sidebar.number_input("Dagligt fast tillæg ($)", min_value=0.0, value=0.0, step=10.0, help="Et fast beløb, der lægges i geninvesteringspuljen hver dag.")

# Indstillinger
st.sidebar.markdown("---")
bonus_options = {"S0 (0%)": 0, "S1 (10%)": 10, "S2 (15%)": 15, "S3 (25%)": 25, "S4 (35%)": 35}
bonus_choice = st.sidebar.radio("Bonus Level", list(bonus_options.keys()))
bonus_pct = bonus_options[bonus_choice]
custom_bonus = st.sidebar.number_input("Eller indtast brugerdefineret bonus (%)", min_value=0.0, value=0.0, step=1.0)
if custom_bonus > 0:
    bonus_pct = custom_bonus

# Checkbokse
reinvest = st.sidebar.checkbox("Geninvestering aktiv?", value=True)
apply_fee = st.sidebar.checkbox("Fratræk 5% gebyr (før bonus)", value=False)

# Beregningsknap
if st.button("Beregn"):
    # --------------------------------------------------------------------
    # RETTET HER: '/ 100' er fjernet, så vi sender den rene procent (f.eks. 10)
    # --------------------------------------------------------------------
    total_earned_income, total_fixed_additions, total_fees, total_bonuses, final_capital, daily_results = calculate_income(
        initial_capital, days, daily_rate_pct, bonus_pct, reinvest, fixed_daily_addition, apply_fee
    )
    
    st.header("Resultat Oversigt")
    
    col1, col2 = st.columns(2)
    col1.metric("Samlet Netto Afkast", f"${total_earned_income:,.2f}", help="Den totale profit efter gebyrer og bonusser er medregnet.")
    col2.metric("Endelig Kapital", f"${final_capital:,.2f}", help="Din startkapital plus alle geninvesteringer.")

    col1, col2, col3 = st.columns(3)
    col1.metric("Samlede Faste Tillæg", f"${total_fixed_additions:,.2f}", help="Den totale mængde penge du selv har tilføjet.")
    col2.metric("Samlet Bonus", f"${total_bonuses:,.2f}", help="Den samlede værdi af din bonus.")
    col3.metric("Samlet Gebyr (5%)", f"${total_fees:,.2f}", help="Det samlede beløb fratrukket i gebyr.")
    
    st.divider()
    
    st.subheader("Detaljeret Daglig Oversigt")
    results_df = pd.DataFrame(daily_results)
    
    column_order = [
        "Dag", "Rå-afkast ($)", "Gebyr (5%) ($)", "Bonus ($)", "Netto Afkast ($)", 
        "Fast Tillæg ($)", "Total til Pulje ($)", "Reinvest Pulje ($)", "Kapital ved Dagens Slut ($)"
    ]
    
    st.dataframe(results_df[column_order].style.format({
        'Rå-afkast ($)': '{:,.2f}',
        'Gebyr (5%) ($)': '{:,.2f}',
        'Bonus ($)': '{:,.2f}',
        'Netto Afkast ($)': '{:,.2f}',
        'Fast Tillæg ($)': '{:,.2f}',
        'Total til Pulje ($)': '{:,.2f}',
        'Reinvest Pulje ($)': '{:,.2f}',
        'Kapital ved Dagens Slut ($)': '{:,.2f}'
    }), use_container_width=True)
