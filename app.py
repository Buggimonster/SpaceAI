import streamlit as st
import pandas as pd

# ==============================================================================
# 1. ORDBOG FOR OVERSÆTTELSER
# ==============================================================================
translations = {
    'da': {
        # Generelt & Sidebar
        "lang_selector_label": "Vælg sprog",
        "title": "Avanceret Investeringsberegner",
        "sidebar_header": "Indtast dine værdier",
        "initial_capital": "Startkapital ($)",
        "days": "Antal dage (d)",
        "daily_rate_pct": "Gennemsnitlig daglig indkomst (%)",
        "fixed_daily_addition": "Dagligt fast tillæg ($)",
        "fixed_daily_addition_help": "Et fast beløb, der lægges i geninvesteringspuljen hver dag.",
        "bonus_level": "Bonusniveau",
        "custom_bonus": "Eller indtast brugerdefineret bonus (%)",
        "reinvest_active": "Geninvestering aktiv?",
        "apply_fee": "Fratræk 5% gebyr (før bonus)",
        "calculate_button": "Beregn",
        # Resultater
        "results_header": "Resultat Oversigt",
        "total_net_income": "Samlet Netto Afkast",
        "total_net_income_help": "Den totale profit efter gebyrer og bonusser er medregnet.",
        "final_capital": "Endelig Kapital",
        "final_capital_help": "Din startkapital plus alle geninvesteringer.",
        "total_fixed_additions": "Samlede Faste Tillæg",
        "total_fixed_additions_help": "Den totale mængde penge du selv har tilføjet.",
        "total_bonus": "Samlet Bonus",
        "total_bonus_help": "Den samlede værdi af din bonus.",
        "total_fee": "Samlet Gebyr (5%)",
        "total_fee_help": "Det samlede beløb fratrukket i gebyr.",
        # Tabel
        "daily_results_header": "Detaljeret Daglig Oversigt",
        "col_day": "Dag",
        "col_raw_income": "Rå-afkast ($)",
        "col_fee": "Gebyr (5%) ($)",
        "col_bonus": "Bonus ($)",
        "col_net_income": "Netto Afkast ($)",
        "col_fixed_add": "Fast Tillæg ($)",
        "col_total_pool": "Total til Pulje ($)",
        "col_reinvest_pool": "Reinvest Pulje ($)",
        "col_final_capital": "Kapital v/Dagens Slut ($)"
    },
    'en': {
        # General & Sidebar
        "lang_selector_label": "Select language",
        "title": "Advanced Investment Calculator",
        "sidebar_header": "Enter your values",
        "initial_capital": "Initial Capital ($)",
        "days": "Number of Days (d)",
        "daily_rate_pct": "Average Daily Income (%)",
        "fixed_daily_addition": "Fixed Daily Addition ($)",
        "fixed_daily_addition_help": "A fixed amount added to the reinvestment pool each day.",
        "bonus_level": "Bonus Level",
        "custom_bonus": "Or enter custom bonus (%)",
        "reinvest_active": "Reinvestment active?",
        "apply_fee": "Deduct 5% fee (before bonus)",
        "calculate_button": "Calculate",
        # Results
        "results_header": "Result Summary",
        "total_net_income": "Total Net Return",
        "total_net_income_help": "The total profit after all fees and bonuses are included.",
        "final_capital": "Final Capital",
        "final_capital_help": "Your initial capital plus all reinvestments.",
        "total_fixed_additions": "Total Fixed Additions",
        "total_fixed_additions_help": "The total amount of money you have added yourself.",
        "total_bonus": "Total Bonus",
        "total_bonus_help": "The total value of your bonus.",
        "total_fee": "Total Fee (5%)",
        "total_fee_help": "The total amount deducted as a fee.",
        # Table
        "daily_results_header": "Detailed Daily Overview",
        "col_day": "Day",
        "col_raw_income": "Raw Return ($)",
        "col_fee": "Fee (5%) ($)",
        "col_bonus": "Bonus ($)",
        "col_net_income": "Net Return ($)",
        "col_fixed_add": "Fixed Add. ($)",
        "col_total_pool": "Total to Pool ($)",
        "col_reinvest_pool": "Reinvest Pool ($)",
        "col_final_capital": "Capital at Day End ($)"
    }
}

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
# SPROG OG UI SETUP
# ==============================================================================

# Sæt et standardsprog, hvis intet er valgt i sessionen
if 'lang' not in st.session_state:
    st.session_state.lang = 'da'

