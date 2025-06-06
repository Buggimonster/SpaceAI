import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="Avanceret Rentevækst Beregner", layout="wide")
st.title("Avanceret Rentevækst Beregner")

# Input: Startbeløb i USD
initial_amount = st.number_input("Startbeløb (USD)", min_value=0.0, format="%.2f")

# Input: Antal dage
num_days = st.number_input("Antal dage", min_value=1, step=1)

# Input: Dagligt procentvis vækst (via slider)
daily_percent = st.slider("Daglig procentvis vækst", min_value=0.4, max_value=5.0, step=0.1, format="%.1f") / 100

# Input: Dagligt fast tillæg
daily_addition = st.number_input("Dagligt tillæg (USD)", min_value=0.0, format="%.2f")

# Input: Reinvester renter hver X dage
compound_interval = st.number_input(
    "Reinvestér renter hver X dage (0 = ingen reinvestering)",
    min_value=0,
    value=1,
    step=1
)

# Valgmulighed: Træk 5% fra dagligt afkast (skat/omkostning)
apply_tax = st.checkbox("Fratræk 5% af dagligt afkast", value=False)

# Valgfri: Spring specifikke dage over
skip_days_input = st.text_input("Spring disse dage over (kommasepareret, fx 5,10,15)", value="")
skip_days = set()
if skip_days_input:
    try:
        skip_days = set(int(day.strip()) for day in skip_days_input.split(",") if day.strip().isdigit())
    except ValueError:
        st.warning("Kun gyldige heltal tilladt i spring-dage feltet.")

# Beregn-knap
if st.button("Beregn"):
    results = []
    amount = initial_amount

    for day in range(1, num_days + 1):
        if day in skip_days:
            results.append({"Dag": day, "Beløb (USD)": round(amount, 2)})
            continue

        # Bestem om renter skal reinvesteres denne dag
        if compound_interval == 0:
            base_for_interest = initial_amount
        elif day % compound_interval == 0:
            base_for_interest = amount
        else:
            base_for_interest = initial_amount

        daily_interest = base_for_interest * daily_percent

        # Træk 5% fra dagligt afkast hvis valgt
        if apply_tax:
            daily_interest *= 0.95  # Fratræk 5%

        # Læg rente og dagligt tillæg til
        amount += daily_interest + daily_addition

        results.append({"Dag": day, "Beløb (USD)": round(amount, 2)})

    df = pd.DataFrame(results)
    st.subheader("Udvikling pr. dag:")
    st.dataframe(df, use_container_width=True)

    # Download-knap
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download som CSV",
        data=csv,
        file_name="avanceret_daglig_vækst.csv",
        mime="text/csv"
    )

    # Graf
    st.subheader("Graf: Beløb over tid")
    fig, ax = plt.subplots()
    ax.plot(df["Dag"], df["Beløb (USD)"], marker="o")
    ax.set_xlabel("Dag")
    ax.set_ylabel("Beløb (USD)")
    ax.grid(True)
    st.pyplot(fig)
