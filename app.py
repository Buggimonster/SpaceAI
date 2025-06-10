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

# Ordbog for tekster (en simpel version til denne app)
translations = {
    'da': {
        "title": "Daglig Profit Beregner",
        "calculate_button": "Beregn",
        "results_header": "Resultater",
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
        "input_A": "Today's revenue",
        "input_B": "SAT Value (US$)",
        "input_C": "Team Profit (SAT)",
        "input_D": "Choose S Captain bonus",
        "output_F": "Team Profit (US$)",
        "output_G": "Investment Profit (US$)",
        "output_H": "Total profit of the day (US$)"
    }
}
# For nu er appen kun på ét sprog, men strukturen er klar hvis den skal udvides
texts = translations['da'] 


# --- HOVEDSIDE SETUP ---
logo_url = "https://raw.githubusercontent.com/Buggimonster/SpaceAI/591366f7037c4b66479ce01fac236b4053d01c45/logo.png"
c1, c2, c3 = st.columns([1,2,1])
with c2:
    st.image(logo_url)

st.title(texts['title'])
st.markdown("---")


# --- INPUT-FELTER ---
st.header("Indtast dine værdier")

# Input A2
todays_revenue = st.number_input(label=texts['input_A'], value=1000.0, step=100.0)

# Input B2
sat_value = st.number_input(label=texts['input_B'], value=0.01, step=0.01, format="%.2f")

# Input C2
team_profit_sat = st.number_input(label=texts['input_C'], value=5000.0, step=100.0)

# Input D2
bonus_options = [10, 15, 25, 35]
s_captain_bonus_pct = st.selectbox(
    label=texts['input_D'],
    options=bonus_options,
    format_func=lambda x: f"{x}%" # Viser % i dropdown
)

st.markdown("---")


# --- BEREGNING OG RESULTATER ---
if st.button(texts['calculate_button']):
    # Konstanter og værdier fra input
    platform_fee_pct = 0.05  # Fast 5%
    bonus_pct_decimal = s_captain_bonus_pct / 100
    
    # Formel F2 = B2 * C2
    team_profit_usd = sat_value * team_profit_sat
    
    # Formel H2 = A2 - (((A2 - F2) / (1 + D2)) * E2)
    # Håndterer division med nul, hvis 1 + bonus er nul (usandsynligt, men god praksis)
    denominator = 1 + bonus_pct_decimal
    if denominator == 0:
        st.error("Bonus Procent kan ikke være -100%.")
    else:
        total_profit_of_the_day = todays_revenue - (((todays_revenue - team_profit_usd) / denominator) * platform_fee_pct)
        
        # Formel G2 = H2 - F2
        investment_profit_usd = total_profit_of_the_day - team_profit_usd

        # Vis resultater
        st.header(texts['results_header'])
        
        # Opret kolonner for et pænt layout
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(label=texts['output_F'], value=f"${team_profit_usd:,.2f}")
        
        with col2:
            st.metric(label=texts['output_G'], value=f"${investment_profit_usd:,.2f}")
            
        with col3:
            st.metric(label=texts['output_H'], value=f"${total_profit_of_the_day:,.2f}")
