import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from motor_model import induction_motor_simulation, synchronous_motor_simulation

# PAGE CONFIG
st.set_page_config(page_title="MotorSim Pro", layout="wide")

# CUSTOM STYLING
st.markdown("""
<style>
/* Main app background */
.stApp {
    background: linear-gradient(135deg, #0b1220 0%, #111827 45%, #0f172a 100%);
    color: #f3f4f6;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827 0%, #1f2937 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Main text */
html, body, [class*="css"] {
    color: #f3f4f6;
    font-family: "Segoe UI", sans-serif;
}

/* Cards */
.metric-card {
    background: rgba(255, 255, 255, 0.05);
    padding: 18px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
    text-align: center;
    margin-bottom: 12px;
}

.metric-title {
    font-size: 14px;
    color: #cbd5e1;
    margin-bottom: 6px;
}

.metric-value {
    font-size: 32px;
    font-weight: 700;
    color: #ffffff;
}

/* Section headers */
.section-box {
    background: rgba(255, 255, 255, 0.04);
    padding: 16px 20px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 18px;
}

/* Recommendation panel */
.recommend-box {
    background: linear-gradient(135deg, rgba(34,197,94,0.12), rgba(59,130,246,0.12));
    padding: 18px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-top: 10px;
}

/* Fault box */
.fault-box {
    background: linear-gradient(135deg, rgba(239,68,68,0.14), rgba(245,158,11,0.12));
    padding: 18px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-top: 10px;
}

/* Brand box */
.brand-box {
    background: linear-gradient(135deg, rgba(99,102,241,0.14), rgba(14,165,233,0.12));
    padding: 18px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 18px;
}

/* Tabs */
button[data-baseweb="tab"] {
    font-size: 15px;
    font-weight: 600;
    color: #e5e7eb;
}

/* Hide Streamlit footer/menu */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Rotor Animation */
.rotor-wrap {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 10px;
    margin-bottom: 10px;
}

.rotor {
    width: 180px;
    height: 180px;
    border-radius: 50%;
    border: 10px solid rgba(255,255,255,0.12);
    border-top: 10px solid #38bdf8;
    border-right: 10px solid #22c55e;
    border-bottom: 10px solid #f59e0b;
    position: relative;
    animation: spin 2s linear infinite;
    box-shadow: 0 0 30px rgba(56,189,248,0.15);
}

.rotor::before {
    content: "";
    position: absolute;
    top: 50%;
    left: 50%;
    width: 70px;
    height: 70px;
    background: rgba(255,255,255,0.08);
    border: 2px solid rgba(255,255,255,0.12);
    border-radius: 50%;
    transform: translate(-50%, -50%);
}

.rotor::after {
    content: "";
    position: absolute;
    top: 8px;
    left: 50%;
    width: 8px;
    height: 40px;
    background: #ffffff;
    border-radius: 8px;
    transform: translateX(-50%);
}

@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
</style>
""", unsafe_allow_html=True)

# TITLE
st.title("⚙️ MotorSim Pro")
st.subheader("Advanced Simulation and Performance Analysis of Synchronous and Induction Motors")

st.markdown("""
<div class="brand-box">
<h3 style="margin-top:0;">🏭 Industrial Digital Twin Dashboard</h3>
<p style="margin-bottom:0;">
Designed as a <b>third-party industrial motor analysis platform</b> for electrical labs, automation companies, and equipment testing environments.
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="section-box">
<b>Industrial Use Case:</b> This software is designed for <b>electrical industries, testing labs, motor manufacturers, and industrial automation firms</b>
to simulate, compare, and analyze the behavior of <b>Induction Motors</b> and <b>Synchronous Motors</b> under varying operating conditions.
</div>
""", unsafe_allow_html=True)

# SIDEBAR INPUTS
st.sidebar.header("🔧 Input Parameters")

mode = st.sidebar.radio("Select Mode", ["Single Motor Analysis", "Comparison Mode"])

motor_type = st.sidebar.selectbox(
    "Select Motor Type",
    ["Induction Motor", "Synchronous Motor"]
)

voltage = st.sidebar.slider("Applied Voltage (V)", 100, 500, 415)
frequency = st.sidebar.slider("Supply Frequency (Hz)", 25, 100, 50)
poles = st.sidebar.selectbox("Number of Poles", [2, 4, 6, 8], index=1)
load_torque = st.sidebar.slider("Load Torque (Nm)", 1, 100, 20)
rheostat_resistance = st.sidebar.slider("Rheostat Resistance (Ohm)", 0.0, 5.0, 0.5)

if motor_type == "Induction Motor":
    slip = st.sidebar.slider("Slip", 0.01, 0.20, 0.04, step=0.01)
else:
    excitation_factor = st.sidebar.slider("Excitation Factor", 0.8, 1.2, 1.0, step=0.05)

# Fault Simulation
st.sidebar.markdown("### ⚠ Fault Simulation")
fault_mode = st.sidebar.selectbox(
    "Fault Scenario",
    ["Normal", "Voltage Drop", "Overload", "Over Frequency", "High Rheostat"]
)

