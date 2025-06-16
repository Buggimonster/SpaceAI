import streamlit as st
import pandas as pd
from io import BytesIO

# Brugerdefineret CSS for baggrund og styling
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
    .stApp, h1, h2, h3, h4, h5, h6, p {
        color: white;
    }
    /* Metrics farve */
    .stMetric [data-testid="stMetricLabel"],
    .stMetric [data-testid="stMetricValue"] {
        color: white;
    }
    /* Knap styling */
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
    </style>
    """, unsafe_allow_html=True)

# Ordbog for tekster til sprogvalg
translations = {
    'da': {
        "title": "Daglig Profit Beregner",
        "calculate_button": "Beregn",
        "results_header": "Resultater",
        "input_header": "Indtast dine værdier",
        "lang_select_label": "Sprog/Language",
        "reset_button_label": "Nulstil",
        "guide_expander_label": "Klik her for at se vejledning til input-felter",
        "input_A": "Dagens omsætning",
        "input_B": "SAT Værdi (US$)",
        "input_C": "Team Profit (SAT)",
        "input_D": "Vælg S Kaptajn bonus",
        "output_F": "Team Profit (US$)",
        "output_G": "Investerings-profit (US$)",
        "output_H": "Dagens totale profit (US$)"
    },
    'en': {
        "title": "Daily Profit Calculator",
        "calculate_button": "Calculate",
        "results_header": "Results",
        "input_header": "Enter your values",
        "lang_select_label": "Language/Sprog",
        "reset_button_label": "Reset",
        "guide_expander_label": "Click here for a guide to the input fields",
        "input_A": "Today's revenue",
        "input_B": "SAT Value (US$)",
        "input_C": "Team Profit (SAT)",
        "input_D": "Choose S Captain bonus",
        "output_F": "Team Profit (US$)",
        "output_G": "Investment Profit (US$)",
        "output_H": "Total profit of the day (US$)"
    }
}

# ==============================================================================
# SPROG OG UI SETUP
# ==============================================================================
if 'lang' not in st.session_state:
    st.session_state.lang = 'da'

lang_options = {'Dansk': 'da', 'English': 'en'}

# Placer Sprogvælger øverst til højre
_, lang_col = st.columns([3, 1])
with lang_col:
    selected_lang_name = st.selectbox(
        label=translations['da']['lang_select_label'], 
        options=lang_options.keys(),
        index=list(lang_options.values()).index(st.session_state.lang),
        label_visibility="collapsed"
    )
    st.session_state.lang = lang_options[selected_lang_name]

# Hent den korrekte ordbog baseret på valg
texts = translations[st.session_state.lang]

# --- HOVEDSIDE LAYOUT ---
logo_url = "https://raw.githubusercontent.com/Buggimonster/SpaceAI/591366f7037c4b66479ce01fac236b4053d01c45/logo.png"
c1, c2, c3 = st.columns([1,2,1])
with c2:
    st.image(logo_url)
    credit_text = "Created by Buggi"
    st.markdown(
        f'<p style="text-align: center; color: #FF4444; font-style: italic; font-size: 1.0em;">{credit_text}</p>',
        unsafe_allow_html=True
    )

st.title(texts['title'])

# Vejledning i en "expander" sektion
# OPDATERET: URL'en er nu den korrekte, permanente sti til billedet
image_url = "https://raw.githubusercontent.com/Buggimonster/SpaceAI/b3553ac3396928e06363fdc56d90845129f67460/adv-calc.jpg"
with st.expander(texts['guide_expander_label']):
    st.image(image_url)

st.markdown("---")


# --- INPUT-FELTER PÅ HOVEDSIDEN ---
st.header(texts['input_header'])

# Opdel inputs i to kolonner for et pænere layout
col1, col2 = st.columns(2)

with col1:
    todays_revenue = st.number_input(
        label=texts['input_A'], value=0.0, step=100.0, format="%.4f"
    )
    sat_value = st.number_input(
        label=texts['input_B'], value=0.0, step=0.01, format="%.4f"
    )

with col2:
    team_profit_sat = st.number_input(
        label=texts['input_C'], value=0.0, step=100.0, format="%.4f"
    )
    bonus_options = [10, 15, 25, 35]
    s_captain_bonus_pct = st.selectbox(
        label=texts['input_D'],
        options=bonus_options,
        format_func=lambda x: f"{x}%" 
    )

st.markdown("---")

# --- KNAPPER TIL HANDLINGER ---
btn_col1, btn_col2, _ = st.columns([1, 1, 2])

with btn_col1:
    calculate_clicked = st.button(texts['calculate_button'], use_container_width=True)

with btn_col2:
    if st.button(texts['reset_button_label'], use_container_width=True):
        st.rerun()


# --- BEREGNING OG RESULTATER ---
if calculate_clicked:
    platform_fee_pct = 0.05
    bonus_pct_decimal = s_captain_bonus_pct / 100
    team_profit_usd = sat_value * team_profit_sat
    
    denominator = 1 + bonus_pct_decimal
    if denominator == 0:
        st.error("Bonus Procent kan ikke være -100%.")
    else:
        total_profit_of_the_day = todays_revenue - (((todays_revenue - team_profit_usd) / denominator) * platform_fee_pct)
        investment_profit_usd = total_profit_of_the_day - team_profit_usd

        st.markdown("---")
        st.header(texts['results_header'])
        
        res_col1, res_col2, res_col3 = st.columns(3)
        with res_col1:
            st.metric(label=texts['output_F'], value=f"${team_profit_usd:,.4f}")
        with res_col2:
            st.metric(label=texts['output_G'], value=f"${investment_profit_usd:,.4f}")
        with res_col3:
            st.metric(label=texts['output_H'], value=f"${total_profit_of_the_day:,.4f}")
