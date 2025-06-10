import streamlit as st

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
        "sidebar_header": "Indtast dine værdier",
        "lang_select_label": "Vælg sprog",
        "reset_button_label": "Nulstil",
        "input_A": "Today's revenue",
        "input_B": "SAT Value (US$)",
        "input_C": "Team Profit (SAT)",
        "input_D": "Choose S Captain bonus",
        "output_F": "Team Profit (US$)",
        "output_G": "Investment Profit (US$)",
        "output_H": "Total profit of the day (US$)"
    },
    'en': {
        "title": "Daily Profit Calculator",
        "calculate_button": "Calculate",
        "results_header": "Results",
        "sidebar_header": "Enter your values",
        "lang_select_label": "Select language",
        "reset_button_label": "Reset",
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

# --- SIDEBAR SETUP ---
selected_lang_name = st.sidebar.selectbox(
    label="Vælg sprog / Select language",
    options=lang_options.keys(),
    index=list(lang_options.values()).index(st.session_state.lang)
)
st.session_state.lang = lang_options[selected_lang_name]
texts = translations[st.session_state.lang]

# --- HOVEDSIDE SETUP ---
logo_url = "https://raw.githubusercontent.com/Buggimonster/SpaceAI/591366f7037c4b66479ce01fac236b4053d01c45/logo.png"
c1, c2, c3 = st.columns([1,2,1])
with c2:
    st.image(logo_url)
st.title(texts['title'])
st.markdown("---")


# --- INPUT-FELTER I SIDEBAR ---
st.sidebar.header(texts['sidebar_header'])

# Input A2 - med 4 decimaler og default 0
todays_revenue = st.sidebar.number_input(
    label=texts['input_A'], value=0.0, step=100.0, format="%.4f"
)

# Input B2 - med 4 decimaler og default 0
sat_value = st.sidebar.number_input(
    label=texts['input_B'], value=0.0, step=0.01, format="%.4f"
)

# Input C2 - med 4 decimaler og default 0
team_profit_sat = st.sidebar.number_input(
    label=texts['input_C'], value=0.0, step=100.0, format="%.4f"
)

# Input D2
bonus_options = [10, 15, 25, 35]
s_captain_bonus_pct = st.sidebar.selectbox(
    label=texts['input_D'],
    options=bonus_options,
    format_func=lambda x: f"{x}%" 
)

st.sidebar.markdown("---")

# Nulstil-knap i sidebar
if st.sidebar.button(texts['reset_button_label']):
    st.rerun()


# --- BEREGNING OG RESULTATER PÅ HOVEDSIDEN ---
# Placer Beregn-knappen i midten
_, col_button, _ = st.columns([1,1,1])
with col_button:
    calculate_clicked = st.button(texts['calculate_button'], use_container_width=True)


if calculate_clicked:
    # Konstanter og værdier fra input
    platform_fee_pct = 0.05  # Fast 5%
    bonus_pct_decimal = s_captain_bonus_pct / 100
    
    # Formel F2 = B2 * C2
    team_profit_usd = sat_value * team_profit_sat
    
    # Formel H2 = A2 - (((A2 - F2) / (1 + D2)) * E2)
    denominator = 1 + bonus_pct_decimal
    if denominator == 0:
        st.error("Bonus Procent kan ikke være -100%.")
    else:
        total_profit_of_the_day = todays_revenue - (((todays_revenue - team_profit_usd) / denominator) * platform_fee_pct)
        
        # Formel G2 = H2 - F2
        investment_profit_usd = total_profit_of_the_day - team_profit_usd

        # Vis resultater
        st.markdown("---")
        st.header(texts['results_header'])
        
        # Opret kolonner for et pænt layout
        col1, col2, col3 = st.columns(3)
        
        # Vis outputs med 4 decimaler
        with col1:
            st.metric(label=texts['output_F'], value=f"${team_profit_usd:,.4f}")
        
        with col2:
            st.metric(label=texts['output_G'], value=f"${investment_profit_usd:,.4f}")
            
        with col3:
            st.metric(label=texts['output_H'], value=f"${total_profit_of_the_day:,.4f}")