# Apply fault conditions
fault_voltage = voltage
fault_load = load_torque
fault_frequency = frequency
fault_rheostat = rheostat_resistance

if fault_mode == "Voltage Drop":
    fault_voltage = max(100, voltage - 120)
elif fault_mode == "Overload":
    fault_load = min(100, load_torque + 30)
elif fault_mode == "Over Frequency":
    fault_frequency = min(100, frequency + 20)
elif fault_mode == "High Rheostat":
    fault_rheostat = min(5.0, rheostat_resistance + 2.5)


# MOTOR RESULTS

if motor_type == "Induction Motor":
    result = induction_motor_simulation(fault_voltage, fault_frequency, poles, slip, fault_load, fault_rheostat)
else:
    result = synchronous_motor_simulation(fault_voltage, fault_frequency, poles, fault_load, excitation_factor, fault_rheostat)


# HELPERS

def recommendation_engine(result):
    recs = []

    if result["Efficiency (%)"] < 60:
        recs.append("Increase efficiency by reducing load fluctuations or improving supply conditions.")
    if result["Current (A)"] > 25:
        recs.append("Current is relatively high — consider reducing torque demand or rheostat resistance.")
    if result["Power Factor"] < 0.75:
        recs.append("Power factor is low — compensation or improved excitation may help.")
    if result["Torque (Nm)"] < 5:
        recs.append("Developed torque is low — check rheostat setting or increase applied voltage.")
    if result["Health Status"] == "Critical":
        recs.append("Motor health is critical — immediate operating condition correction is recommended.")
    elif result["Health Status"] == "Warning":
        recs.append("Motor health is in warning zone — monitor parameters carefully.")

    if not recs:
        recs.append("Motor is operating within acceptable simulated conditions.")

    return recs

def gauge_chart(title, value, min_val, max_val, suffix=""):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={"suffix": suffix},
        title={"text": title},
        gauge={
            "axis": {"range": [min_val, max_val]},
            "bar": {"thickness": 0.25},
            "steps": [
                {"range": [min_val, min_val + (max_val-min_val)*0.5], "color": "rgba(34,197,94,0.25)"},
                {"range": [min_val + (max_val-min_val)*0.5, min_val + (max_val-min_val)*0.8], "color": "rgba(245,158,11,0.25)"},
                {"range": [min_val + (max_val-min_val)*0.8, max_val], "color": "rgba(239,68,68,0.25)"},
            ],
        }
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "#f3f4f6", "family": "Segoe UI"},
        margin=dict(l=10, r=10, t=50, b=10),
        height=260
    )
    return fig

recommendations = recommendation_engine(result)


# TAB
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard",
    "📈 Performance Graphs",
    "⚡ 3-Phase Waveforms",
    "🆚 Comparison",
    "📤 Export"
])


# TAB 1 - DASHBOARD

