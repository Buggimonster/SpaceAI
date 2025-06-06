import streamlit as st
import pandas as pd

# NYT: Udvidet brugerdefineret CSS for baggrund, tekst og knapper
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

    /* --- OPDATEREDE REGLER FOR TEKSTFARVE --- */
    /* Gør al primær tekst og alle overskrifter hvide */
    .stApp, h1, h2, h3, h4, h5, h6, .st-emotion-cache-16idsys p {
        color: white;
    }

    /* Sikrer at tal-visninger (metrics) også bliver hvide */
    .stMetric [data-testid="stMetricLabel"],
    .stMetric [data-testid="stMetricValue"] {
        color: white;
    }
    
    /* --- NYE REGLER FOR KNAP --- */
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
        "total_bonus_help": "The total value of your
