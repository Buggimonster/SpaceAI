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
        "initial_capital": "Startkapital (<span class="math-inline">\)",
"days"\: "Antal dage \(d\)",
"daily\_rate\_pct"\: "Gennemsnitlig daglig indkomst \(%\)",
"fixed\_daily\_addition"\: "Dagligt fast tillæg \(</span>)",
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
        "col_raw_income": "Rå-afkast (<span class="math-inline">\)",
"col\_fee"\: "Gebyr \(5%\) \(</span>)",
        "col_bonus": "Bonus (<span class="math-inline">\)",
"col\_net\_income"\: "Netto Afkast \(</span>)",
        "col_fixed_add": "Fast Tillæg (<span class="math-inline">\)",
"col\_total\_pool"\: "Total til Pulje \(</span>)",
        "col_reinvest_pool": "Reinvest Pulje (<span class="math-inline">\)",
"col\_final\_capital"\: "Kapital v/Dagens Slut \(</span>)"
    },
    'en': {
        # General & Sidebar
        "lang_selector_label": "Select language",
        "title": "Advanced Investment Calculator",
        "sidebar_header": "Enter your values",
        "initial_capital": "Initial Capital (<span class="math-inline">\)",
"days"\: "Number of Days \(d\)",
"daily\_rate\_pct"\: "Average Daily Income \(%\)",
"fixed\_daily\_addition"\: "Fixed Daily Addition \(</span>)",
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
        "col_raw_income": "Raw Return (<span class="math-inline">\)",
"col\_fee"\: "Fee \(5%\) \(</span>)",
        "col_bonus": "Bonus (<span class="math-inline">\)",
"col\_net\_income"\: "Net Return \(</span>)",
        "col_fixed_add": "Fixed Add. (<span class="math-inline">\)",
"col\_total\_pool"\: "Total to Pool \(</span>)",
        "col_reinvest_pool": "Reinvest Pool (<span class="math-inline">\)",
"col\_final\_capital"\: "Capital at Day End \(</span>)"
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
# HÅNDTERING AF SPROGVALG
# ==============================================================================
if 'lang' not in st.session_state:
    st.session_state.lang = 'da'

lang_options = {'Dansk': 'da', 'English': 'en'}

# ==============================================================================
# BRUGERFLADE
# ==============================================================================
st.title(texts['title'])

# --- SIDEBAR STARTER HER ---

# Logo indsat med det korrekte, rå link fra GitHub
logo_url = "https://raw.githubusercontent.com/Buggimonster/SpaceAI/591366f7037c4b66479ce01fac236b4053d01c45/logo.png"
st.sidebar.image(logo_url)

selected_lang_name = st.sidebar.selectbox(
    label="Vælg sprog / Select language",
    options=lang_options.keys(),
    index=list(lang_options.values()).index(st.session_state.lang)
)
# Opdater session state og hent den korrekte ordbog
st.session_state.lang = lang_options[selected_lang_name]
texts = translations[st.session_state.lang]

st.sidebar.header(texts['sidebar_header'])
initial_capital = st.sidebar.number_input(texts['initial_