with tab1:
    st.markdown(f"""
    <div class="section-box">
    <h3 style="margin-bottom:6px;">📊 Simulation Dashboard</h3>
    <p style="margin:0;">Active Scenario: <b>{fault_mode}</b></p>
    </div>
    """, unsafe_allow_html=True)

    # Top metrics
    c1, c2, c3, c4, c5, c6 = st.columns(6)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Motor Type</div>
            <div class="metric-value" style="font-size:22px;">{result["Motor Type"]}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Speed</div>
            <div class="metric-value">{result["Speed (RPM)"]}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Current</div>
            <div class="metric-value">{result["Current (A)"]}</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Torque</div>
            <div class="metric-value">{result["Torque (Nm)"]}</div>
        </div>
        """, unsafe_allow_html=True)

    with c5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Efficiency</div>
            <div class="metric-value">{result["Efficiency (%)"]}</div>
        </div>
        """, unsafe_allow_html=True)

    with c6:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Power Factor</div>
            <div class="metric-value">{result["Power Factor"]}</div>
        </div>
        """, unsafe_allow_html=True)

    # Rotor animation + gauges
    left, right = st.columns([1, 2])

    with left:
        st.markdown("### 🌀 Motor Rotor Animation")
        st.markdown("""
        <div class="rotor-wrap">
            <div class="rotor"></div>
        </div>
        """, unsafe_allow_html=True)
        st.caption("Animated rotor representation for visual simulation.")

    with right:
        g1, g2, g3 = st.columns(3)
        with g1:
            st.plotly_chart(gauge_chart("RPM", result["Speed (RPM)"], 0, 3000), use_container_width=True)
        with g2:
            st.plotly_chart(gauge_chart("Current", result["Current (A)"], 0, 50, " A"), use_container_width=True)
        with g3:
            st.plotly_chart(gauge_chart("Efficiency", result["Efficiency (%)"], 0, 100, " %"), use_container_width=True)

    st.markdown("### 📋 Detailed Output Table")
    df_result = pd.DataFrame(result.items(), columns=["Parameter", "Value"])
    st.dataframe(df_result, use_container_width=True)

    # Health + Fault + AI Recommendation
    a1, a2 = st.columns(2)

    with a1:
        health = result["Health Status"]
        if health == "Normal":
            st.success(f"🟢 Health Status: {health}")
        elif health == "Warning":
            st.warning(f"🟠 Health Status: {health}")
        else:
            st.error(f"🔴 Health Status: {health}")

        st.markdown(f"""
        <div class="fault-box">
        <h4 style="margin-top:0;">⚠ Fault Analysis</h4>
        <p><b>Scenario:</b> {fault_mode}</p>
        <p><b>Observed Impact:</b> Fault conditions may affect speed, torque, current, and efficiency.</p>
        </div>
        """, unsafe_allow_html=True)

    with a2:
        rec_html = "".join([f"<li>{r}</li>" for r in recommendations])
        st.markdown(f"""
        <div class="recommend-box">
        <h4 style="margin-top:0;">🤖 Smart Recommendation Engine</h4>
        <ul>{rec_html}</ul>
        </div>
        """, unsafe_allow_html=True)


# TAB 2 - GRAPHS

with tab2:
    st.markdown("## 📈 Performance Graphs")

    # Graph 1
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    if motor_type == "Induction Motor":
        slips = np.linspace(0.01, 0.20, 50)
        speeds = []
        torques = []
        for s in slips:
            r = induction_motor_simulation(fault_voltage, fault_frequency, poles, s, fault_load, fault_rheostat)
            speeds.append(r["Speed (RPM)"])
            torques.append(r["Torque (Nm)"])
        ax1.plot(speeds, torques, linewidth=2)
        ax1.set_title("Torque vs Speed (Induction Motor)")
        ax1.set_xlabel("Speed (RPM)")
        ax1.set_ylabel("Torque (Nm)")
    else:
        torques = np.linspace(1, 100, 50)
        currents = []
        for t in torques:
            r = synchronous_motor_simulation(fault_voltage, fault_frequency, poles, t, excitation_factor, fault_rheostat)
            currents.append(r["Current (A)"])
        ax1.plot(torques, currents, linewidth=2)
        ax1.set_title("Current vs Load Torque (Synchronous Motor)")
        ax1.set_xlabel("Load Torque (Nm)")
        ax1.set_ylabel("Current (A)")
    ax1.grid(True)
    st.pyplot(fig1)

    # Graph 2
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    frequencies = np.linspace(25, 100, 50)
    speeds_freq = []
    for f in frequencies:
        if motor_type == "Induction Motor":
            r = induction_motor_simulation(fault_voltage, f, poles, slip, fault_load, fault_rheostat)
            speeds_freq.append(r["Speed (RPM)"])
        else:
            r = synchronous_motor_simulation(fault_voltage, f, poles, fault_load, excitation_factor, fault_rheostat)
            speeds_freq.append(r["Speed (RPM)"])
    ax2.plot(frequencies, speeds_freq, linewidth=2)
    ax2.set_title("Speed vs Frequency")
    ax2.set_xlabel("Frequency (Hz)")
    ax2.set_ylabel("Speed (RPM)")
    ax2.grid(True)
    st.pyplot(fig2)

    # Graph 3
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    voltages = np.linspace(100, 500, 50)
    currents_voltage = []
    for v in voltages:
        if motor_type == "Induction Motor":
            r = induction_motor_simulation(v, fault_frequency, poles, slip, fault_load, fault_rheostat)
            currents_voltage.append(r["Current (A)"])
        else:
            r = synchronous_motor_simulation(v, fault_frequency, poles, fault_load, excitation_factor, fault_rheostat)
            currents_voltage.append(r["Current (A)"])
    ax3.plot(voltages, currents_voltage, linewidth=2)
    ax3.set_title("Current vs Voltage")
    ax3.set_xlabel("Voltage (V)")
    ax3.set_ylabel("Current (A)")
    ax3.grid(True)
    st.pyplot(fig3)

    # Graph 4
    fig4, ax4 = plt.subplots(figsize=(8, 5))
    torque_range = np.linspace(1, 100, 50)
    efficiencies = []
    for t in torque_range:
        if motor_type == "Induction Motor":
            r = induction_motor_simulation(fault_voltage, fault_frequency, poles, slip, t, fault_rheostat)
            efficiencies.append(r["Efficiency (%)"])
        else:
            r = synchronous_motor_simulation(fault_voltage, fault_frequency, poles, t, excitation_factor, fault_rheostat)
            efficiencies.append(r["Efficiency (%)"])
    ax4.plot(torque_range, efficiencies, linewidth=2)
    ax4.set_title("Efficiency vs Load Torque")
    ax4.set_xlabel("Load Torque (Nm)")
    ax4.set_ylabel("Efficiency (%)")
    ax4.grid(True)
    st.pyplot(fig4)

    # Graph 5
    fig5, ax5 = plt.subplots(figsize=(8, 5))
    rheostat_values = np.linspace(0, 5, 50)
    currents_rheo = []
    for rr in rheostat_values:
        if motor_type == "Induction Motor":
            r = induction_motor_simulation(fault_voltage, fault_frequency, poles, slip, fault_load, rr)
            currents_rheo.append(r["Current (A)"])
        else:
            r = synchronous_motor_simulation(fault_voltage, fault_frequency, poles, fault_load, excitation_factor, rr)
            currents_rheo.append(r["Current (A)"])
    ax5.plot(rheostat_values, currents_rheo, linewidth=2)
    ax5.set_title("Rheostat Resistance vs Current")
    ax5.set_xlabel("Rheostat Resistance (Ohm)")
    ax5.set_ylabel("Current (A)")
    ax5.grid(True)
    st.pyplot(fig5)

    # Graph 6
    fig6, ax6 = plt.subplots(figsize=(8, 5))
    torques_rheo = []
    for rr in rheostat_values:
        if motor_type == "Induction Motor":
            r = induction_motor_simulation(fault_voltage, fault_frequency, poles, slip, fault_load, rr)
            torques_rheo.append(r["Torque (Nm)"])
        else:
            r = synchronous_motor_simulation(fault_voltage, fault_frequency, poles, fault_load, excitation_factor, rr)
            torques_rheo.append(r["Torque (Nm)"])
    ax6.plot(rheostat_values, torques_rheo, linewidth=2)
    ax6.set_title("Rheostat Resistance vs Torque")
    ax6.set_xlabel("Rheostat Resistance (Ohm)")
    ax6.set_ylabel("Torque (Nm)")
    ax6.grid(True)
    st.pyplot(fig6)


# TAB 3 - 3 PHASE WAVEFORMS

with tab3:
    st.markdown("## ⚡ 3-Phase Waveforms")

    t = np.linspace(0, 0.04, 1000)
    Vm = fault_voltage / np.sqrt(3)

    phase_a = Vm * np.sin(2 * np.pi * fault_frequency * t)
    phase_b = Vm * np.sin(2 * np.pi * fault_frequency * t - 2*np.pi/3)
    phase_c = Vm * np.sin(2 * np.pi * fault_frequency * t + 2*np.pi/3)

    figw, axw = plt.subplots(figsize=(10, 5))
    axw.plot(t, phase_a, label="Phase A")
    axw.plot(t, phase_b, label="Phase B")
    axw.plot(t, phase_c, label="Phase C")
    axw.set_title("3-Phase Voltage Waveforms")
    axw.set_xlabel("Time (s)")
    axw.set_ylabel("Voltage (V)")
    axw.grid(True)
    axw.legend()
    st.pyplot(figw)


# TAB 4 - COMPARISON

with tab4:
    st.markdown("## 🆚 Motor Comparison")

    ind_result = induction_motor_simulation(fault_voltage, fault_frequency, poles, 0.04, fault_load, fault_rheostat)
    syn_result = synchronous_motor_simulation(fault_voltage, fault_frequency, poles, fault_load, 1.0, fault_rheostat)

    comp_df = pd.DataFrame({
        "Parameter": ["Speed (RPM)", "Current (A)", "Torque (Nm)", "Efficiency (%)", "Power Factor", "Input Power (kW)", "Output Power (kW)", "Health Status"],
        "Induction Motor": [
            ind_result["Speed (RPM)"],
            ind_result["Current (A)"],
            ind_result["Torque (Nm)"],
            ind_result["Efficiency (%)"],
            ind_result["Power Factor"],
            ind_result["Input Power (kW)"],
            ind_result["Output Power (kW)"],
            ind_result["Health Status"]
        ],
        "Synchronous Motor": [
            syn_result["Speed (RPM)"],
            syn_result["Current (A)"],
            syn_result["Torque (Nm)"],
            syn_result["Efficiency (%)"],
            syn_result["Power Factor"],
            syn_result["Input Power (kW)"],
            syn_result["Output Power (kW)"],
            syn_result["Health Status"]
        ]
    })

    st.dataframe(comp_df, use_container_width=True)


# TAB 5 - EXPORT

with tab5:
    st.markdown("## 📤 Export Results")

    export_df = pd.DataFrame(result.items(), columns=["Parameter", "Value"])
    csv = export_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Current Results as CSV",
        data=csv,
        file_name="motorsim_results.csv",
        mime="text/csv"
    )


import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.graph_objects as go

from motor_model import induction_motor_simulation, synchronous_motor_simulation


# PAGE CONFIG

st.set_page_config(page_title="MotorSim Pro", layout="wide")


# CUSTOM STYLING

st.markdown("""
<style>
/* Main app background */
.stApp {
    background: linear-gradient(135deg, #0b1220 0%, #111827 45%, #0f172a 100%);
    color: #f3f4f6;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #111827 0%, #1f2937 100%);
    border-right: 1px solid rgba(255,255,255,0.08);
}

/* Main text */
html, body, [class*="css"] {
    color: #f3f4f6;
    font-family: "Segoe UI", sans-serif;
}

/* Cards */
.metric-card {
    background: rgba(255, 255, 255, 0.05);
    padding: 18px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.08);
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
    text-align: center;
    margin-bottom: 12px;
}

