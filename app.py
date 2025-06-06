import streamlit as st
import pandas as pd

# Brugerdefineret CSS for baggrund, tekst og knapper
st.markdown("""
    <style>
    /* Sætter gradient-baggrunden for hovedvinduet */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(to right, #0d1b2a, #415a77);
    }

    /* Gør headeren gennemsigtig, så baggrunden ses igennem */
    [data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0);
    }

    /* Gør al primær tekst og alle overskrifter hvide */
    .stApp, h1, h2, h3, h4, h5, h6, .st-emotion-cache-16idsys p {
        color: white;
    }

    /* Sikrer at tal-visninger (metrics) også bliver hvide */
    .stMetric [data-testid="stMetricLabel"],
    .stMetric [data-testid="stMetricValue"] {
        color: white;
    }
    
    /* Styler "Beregn"-knappen */
    .stButton>button {
        border: 2px solid #C00;
        border-radius: 5px;
        color: black !important; /* Sort tekst, !important er for at gennemtvinge det */
        background-color: #FF0000; /* Rød baggrund */
    }

    /* Giver en effekt, når musen er over knappen */
    .stButton>button:hover {
        border-color: #A00;
        background-color: #D00000; /* Lidt mørkere rød */
        color: black !important;
    }

    </style>
    """, unsafe_allow_html=True)


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
        base_daily_income = current_capital * daily_rate
        fee_amount = base_daily_income * 0.05 if apply_fee else 0
        bonus_amount = base_daily_income * bonus_rate
        daily_earned_income_net = base_daily_income - fee_amount + bonus_amount
        
        total_earned_income += daily_earned_income_net
        total_fees += fee_amount
        total_bonuses += bonus_amount
        total_fixed_additions += fixed_daily_addition
        
        total_added_to_pool = daily_earned_income_net + fixed_daily_addition
        
        if reinvest:
            reinvestment_pool += total_added_to_pool
            if reinvestment_pool >= 50:
                num_reinvestments = int(reinvestment_pool / 50)
                reinvest_amount = num_reinvestments * 50
                
                current_capital += reinvest_amount
                reinvestment_pool -= reinvest_amount
        
        daily_results.append({
            "day": day, "raw_income": base_daily_income, "fee": fee_amount, "bonus": bonus_amount,
            "net_income": daily_earned_income_net, "fixed_add": fixed_daily_addition,
            "total_pool": total_added_to_pool, "reinvest_pool": reinvestment_pool,
            "final_capital": current_capital
        })

    return total_earned_income, total_fixed_additions, total_fees, total_bonuses, current_capital, daily_results

# ==============================================================================
# UI SETUP (Hardcoded på dansk)
# ==============================================================================

# --- HOVEDSIDE SETUP ---
logo_url = "https://raw.githubusercontent.com/Buggimonster/SpaceAI/591366f7037c4b66479ce01fac236b4053d01c45/logo.png"
col1, col2, col3 = st.columns([1,2,1])
with col2:
    st.image(logo_url)

st.title("Avanceret Investeringsberegner")

# --- SIDEBAR SETUP ---
st.sidebar.header("Indtast dine værdier")
initial_capital = st.sidebar.number_input("Startkapital ($)", min_value=0.0, value=1000.0, step=100.0)
days = st.sidebar.number_input("Antal dage (d)", min_value=1, value=30, step=1)
daily_rate_pct = st.sidebar.number_input("Gennemsnitlig daglig indkomst (%)", min_value=0.0, value=1.5, step=0.1)
fixed_daily_addition = st.sidebar.number_input(
    "Dagligt fast tillæg ($)", min_value=0.0, value=0.0, step=10.0, help="Et fast beløb, der lægges i geninvesteringspuljen hver dag."
)

st.sidebar.markdown("---")
bonus_options = {"S0 (0%)": 0, "S1 (10%)": 10, "S2 (15%)": 15, "S3 (25%)": 25, "S4 (35%)": 35}
bonus_choice = st.sidebar.radio("Bonusniveau", list(bonus_options.keys()))
bonus_pct = bonus_options[bonus_choice]
custom_bonus = st.sidebar.number_input("Eller indtast brugerdefineret bonus (%)", min_value=0.0, value=0.0, step=1.0)
if custom_bonus > 0:
    bonus_pct = custom_bonus

reinvest = st.sidebar.checkbox("Geninvestering aktiv?", value=True)
apply_fee = st.sidebar.checkbox("Fratræk 5% gebyr (før bonus)", value=False)

# --- BEREGNING OG RESULTATER ---
if st.button("Beregn"):
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
    
    results_df = results_df.rename(columns={
        "day": "Dag", "raw_income": "Rå-afkast ($)", "fee": "Gebyr (5%) ($)",
        "bonus": "Bonus ($)", "net_income": "Netto Afkast ($)", "fixed_add": "Fast Tillæg ($)",
        "total_pool": "Total til Pulje ($)", "reinvest_pool": "Reinvest Pulje ($)",
        "final_capital": "Kapital v/Dagens Slut ($)"
    })
    
    st.dataframe(results_df.style.format({
        "Rå-afkast ($)": '{:,.2f}', "Gebyr (5%) ($)": '{:,.2f}', "Bonus ($)": '{:,.2f}',
        "Netto Afkast ($)": '{:,.2f}', "Fast Tillæg ($)": '{:,.2f}', "Total til Pulje ($)": '{:,.2f}',
        "Reinvest Pulje ($)": '{:,.2f}', "Kapital v/Dagens Slut ($)": '{:,.2f}'
    }), use_container_width=True)
