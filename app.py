import streamlit as st
import pandas as pd

st.title("Daglig Rentevækst Beregner")

# Input: Startbeløb i USD
initial_amount = st.number_input("Startbeløb (USD)", min_value=0.0, format="%.2f")

# Input: Antal dage
num_days = st.number_input("Antal dage", min_value=1, step=1)

# Input: Procent som daglig vækst (via slider)
daily_percent = st.slider("Daglig procentvis vækst", min_value=0.4, max_value=5.0, step=0.1, format="%.1f") / 100

# Beregn-knap
if st.button("Beregn"):
    results = []
    amount = initial_amount

    for day in range(1, num_days + 1):
        amount += amount * daily_percent
        results.append({"Dag": day, "Beløb (USD)": round(amount, 2)})

    df = pd.DataFrame(results)
    st.subheader("Udvikling pr. dag:")
    st.dataframe(df, use_container_width=True)

    # Download-knap
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="Download som CSV",
        data=csv,
        file_name="daglig_vækst.csv",
        mime="text/csv"
    )