.metric-title {
    font-size: 14px;
    color: #cbd5e1;
    margin-bottom: 6px;
}

.metric-value {
    font-size: 32px;
    font-weight: 700;
    color: #ffffff;
}

/* Section headers */
.section-box {
    background: rgba(255, 255, 255, 0.04);
    padding: 16px 20px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 18px;
}

/* Recommendation panel */
.recommend-box {
    background: linear-gradient(135deg, rgba(34,197,94,0.12), rgba(59,130,246,0.12));
    padding: 18px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-top: 10px;
}

/* Fault box */
.fault-box {
    background: linear-gradient(135deg, rgba(239,68,68,0.14), rgba(245,158,11,0.12));
    padding: 18px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-top: 10px;
}

/* Brand box */
.brand-box {
    background: linear-gradient(135deg, rgba(99,102,241,0.14), rgba(14,165,233,0.12));
    padding: 18px;
    border-radius: 18px;
    border: 1px solid rgba(255,255,255,0.08);
    margin-bottom: 18px;
}

/* Tabs */
button[data-baseweb="tab"] {
    font-size: 15px;
    font-weight: 600;
    color: #e5e7eb;
}

/* Hide Streamlit footer/menu */
#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

/* Rotor Animation */
.rotor-wrap {
    display: flex;
    justify-content: center;
    align-items: center;
    margin-top: 10px;
    margin-bottom: 10px;
}

