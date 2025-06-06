import streamlit as st
import pandas as pd

def calculate_income(initial_capital, days, daily_rate_pct, bonus_pct, reinvest, fixed_daily_addition):
    """
    Beregner afkast, hvor det faste tillæg lægges til dagens afkast og indgår i geninvesteringspuljen.
    """
    daily_rate = daily_rate_pct / 100
    bonus_rate = bonus_pct / 100
    
    effective_daily_rate = daily_rate * (1 + bonus_rate)
    
    total_earned_income = 0
    total_fixed_additions = 0 # Ny variabel til at spore samlede faste tillæg
    current_capital = initial_capital
    reinvestment_pool = 0

    daily_results = []

    for day in range(1, days + 1):
        # 1. Beregn dagens afkast KUN baseret på nuværende kapital
        daily_earned_income = current_capital * effective_daily_rate
        total_earned_income += daily_earned_income
        
        # 2. Læg dagens afkast og det faste tillæg sammen
        total_added_to_pool = daily_earned_income + fixed_daily_addition
        
        # 3. Tilføj den samlede sum til geninvesteringspuljen
        if reinvest:
            reinvestment_pool += total_added_to_pool
            # Tjek om vi kan geninvestere $50
            if reinvestment_pool >= 50:
                num_reinvestments = int(reinvestment_pool / 50)
                reinvest_amount = num_reinvestments * 50
                
                # Føj til kapitalen og træk fra puljen
                current_capital += reinvest_amount
                reinvestment_pool -= reinvest_amount
        else:
            # Hvis geninvestering er slået fra, går afkastet tabt i denne model,
            # da det kun er puljen, der øger kapitalen. Man kan justere dette, hvis det ønskes.
            pass

        # Spor de samlede faste tillæg
        total_fixed_additions += fixed_daily_addition
        
        daily_results.append({
            "Dag": day,
            "Optjent Afkast ($)": daily_earned_income,
            "Fast Tillæg ($)": fixed_daily_addition,
            "Total til Pulje ($)": total_added_to_pool,
            "Reinvest Pulje ($)": reinvestment_pool,
            "Kapital ved Dagens Slut ($)": current_capital
        })

    return total_earned_income, total_fixed_additions, current_capital, daily_results


# --- Streamlit Brugerflade ---
st.title("Avanceret Investeringsberegner")

# Input-felter i sidebar
st.sidebar.header("Indtast dine værdier")
initial_capital = st.sidebar.number_input("Startkapital ($)", min_value=0.0, value=1000.0, step=100.0)
days = st.sidebar.number_input("Antal dage (d)", min_value=1, value=30, step=1)
daily_rate_pct = st.sidebar.number_input("Gennemsnitlig daglig indkomst (%)", min_value=0.0, value=1.5, step=0.1)
fixed_daily_addition = st.sidebar.number_input("Dagligt fast tillæg ($)", min_value=0.0, value=0.0, step=10.0, help="Et fast beløb, der lægges i geninvesteringspuljen hver dag.")

# Bonus-valg
st.sidebar.markdown("---")
bonus_options = {"S0 (0%)": 0, "S1 (10%)": 10, "S2 (15%)": 15, "S3 (25%)": 25, "S4 (35%)": 35}
bonus_choice = st.sidebar.radio("Bonus Level", list(bonus_options.keys()))
bonus_pct = bonus_options[bonus_choice]
custom_bonus = st.sidebar.number_input("Eller indtast brugerdefineret bonus (%)", min_value=0.0, value=0.0, step=1.0)
if custom_bonus > 0:
    bonus_pct = custom_bonus

# Geninvestering
reinvest = st.sidebar.checkbox("Geninvestering aktiv?", value=True)

# Beregningsknap
if st.button("Beregn"):
    total_earned_income, total_fixed_additions, final_capital, daily_results = calculate_income(
        initial_capital, days, daily_rate_pct, bonus_pct, reinvest, fixed_daily_addition
    )
    
    st.header("Resultat Oversigt")
    
    # Opdelte resultater for klarhed
    col1, col2 = st.columns(2)
    col1.metric("Samlet Optjent Afkast", f"${total_earned_income:,.2f}", help="Den totale profit genereret fra din kapital og daglige rate.")
    col2.metric("Samlede Faste Tillæg", f"${total_fixed_additions:,.2f}", help="Den totale mængde penge du selv har tilføjet via det daglige tillæg.")
    
    st.metric("Endelig Kapital", f"${final_capital:,.2f}", help="Din startkapital plus alle geninvesteringer.")

    st.divider()
    
    # Udvidet daglig oversigt
    st.subheader("Detaljeret Daglig Oversigt")
    results_df = pd.DataFrame(daily_results)
    
    # Formatering for læselighed
    st.dataframe(results_df.style.format({
        'Optjent Afkast ($)': '{:,.2f}',
        'Fast Tillæg ($)': '{:,.2f}',
        'Total til Pulje ($)': '{:,.2f}',
        'Reinvest Pulje ($)': '{:,.2f}',
        'Kapital ved Dagens Slut ($)': '{:,.2f}'
    }), use_container_width=True)
