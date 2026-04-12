import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# External modules (make sure these files exist)
from motor_model import induction_motor_simulation, synchronous_motor_simulation
from dc_motor import (
    calculate_efficiency as dc_calculate_efficiency,
    calculate_speed as dc_calculate_speed,
    calculate_stall_current,
    calculate_stall_torque,
    calculate_torque as dc_calculate_torque,
    simulate_step_response,
)

# PAGE CONFIG
st.set_page_config(page_title="MotorSim Pro", layout="wide")

# TITLE
st.title("⚙️ MotorSim Pro")
st.subheader("Motor Simulation Dashboard (Clean Version)")

# SIDEBAR
st.sidebar.header("🔧 Input Parameters")
analysis_domain = st.sidebar.radio("Simulation Domain", ["AC Motors", "DC Motor"])

# ---------------- DC MOTOR MODULE ----------------
def render_dc_module():
    st.header("🔋 DC Motor Analysis")

    col1, col2, col3 = st.columns(3)

    with col1:
        V = st.number_input("Voltage (V)", value=12.0)
        I = st.number_input("Current (A)", value=3.0)
        R = st.number_input("Resistance (Ω)", value=2.0)

    with col2:
        flux = st.number_input("Flux (Wb)", value=0.05)
        k = st.number_input("Motor Constant K", value=0.1)
        kt = st.number_input("Torque Constant", value=0.1)

    with col3:
        L = st.number_input("Inductance (H)", value=0.5)
        J = st.number_input("Inertia", value=0.01)
        b = st.number_input("Damping", value=0.001)

    try:
        speed = dc_calculate_speed(V, I, R, flux, k)
        torque = dc_calculate_torque(I, kt)
        efficiency = dc_calculate_efficiency(V, I, torque, speed)

        st.subheader("📊 Results")
        c1, c2, c3 = st.columns(3)
        c1.metric("Speed (RPM)", f"{speed:.2f}")
        c2.metric("Torque (Nm)", f"{torque:.2f}")
        c3.metric("Efficiency (%)", f"{efficiency:.2f}")

        # Step response
        t, rpm = simulate_step_response(R, L, k, J, b, V, 2.0)
        fig, ax = plt.subplots()
        ax.plot(t, rpm)
        ax.set_title("Step Response")
        ax.set_xlabel("Time")
        ax.set_ylabel("Speed")
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error: {e}")


if analysis_domain == "DC Motor":
    render_dc_module()
    st.stop()

# ---------------- AC MOTOR MODULE ----------------
motor_type = st.sidebar.selectbox("Motor Type", ["Induction Motor", "Synchronous Motor"])

voltage = st.sidebar.slider("Voltage", 100, 500, 415)
frequency = st.sidebar.slider("Frequency", 25, 100, 50)
poles = st.sidebar.selectbox("Poles", [2, 4, 6, 8])
load = st.sidebar.slider("Load Torque", 1, 100, 20)
rheostat = st.sidebar.slider("Rheostat", 0.0, 5.0, 0.5)

if motor_type == "Induction Motor":
    slip = st.sidebar.slider("Slip", 0.01, 0.2, 0.04)
    result = induction_motor_simulation(voltage, frequency, poles, slip, load, rheostat)
else:
    excitation = st.sidebar.slider("Excitation", 0.8, 1.2, 1.0)
    result = synchronous_motor_simulation(voltage, frequency, poles, load, excitation, rheostat)

# ---------------- OUTPUT ----------------
st.subheader("📊 Motor Results")

c1, c2, c3, c4 = st.columns(4)
c1.metric("Speed", result["Speed (RPM)"])
c2.metric("Current", result["Current (A)"])
c3.metric("Torque", result["Torque (Nm)"])
c4.metric("Efficiency", result["Efficiency (%)"])

# Table
df = pd.DataFrame(result.items(), columns=["Parameter", "Value"])
st.dataframe(df)

# ---------------- GRAPH ----------------
st.subheader("📈 Torque vs Speed")

speeds = np.linspace(500, 3000, 50)
torques = []

for s in speeds:
    if motor_type == "Induction Motor":
        r = induction_motor_simulation(voltage, frequency, poles, 0.04, load, rheostat)
    else:
        r = synchronous_motor_simulation(voltage, frequency, poles, load, 1.0, rheostat)
    torques.append(r["Torque (Nm)"])

fig, ax = plt.subplots()
ax.plot(speeds, torques)
ax.set_xlabel("Speed")
ax.set_ylabel("Torque")
st.pyplot(fig)

# ---------------- EXPORT ----------------
csv = df.to_csv(index=False).encode("utf-8")
st.download_button("Download CSV", csv, "motor_results.csv")