.rotor {
    width: 180px;
    height: 180px;
    border-radius: 50%;
    border: 10px solid rgba(255,255,255,0.12);
    border-top: 10px solid #38bdf8;
    border-right: 10px solid #22c55e;
    border-bottom: 10px solid #f59e0b;
    position: relative;
    animation: spin 2s linear infinite;
    box-shadow: 0 0 30px rgba(56,189,248,0.15);
}

.rotor::before {
    content: "";
    position: absolute;
    top: 50%;
    left: 50%;
    width: 70px;
    height: 70px;
    background: rgba(255,255,255,0.08);
    border: 2px solid rgba(255,255,255,0.12);
    border-radius: 50%;
    transform: translate(-50%, -50%);
}

.rotor::after {
    content: "";
    position: absolute;
    top: 8px;
    left: 50%;
    width: 8px;
    height: 40px;
    background: #ffffff;
    border-radius: 8px;
    transform: translateX(-50%);
}

@keyframes spin {
    from { transform: rotate(0deg); }
    to { transform: rotate(360deg); }
}
</style>
""", unsafe_allow_html=True)


# TITLE

st.title("⚙️ MotorSim Pro")
st.subheader("Advanced Simulation and Performance Analysis of Synchronous and Induction Motors")

st.markdown("""
<div class="brand-box">
<h3 style="margin-top:0;">🏭 Industrial Digital Twin Dashboard</h3>
<p style="margin-bottom:0;">
Designed as a <b>third-party industrial motor analysis platform</b> for electrical labs, automation companies, and equipment testing environments.
</p>
</div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="section-box">
<b>Industrial Use Case:</b> This software is designed for <b>electrical industries, testing labs, motor manufacturers, and industrial automation firms</b>
to simulate, compare, and analyze the behavior of <b>Induction Motors</b> and <b>Synchronous Motors</b> under varying operating conditions.
</div>
""", unsafe_allow_html=True)


# SIDEBAR INPUTS

st.sidebar.header("🔧 Input Parameters")

mode = st.sidebar.radio("Select Mode", ["Single Motor Analysis", "Comparison Mode"])

motor_type = st.sidebar.selectbox(
    "Select Motor Type",
    ["Induction Motor", "Synchronous Motor"]
)

voltage = st.sidebar.slider("Applied Voltage (V)", 100, 500, 415)
frequency = st.sidebar.slider("Supply Frequency (Hz)", 25, 100, 50)
poles = st.sidebar.selectbox("Number of Poles", [2, 4, 6, 8], index=1)
load_torque = st.sidebar.slider("Load Torque (Nm)", 1, 100, 20)
rheostat_resistance = st.sidebar.slider("Rheostat Resistance (Ohm)", 0.0, 5.0, 0.5)

if motor_type == "Induction Motor":
    slip = st.sidebar.slider("Slip", 0.01, 0.20, 0.04, step=0.01)
else:
    excitation_factor = st.sidebar.slider("Excitation Factor", 0.8, 1.2, 1.0, step=0.05)

# Fault Simulation
st.sidebar.markdown("### ⚠ Fault Simulation")
fault_mode = st.sidebar.selectbox(
    "Fault Scenario",
    ["Normal", "Voltage Drop", "Overload", "Over Frequency", "High Rheostat"]
)

# Apply fault conditions
fault_voltage = voltage
fault_load = load_torque
fault_frequency = frequency
fault_rheostat = rheostat_resistance

if fault_mode == "Voltage Drop":
    fault_voltage = max(100, voltage - 120)
elif fault_mode == "Overload":
    fault_load = min(100, load_torque + 30)
elif fault_mode == "Over Frequency":
    fault_frequency = min(100, frequency + 20)
elif fault_mode == "High Rheostat":
    fault_rheostat = min(5.0, rheostat_resistance + 2.5)


# MOTOR RESULTS

if motor_type == "Induction Motor":
    result = induction_motor_simulation(fault_voltage, fault_frequency, poles, slip, fault_load, fault_rheostat)
else:
    result = synchronous_motor_simulation(fault_voltage, fault_frequency, poles, fault_load, excitation_factor, fault_rheostat)


# HELPERS

def recommendation_engine(result):
    recs = []

    if result["Efficiency (%)"] < 60:
        recs.append("Increase efficiency by reducing load fluctuations or improving supply conditions.")
    if result["Current (A)"] > 25:
        recs.append("Current is relatively high — consider reducing torque demand or rheostat resistance.")
    if result["Power Factor"] < 0.75:
        recs.append("Power factor is low — compensation or improved excitation may help.")
    if result["Torque (Nm)"] < 5:
        recs.append("Developed torque is low — check rheostat setting or increase applied voltage.")
    if result["Health Status"] == "Critical":
        recs.append("Motor health is critical — immediate operating condition correction is recommended.")
    elif result["Health Status"] == "Warning":
        recs.append("Motor health is in warning zone — monitor parameters carefully.")

    if not recs:
        recs.append("Motor is operating within acceptable simulated conditions.")

    return recs

def gauge_chart(title, value, min_val, max_val, suffix=""):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        number={"suffix": suffix},
        title={"text": title},
        gauge={
            "axis": {"range": [min_val, max_val]},
            "bar": {"thickness": 0.25},
            "steps": [
                {"range": [min_val, min_val + (max_val-min_val)*0.5], "color": "rgba(34,197,94,0.25)"},
                {"range": [min_val + (max_val-min_val)*0.5, min_val + (max_val-min_val)*0.8], "color": "rgba(245,158,11,0.25)"},
                {"range": [min_val + (max_val-min_val)*0.8, max_val], "color": "rgba(239,68,68,0.25)"},
            ],
        }
    ))
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": "#f3f4f6", "family": "Segoe UI"},
        margin=dict(l=10, r=10, t=50, b=10),
        height=260
    )
    return fig

recommendations = recommendation_engine(result)


# TABS

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Dashboard",
    "📈 Performance Graphs",
    "⚡ 3-Phase Waveforms",
    "🆚 Comparison",
    "📤 Export"
])


# TAB 1 - DASHBOARD

with tab1:
    st.markdown(f"""
    <div class="section-box">
    <h3 style="margin-bottom:6px;">📊 Simulation Dashboard</h3>
    <p style="margin:0;">Active Scenario: <b>{fault_mode}</b></p>
    </div>
    """, unsafe_allow_html=True)

    # Top metrics
    c1, c2, c3, c4, c5, c6 = st.columns(6)

    with c1:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Motor Type</div>
            <div class="metric-value" style="font-size:22px;">{result["Motor Type"]}</div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Speed</div>
            <div class="metric-value">{result["Speed (RPM)"]}</div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Current</div>
            <div class="metric-value">{result["Current (A)"]}</div>
        </div>
        """, unsafe_allow_html=True)

    with c4:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Torque</div>
            <div class="metric-value">{result["Torque (Nm)"]}</div>
        </div>
        """, unsafe_allow_html=True)

    with c5:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Efficiency</div>
            <div class="metric-value">{result["Efficiency (%)"]}</div>
        </div>
        """, unsafe_allow_html=True)

    with c6:
        st.markdown(f"""
        <div class="metric-card">
            <div class="metric-title">Power Factor</div>
            <div class="metric-value">{result["Power Factor"]}</div>
        </div>
        """, unsafe_allow_html=True)

    # Rotor animation + gauges
    left, right = st.columns([1, 2])

    with left:
        st.markdown("### 🌀 Motor Rotor Animation")
        st.markdown("""
        <div class="rotor-wrap">
            <div class="rotor"></div>
        </div>
        """, unsafe_allow_html=True)
        st.caption("Animated rotor representation for visual simulation.")

    with right:
        g1, g2, g3 = st.columns(3)
        with g1:
            st.plotly_chart(gauge_chart("RPM", result["Speed (RPM)"], 0, 3000), use_container_width=True)
        with g2:
            st.plotly_chart(gauge_chart("Current", result["Current (A)"], 0, 50, " A"), use_container_width=True)
        with g3:
            st.plotly_chart(gauge_chart("Efficiency", result["Efficiency (%)"], 0, 100, " %"), use_container_width=True)

    st.markdown("### 📋 Detailed Output Table")
    df_result = pd.DataFrame(result.items(), columns=["Parameter", "Value"])
    st.dataframe(df_result, use_container_width=True)

    # Health + Fault + AI Recommendation
    a1, a2 = st.columns(2)

    with a1:
        health = result["Health Status"]
        if health == "Normal":
            st.success(f"🟢 Health Status: {health}")
        elif health == "Warning":
            st.warning(f"🟠 Health Status: {health}")
        else:
            st.error(f"🔴 Health Status: {health}")

        st.markdown(f"""
        <div class="fault-box">
        <h4 style="margin-top:0;">⚠ Fault Analysis</h4>
        <p><b>Scenario:</b> {fault_mode}</p>
        <p><b>Observed Impact:</b> Fault conditions may affect speed, torque, current, and efficiency.</p>
        </div>
        """, unsafe_allow_html=True)

    with a2:
        rec_html = "".join([f"<li>{r}</li>" for r in recommendations])
        st.markdown(f"""
        <div class="recommend-box">
        <h4 style="margin-top:0;">🤖 Smart Recommendation Engine</h4>
        <ul>{rec_html}</ul>
        </div>
        """, unsafe_allow_html=True)


