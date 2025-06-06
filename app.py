import streamlit as st
import pandas as pd
from io import BytesIO

# Brugerdefineret CSS for baggrund, tekst og knapper
st.markdown("""
    <style>
    /* Sætter gradient-baggrunden for hovedvinduet */
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(to right, #0d1b2a, #415a77);
    }
    /* Gør headeren gennemsigtig */
    [data-testid="stHeader"] {
        background-color: rgba(0, 0, 0, 0);
    }
    /* Generel tekst- og overskriftsfarve */
    .stApp, h1, h2, h3, h4, h5, h6, .st-emotion-cache-16idsys p {
        color: white;
    }
    /* Metrics farve */
    .stMetric [data-testid="stMetricLabel"],
    .stMetric [data-testid="stMetricValue"] {
        color: white;
    }
    
    /* --- KNAP STYLING --- */
    /* Styler den almindelige "Beregn"-knap */
    .stButton>button {
        border: 2px solid #C00;
        border-radius: 5px;
        color: black !important;
        background-color: #FF0000;
    }
    .stButton>button:hover {
        border-color: #A00;
        background-color: #D00000;
        color: black !important;
    }

    /* Simpel regel for at gøre teksten på download-knappen sort */
    div[data-testid="stDownloadButton"] a {
        color: black !important;
    }

    </style>
    """, unsafe_allow_html=True)


# ==============================================================================
# 1. ORDBOG FOR OVERSÆTTELSER
# ==============================================================================
translations = {
    'da': {
        "lang_selector_label": "Vælg sprog", "title": "Avanceret Investeringsberegner", "sidebar_header": "Indtast dine værdier",
        "initial_capital": "Startkapital ($)", "days": "Antal dage (d)", "daily_rate_pct": "Gennemsnitlig daglig indkomst (%)",
        "fixed_daily_addition": "Gennemsnitligt dagligt Team afkast ($)", "fixed_daily_addition_help": "Det gennemsnitlige afkast du forventer fra dit team hver dag.",
        "bonus_level": "S Kaptajn bonus niveau", "custom_bonus": "Eller indtast brugerdefineret bonus (%)",
        "reinvest_active": "Geinvester hver gang du har min. 50$", "apply_fee": "Fratræk 5% platform gebyr",
        "calculate_button": "Beregn", "results_header": "Resultat Oversigt", "total_net_income": "Samlet Netto Afkast",
        "total_net_income_help": "Den totale profit efter gebyrer og bonusser er medregnet.", "final_capital": "Endelig Kapital",
        "final_capital_help": "Din startkapital plus alle geninvesteringer.", "total_fixed_additions": "Samlede Faste Tillæg",
        "total_fixed_additions_help": "Den totale mængde penge du selv har tilføjet.", "total_bonus": "Samlet Bonus",
        "total_bonus_help": "Den samlede værdi af din bonus.", "total_fee": "Samlet Gebyr (5%)",
        "total_fee_help": "Det samlede beløb fratrukket i gebyr.", "daily_results_header": "Detaljeret Daglig Oversigt",
        "col_day": "Dag", "col_raw_income": "Rå-afkast ($)", "col_fee": "Gebyr (5%) ($)", "col_bonus": "Bonus ($)",
        "col_net_income": "Netto Afkast ($)", "col_fixed_add": "Fast Tillæg ($)", "col_total_pool": "Total til Pulje ($)",
        "col_reinvest_pool": "Reinvest Pulje ($)", "col_final_capital": "Kapital v/Dagens Slut ($)",
        "graph_header": "Kapital Vækst Over Tid", "expander_label": "Vis/skjul detaljeret dag-for-dag oversigt",
        "download_button_label": "Download resultater som Excel (.xlsx)", "download_button_short_label": "Download",
        "reset_button_label": "Nulstil Indtastning", "reinvest_interval_label": "Geninvesterings-interval (dage)",
        "reinvest_interval_help": "Skriv 1 for at geninvestere så ofte som muligt (hver dag).",
        "package_select_label": "Primær investeringspakke"
    },
    'en': {
        "lang_selector_label": "Select language", "title": "Advanced Investment Calculator", "sidebar_header": "Enter your values",
        "initial_capital": "Initial Capital ($)", "days": "Number of Days (d)", "daily_rate_pct": "Average Daily Income (%)",
        "fixed_daily_addition": "Average daily Team return ($)", "fixed_daily_addition_help": "The average return you expect from your team each day.",
        "bonus_level": "S Captain bonus level", "custom_bonus": "Or enter custom bonus (%)",
        "reinvest_active": "Reinvest every min. $50", "apply_fee": "Deduct 5% platform fee",
        "calculate_button": "Calculate", "results_header": "Result Summary", "total_net_income": "Total Net Return",
        "total_net_income_help": "The total profit after all fees and bonuses are included.", "final_capital": "Final Capital",
        "final_capital_help": "Your initial capital plus all reinvestments.", "total_fixed_additions": "Total Fixed Additions",
        "total_fixed_additions_help": "The total amount of money you have added yourself.", "total_bonus": "Total Bonus",
        "total_bonus_help": "The total value of your bonus.", "total_fee": "Total Fee (5%)",
        "total_fee_help": "The total amount deducted as a fee.", "daily_results_header": "Detailed Daily Overview",
        "col_day": "Day", "col_raw_income": "Raw Return ($)", "col_fee": "Fee (5%) ($)", "col_bonus": "Bonus ($)",
        "col_net_income": "Net Return ($)", "col_fixed_add": "Fixed Add. ($)", "col_total_pool": "Total to Pool ($)",
        "col_reinvest_pool": "Reinvest Pool ($)", "col_final_capital": "Capital at Day End ($)",
        "graph_header": "Capital Growth Over Time", "expander_label": "Show/hide detailed day-by-day overview",
        "download_button_label": "Download results as Excel (.xlsx)", "download_button_short_label": "Download",
        "reset_button_label": "Reset Inputs", "reinvest_interval_label": "Reinvestment Interval (days)",
        "reinvest_interval_help": "Enter 1 to reinvest as often as possible (every day).",
        "package_select_label": "Primary investment package"
    }
}