# Definer sprog til dropdown-menuen
lang_options = {'Dansk': 'da', 'English': 'en'}

# --- RÆKKEFØLGEN ER RETTET HER ---

# 1. Opret sprogvælgeren FØRST, så vi ved hvilket sprog der skal bruges
selected_lang_name = st.sidebar.selectbox(
    label="Vælg sprog / Select language",
    options=lang_options.keys(),
    index=list(lang_options.values()).index(st.session_state.lang)
)

# 2. Opdater sproget i session state og hent den korrekte ordbog
st.session_state.lang = lang_options[selected_lang_name]
texts = translations[st.session_state.lang]

# 3. Nu kan vi bygge resten af UI'en med de korrekte tekster
st.title(texts['title'])

# Indsæt logo
logo_url = "https://raw.githubusercontent.com/Buggimonster/SpaceAI/591366f7037c4b66479ce01fac236b4053d01c45/logo.png"
st.sidebar.image(logo_url)

# Fortsæt med resten af sidebaren
st.sidebar.header(texts['sidebar_header'])
initial_capital = st.sidebar.number_input(texts['initial_capital'], min_value=0.0, value=1000.0, step=100.0)
days = st.sidebar.number_input(texts['days'], min_value=1, value=30, step=1)
daily_rate_pct = st.sidebar.number_input(texts['daily_rate_pct'], min_value=0.0, value=1.5, step=0.1)
fixed_daily_addition = st.sidebar.number_input(
    texts['fixed_daily_addition'], min_value=0.0, value=0.0, step=10.0, help=texts['fixed_daily_addition_help']
)

st.sidebar.markdown("---")
bonus_options = {"S0 (0%)": 0, "S1 (10%)": 10, "S2 (15%)": 15, "S3 (25%)": 25, "S4 (35%)": 35}
bonus_choice = st.sidebar.radio(texts['bonus_level'], list(bonus_options.keys()))
bonus_pct = bonus_options[bonus_choice]
custom_bonus = st.sidebar.number_input(texts['custom_bonus'], min_value=0.0, value=0.0, step=1.0)
if custom_bonus > 0:
    bonus_pct = custom_bonus

reinvest = st.sidebar.checkbox(texts['reinvest_active'], value=True)
apply_fee = st.sidebar.checkbox(texts['apply_fee'], value=False)

if st.button(texts['calculate_button']):
    total_earned_income, total_fixed_additions, total_fees, total_bonuses, final_capital, daily_results = calculate_income(
        initial_capital, days, daily_rate_pct, bonus_pct, reinvest, fixed_daily_addition, apply_fee
    )
    
    st.header(texts['results_header'])
    
    col1, col2 = st.columns(2)
    col1.metric(texts['total_net_income'], f"${total_earned_income:,.2f}", help=texts['total_net_income_help'])
    col2.metric(texts['final_capital'], f"${final_capital:,.2f}", help=texts['final_capital_help'])

    col1, col2, col3 = st.columns(3)
    col1.metric(texts['total_fixed_additions'], f"${total_fixed_additions:,.2f}", help=texts['total_fixed_additions_help'])
    col2.metric(texts['total_bonus'], f"${total_bonuses:,.2f}", help=texts['total_bonus_help'])
    col3.metric(texts['total_fee'], f"${total_fees:,.2f}", help=texts['total_fee_help'])
    
    st.divider()
    
    st.subheader(texts['daily_results_header'])
    results_df = pd.DataFrame(daily_results)
    
    # Omdøb kolonner baseret på valgt sprog
    results_df = results_df.rename(columns={
        "day": texts['col_day'], "raw_income": texts['col_raw_income'], "fee": texts['col_fee'],
        "bonus": texts['col_bonus'], "net_income": texts['col_net_income'], "fixed_add": texts['col_fixed_add'],
        "total_pool": texts['col_total_pool'], "reinvest_pool": texts['col_reinvest_pool'],
        "final_capital": texts['col_final_capital']
    })
    
    st.dataframe(results_df.style.format({
        texts['col_raw_income']: '{:,.2f}', texts['col_fee']: '{:,.2f}', texts['col_bonus']: '{:,.2f}',
        texts['col_net_income']: '{:,.2f}', texts['col_fixed_add']: '{:,.2f}', texts['col_total_pool']: '{:,.2f}',
        texts['col_reinvest_pool']: '{:,.2f}', texts['col_final_capital']: '{:,.2f}'
    }), use_container_width=True)