# TAB 2 - GRAPHS

with tab2:
    st.markdown("## 📈 Performance Graphs")

    # Graph 1
    fig1, ax1 = plt.subplots(figsize=(8, 5))
    if motor_type == "Induction Motor":
        slips = np.linspace(0.01, 0.20, 50)
        speeds = []
        torques = []
        for s in slips:
            r = induction_motor_simulation(fault_voltage, fault_frequency, poles, s, fault_load, fault_rheostat)
            speeds.append(r["Speed (RPM)"])
            torques.append(r["Torque (Nm)"])
        ax1.plot(speeds, torques, linewidth=2)
        ax1.set_title("Torque vs Speed (Induction Motor)")
        ax1.set_xlabel("Speed (RPM)")
        ax1.set_ylabel("Torque (Nm)")
    else:
        torques = np.linspace(1, 100, 50)
        currents = []
        for t in torques:
            r = synchronous_motor_simulation(fault_voltage, fault_frequency, poles, t, excitation_factor, fault_rheostat)
            currents.append(r["Current (A)"])
        ax1.plot(torques, currents, linewidth=2)
        ax1.set_title("Current vs Load Torque (Synchronous Motor)")
        ax1.set_xlabel("Load Torque (Nm)")
        ax1.set_ylabel("Current (A)")
    ax1.grid(True)
    st.pyplot(fig1)

    # Graph 2
    fig2, ax2 = plt.subplots(figsize=(8, 5))
    frequencies = np.linspace(25, 100, 50)
    speeds_freq = []
    for f in frequencies:
        if motor_type == "Induction Motor":
            r = induction_motor_simulation(fault_voltage, f, poles, slip, fault_load, fault_rheostat)
            speeds_freq.append(r["Speed (RPM)"])
        else:
            r = synchronous_motor_simulation(fault_voltage, f, poles, fault_load, excitation_factor, fault_rheostat)
            speeds_freq.append(r["Speed (RPM)"])
    ax2.plot(frequencies, speeds_freq, linewidth=2)
    ax2.set_title("Speed vs Frequency")
    ax2.set_xlabel("Frequency (Hz)")
    ax2.set_ylabel("Speed (RPM)")
    ax2.grid(True)
    st.pyplot(fig2)

    # Graph 3
    fig3, ax3 = plt.subplots(figsize=(8, 5))
    voltages = np.linspace(100, 500, 50)
    currents_voltage = []
    for v in voltages:
        if motor_type == "Induction Motor":
            r = induction_motor_simulation(v, fault_frequency, poles, slip, fault_load, fault_rheostat)
            currents_voltage.append(r["Current (A)"])
        else:
            r = synchronous_motor_simulation(v, fault_frequency, poles, fault_load, excitation_factor, fault_rheostat)
            currents_voltage.append(r["Current (A)"])
    ax3.plot(voltages, currents_voltage, linewidth=2)
    ax3.set_title("Current vs Voltage")
    ax3.set_xlabel("Voltage (V)")
    ax3.set_ylabel("Current (A)")
    ax3.grid(True)
    st.pyplot(fig3)

    # Graph 4
    fig4, ax4 = plt.subplots(figsize=(8, 5))
    torque_range = np.linspace(1, 100, 50)
    efficiencies = []
    for t in torque_range:
        if motor_type == "Induction Motor":
            r = induction_motor_simulation(fault_voltage, fault_frequency, poles, slip, t, fault_rheostat)
            efficiencies.append(r["Efficiency (%)"])
        else:
            r = synchronous_motor_simulation(fault_voltage, fault_frequency, poles, t, excitation_factor, fault_rheostat)
            efficiencies.append(r["Efficiency (%)"])
    ax4.plot(torque_range, efficiencies, linewidth=2)
    ax4.set_title("Efficiency vs Load Torque")
    ax4.set_xlabel("Load Torque (Nm)")
    ax4.set_ylabel("Efficiency (%)")
    ax4.grid(True)
    st.pyplot(fig4)

    # Graph 5
    fig5, ax5 = plt.subplots(figsize=(8, 5))
    rheostat_values = np.linspace(0, 5, 50)
    currents_rheo = []
    for rr in rheostat_values:
        if motor_type == "Induction Motor":
            r = induction_motor_simulation(fault_voltage, fault_frequency, poles, slip, fault_load, rr)
            currents_rheo.append(r["Current (A)"])
        else:
            r = synchronous_motor_simulation(fault_voltage, fault_frequency, poles, fault_load, excitation_factor, rr)
            currents_rheo.append(r["Current (A)"])
    ax5.plot(rheostat_values, currents_rheo, linewidth=2)
    ax5.set_title("Rheostat Resistance vs Current")
    ax5.set_xlabel("Rheostat Resistance (Ohm)")
    ax5.set_ylabel("Current (A)")
    ax5.grid(True)
    st.pyplot(fig5)

    # Graph 6
    fig6, ax6 = plt.subplots(figsize=(8, 5))
    torques_rheo = []
    for rr in rheostat_values:
        if motor_type == "Induction Motor":
            r = induction_motor_simulation(fault_voltage, fault_frequency, poles, slip, fault_load, rr)
            torques_rheo.append(r["Torque (Nm)"])
        else:
            r = synchronous_motor_simulation(fault_voltage, fault_frequency, poles, fault_load, excitation_factor, rr)
            torques_rheo.append(r["Torque (Nm)"])
    ax6.plot(rheostat_values, torques_rheo, linewidth=2)
    ax6.set_title("Rheostat Resistance vs Torque")
    ax6.set_xlabel("Rheostat Resistance (Ohm)")
    ax6.set_ylabel("Torque (Nm)")
    ax6.grid(True)
    st.pyplot(fig6)