# Beregningsfunktion (uændret)
def calculate_income(initial_capital, days, daily_rate_pct, bonus_pct, reinvest, reinvest_interval, reinvestment_unit, fixed_daily_addition, apply_fee):
    daily_rate = daily_rate_pct / 100; bonus_rate = bonus_pct / 100
    if reinvest_interval < 1: reinvest_interval = 1
    total_earned_income = 0; total_fixed_additions = 0; total_fees = 0; total_bonuses = 0
    current_capital = initial_capital; reinvestment_pool = 0; daily_results = []
    for day in range(1, days + 1):
        base_daily_income = current_capital * daily_rate
        fee_amount = base_daily_income * 0.05 if apply_fee else 0
        bonus_amount = base_daily_income * bonus_rate
        daily_earned_income_net = base_daily_income - fee_amount + bonus_amount
        total_earned_income += daily_earned_income_net; total_fees += fee_amount; total_bonuses += bonus_amount
        total_fixed_additions += fixed_daily_addition
        total_added_to_pool = daily_earned_income_net + fixed_daily_addition
        reinvestment_pool += total_added_to_pool
        if reinvest and (day % reinvest_interval == 0):
            if reinvestment_pool >= reinvestment_unit:
                num_units = int(reinvestment_pool / reinvestment_unit)
                reinvest_amount = num_units * reinvestment_unit
                if reinvest_amount > 0:
                    current_capital += reinvest_amount
                    reinvestment_pool -= reinvest_amount
        daily_results.append({
            "day": day, "raw_income": base_daily_income, "fee": fee_amount, "bonus": bonus_amount,
            "net_income": daily_earned_income_net, "fixed_add": fixed_daily_addition,
            "total_pool": total_added_to_pool, "reinvest_pool": reinvestment_pool,
            "final_capital": current_capital
        })
    return total_earned_income, total_fixed_additions, total_fees, total_bonuses, current_capital, daily_results

# Funktion til at konvertere DataFrame til Excel i hukommelsen (uændret)
def to_excel(df):
    output = BytesIO();
    with pd.ExcelWriter(output, engine='openpyxl') as writer: df.to_excel(writer, index=False, sheet_name='Results')
    return output.getvalue()

# ==============================================================================
# SPROG OG UI SETUP (uændret)
# ==============================================================================
if 'lang' not in st.session_state: st.session_state.lang = 'da'
lang_options = {'Dansk': 'da', 'English': 'en'}

selected_lang_name = st.sidebar.selectbox(label="Vælg sprog / Select language", options=lang_options.keys(), index=list(lang_options.values()).index(st.session_state.lang))
st.session_state.lang = lang_options[selected_lang_name]
texts = translations[st.session_state.lang]

# --- HOVEDSIDE SETUP ---
logo_url = "https://raw.githubusercontent.com/Buggimonster/SpaceAI/591366f7037c4b66479ce01fac236b4053d01c45/logo.png"
c1, c2, c3 = st.columns([1,2,1]);
with c2:
    st.image(logo_url)
    
    # NYT: Credit-tekst indsat her, under logoet i den midterste kolonne
    credit_text = "Created by Buggi - Credit go to fisatecs OG design which lead to this enhanced version"
    st.markdown(
        f'<p style="text-align: center; color: #FF4444; font-style: italic; font-size: 0.85em;">{credit_text}</p>',
        unsafe_allow_html=True
    )

