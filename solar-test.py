import streamlit as st
import numpy as np
import pandas as pd

st.set_page_config(layout="wide")
st.title("☀️ Photovoltaic Thermal Testing Simulator")
st.write("Analyze how a solar cell's temperature decay profile directly impacts its electrical efficiency.")

# --- SIDEBAR CONTROLS ---
st.sidebar.header("Lab Test Parameters")
T_a = st.sidebar.slider("Ambient Lab Temperature (Ta) [°C]", 15.0, 45.0, 30.0)
T_0 = st.sidebar.slider("Initial Heated Cell Temp (T0) [°C]", 50.0, 90.0, 75.0)
k = st.sidebar.slider("Material Cooling Constant (k) [min⁻¹]", 0.05, 0.50, 0.12)

# --- TIMELINE GENERATION ---
t_values = np.linspace(0, 30, 300)
# The core Newton's Law of Cooling ODE solution solved by students
T_values = T_a + (T_0 - T_a) * np.exp(-k * t_values)
# Embedded solar cell performance math
eff_values = 22.0 * (1 - 0.004 * (T_values - 25.0))

# --- PLOTTING DATA ---
col1, col2 = st.columns(2)
with col1:
    st.subheader("Analytical Model: Cell Temperature (°C)")
    st.line_chart(pd.DataFrame({"Time (mins)": t_values, "Temp (°C)": T_values}).set_index("Time (mins)"), color="#ff4b4b")

with col2:
    st.subheader("Coupled Impact: Cell Efficiency (%)")
    st.line_chart(pd.DataFrame({"Time (mins)": t_values, "Efficiency (%)": eff_values}).set_index("Time (mins)"), color="#00cc66")

# --- VERIFICATION PANEL ---
st.markdown("---")
st.subheader("🔍 Engineering Verification Tool")
t_check = st.slider("Select Test Time (t) to check your tutorial answer:", 0.0, 30.0, 5.0, step=1.0)

# Extract specific timeline points
T_t = T_a + (T_0 - T_a) * np.exp(-k * t_check)
eff_t = 22.0 * (1 - 0.004 * (T_t - 25.0))

c1, c2 = st.columns(2)
c1.metric(label=f"Predicted Cell Temperature at t = {t_check} mins", value=f"{T_t:.2f} °C")
c2.metric(label=f"Resulting Photovoltaic Efficiency", value=f"{eff_t:.2f} %")