# TAB 3 - 3 PHASE WAVEFORMS

with tab3:
    st.markdown("## ⚡ 3-Phase Waveforms")

    t = np.linspace(0, 0.04, 1000)
    Vm = fault_voltage / np.sqrt(3)

    phase_a = Vm * np.sin(2 * np.pi * fault_frequency * t)
    phase_b = Vm * np.sin(2 * np.pi * fault_frequency * t - 2*np.pi/3)
    phase_c = Vm * np.sin(2 * np.pi * fault_frequency * t + 2*np.pi/3)

    figw, axw = plt.subplots(figsize=(10, 5))
    axw.plot(t, phase_a, label="Phase A")
    axw.plot(t, phase_b, label="Phase B")
    axw.plot(t, phase_c, label="Phase C")
    axw.set_title("3-Phase Voltage Waveforms")
    axw.set_xlabel("Time (s)")
    axw.set_ylabel("Voltage (V)")
    axw.grid(True)
    axw.legend()
    st.pyplot(figw)


# TAB 4 - COMPARISON

with tab4:
    st.markdown("## 🆚 Motor Comparison")

    ind_result = induction_motor_simulation(fault_voltage, fault_frequency, poles, 0.04, fault_load, fault_rheostat)
    syn_result = synchronous_motor_simulation(fault_voltage, fault_frequency, poles, fault_load, 1.0, fault_rheostat)

    comp_df = pd.DataFrame({
        "Parameter": ["Speed (RPM)", "Current (A)", "Torque (Nm)", "Efficiency (%)", "Power Factor", "Input Power (kW)", "Output Power (kW)", "Health Status"],
        "Induction Motor": [
            ind_result["Speed (RPM)"],
            ind_result["Current (A)"],
            ind_result["Torque (Nm)"],
            ind_result["Efficiency (%)"],
            ind_result["Power Factor"],
            ind_result["Input Power (kW)"],
            ind_result["Output Power (kW)"],
            ind_result["Health Status"]
        ],
        "Synchronous Motor": [
            syn_result["Speed (RPM)"],
            syn_result["Current (A)"],
            syn_result["Torque (Nm)"],
            syn_result["Efficiency (%)"],
            syn_result["Power Factor"],
            syn_result["Input Power (kW)"],
            syn_result["Output Power (kW)"],
            syn_result["Health Status"]
        ]
    })

    st.dataframe(comp_df, use_container_width=True)


# TAB 5 - EXPORT

with tab5:
    st.markdown("## 📤 Export Results")

    export_df = pd.DataFrame(result.items(), columns=["Parameter", "Value"])
    csv = export_df.to_csv(index=False).encode("utf-8")

    st.download_button(
        label="📥 Download Current Results as CSV",
        data=csv,
        file_name="motorsim_results.csv",
        mime="text/csv"
    )


    st.info("You can export the current motor simulation result table as a CSV file.")