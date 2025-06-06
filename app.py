
import streamlit as st
import pandas as pd

# Function to calculate investment growth
def calculate_investment(initial_capital, days, daily_return, bonus_level, reinvest):
    daily_return = daily_return / 100
    bonus = bonus_level / 100
    capital = initial_capital
    history = []

    for day in range(1, days + 1):
        profit = capital * daily_return
        if reinvest:
            capital += profit
        else:
            capital += profit * (1 + bonus)
        history.append(capital)

    return capital, history

# Streamlit app
st.title("Investment Growth Simulator")

# User inputs
initial_capital = st.number_input("Initial Capital (in USD)", min_value=0.0, value=1000.0)
days = st.number_input("Investment Duration (in days)", min_value=1, value=30)
daily_return = st.number_input("Daily Return (%)", min_value=0.0, value=1.0)
bonus_level = st.number_input("Bonus Level (%)", min_value=0.0, value=0.0)
reinvest = st.checkbox("Reinvest Profits", value=True)

# Calculate investment growth
final_amount, history = calculate_investment(initial_capital, days, daily_return, bonus_level, reinvest)

# Display results
st.subheader("Results")
st.write(f"Final Amount: ${final_amount:.2f}")

# Display investment growth chart
st.subheader("Investment Growth Over Time")
df = pd.DataFrame(history, columns=["Capital"])
st.line_chart(df)
