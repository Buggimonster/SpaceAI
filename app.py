import streamlit as st

st.title("SpaceAI Calculator med 5% fratræk og tillæg")

# Inputfelter til tal
num1 = st.number_input("Indtast det første tal", format="%.2f")
num2 = st.number_input("Indtast det andet tal", format="%.2f")

# Valg af operation
operation = st.selectbox("Vælg operation", ("Addition", "Subtraktion", "Multiplikation", "Division"))

# Ekstra input til tillæg
adjustment = st.number_input("Tillæg (læg dette tal til resultatet efter fradrag)", value=0.0, format="%.2f")

# Beregn-knap
if st.button("Beregn"):
    result = None

    if operation == "Addition":
        result = num1 + num2
    elif operation == "Subtraktion":
        result = num1 - num2
    elif operation == "Multiplikation":
        result = num1 * num2
    elif operation == "Division":
        if num2 != 0:
            result = num1 / num2
        else:
            st.error("Fejl: Division med nul er ikke tilladt.")

    if result is not None:
        result_after_fee = result * 0.95  # Træk 5% fra
        final_result = result_after_fee + adjustment  # Læg tillæg til

        st.success(f"Resultat før fradrag: {result:.2f}")
        st.info(f"Resultat efter 5% fradrag: {result_after_fee:.2f}")
        st.warning(f"Slutresultat efter tillæg: {final_result:.2f}")