st.title(texts['title'])

# --- SIDEBAR SETUP ---
st.sidebar.header(texts['sidebar_header'])
initial_capital = st.sidebar.number_input(texts['initial_capital'], min_value=0.0, value=1000.0, step=100.0)
days = st.sidebar.number_input(texts['days'], min_value=1, value=30, step=1)
daily_rate_pct = st.sidebar.number_input(texts['daily_rate_pct'], min_value=0.0, value=1.5, step=0.1)
fixed_daily_addition = st.sidebar.number_input(texts['fixed_daily_addition'], min_value=0.0, value=0.0, step=10.0, help=texts['fixed_daily_addition_help'])
st.sidebar.markdown("---")
bonus_options = {"S0 (0%)": 0, "S1 (10%)": 10, "S2 (15%)": 15, "S3 (25%)": 25, "S4 (35%)": 35}
bonus_choice = st.sidebar.radio(texts['bonus_level'], list(bonus_options.keys()))
bonus_pct = bonus_options[bonus_choice]
custom_bonus = st.sidebar.number_input(texts['custom_bonus'], min_value=0.0, value=0.0, step=1.0)
if custom_bonus > 0: bonus_pct = custom_bonus

# Re-investerings sektion
reinvest = st.sidebar.checkbox(texts['reinvest_active'], value=True)
reinvest_interval, reinvestment_unit = 1, 50
if reinvest:
    reinvest_interval = st.sidebar.number_input(texts['reinvest_interval_label'], min_value=1, value=7, step=1, help=texts['reinvest_interval_help'])
    package_options = {
        "Pakke 1 (enheder af 50$)": 50,
        "Pakke 2 (enheder af 1000$)": 1000,
        "Pakke 3 (enheder af 10.000$)": 10000,
        "Pakke 4 (enheder af 100.000$)": 100000
    }
    package_choice = st.sidebar.selectbox(texts['package_select_label'], options=package_options.keys())
    reinvestment_unit = package_options[package_choice]

apply_fee = st.sidebar.checkbox(texts['apply_fee'], value=True)

if st.sidebar.button(texts['reset_button_label']): st.rerun()

# --- BEREGNING OG RESULTATER ---
if st.button(texts['calculate_button']):
    total_earned_income, total_fixed_additions, total_fees, total_bonuses, final_capital, daily_results = calculate_income(
        initial_capital, days, daily_rate_pct, bonus_pct, reinvest, reinvest_interval, reinvestment_unit, fixed_daily_addition, apply_fee)
    
    results_df = pd.DataFrame(daily_results)
    results_df_renamed = results_df.rename(columns={
        "day": texts['col_day'], "raw_income": texts['col_raw_income'], "fee": texts['col_fee'],
        "bonus": texts['col_bonus'], "net_income": texts['col_net_income'], "fixed_add": texts['col_fixed_add'],
        "total_pool": texts['col_total_pool'], "reinvest_pool": texts['col_reinvest_pool'],
        "final_capital": texts['col_final_capital']})
    
    st.header(texts['results_header'])
    c1, c2 = st.columns(2); c1.metric(texts['total_net_income'], f"${total_earned_income:,.2f}", help=texts['total_net_income_help']); c2.metric(texts['final_capital'], f"${final_capital:,.2f}", help=texts['final_capital_help'])
    c1, c2, c3 = st.columns(3); c1.metric(texts['total_fixed_additions'], f"${total_fixed_additions:,.2f}", help=texts['total_fixed_additions_help']); c2.metric(texts['total_bonus'], f"${total_bonuses:,.2f}", help=texts['total_bonus_help']); c3.metric(texts['total_fee'], f"${total_fees:,.2f}", help=texts['total_fee_help'])
    st.divider()

    st.subheader(texts['graph_header'])
    chart_data = results_df.rename(columns={"day": "Day"}).set_index("Day")
    st.line_chart(chart_data['final_capital'])

    excel_data = to_excel(results_df_renamed)
    st.divider()

    dl_col1, dl_col2 = st.columns([3, 1])
    with dl_col1: st.markdown(f"<p style='text-align: right; color: white; padding-top: 1em;'>{texts['download_button_label']}</p>", unsafe_allow_html=True)
    with dl_col2: st.download_button(label=texts['download_button_short_label'], data=excel_data, file_name='investment_results.xlsx', mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

    st.divider()
    
    with st.expander(texts['expander_label']):
        st.subheader(texts['daily_results_header'])
        st.dataframe(results_df_renamed.style.format(formatter="{:,.2f}", subset=pd.IndexSlice[:, results_df_renamed.columns[1:]]), use_container_width=True)
