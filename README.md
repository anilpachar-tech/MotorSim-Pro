# ⚙️ MotorSim Pro

Advanced Streamlit-based motor simulation dashboard for induction and synchronous AC motors.

## Overview
MotorSim Pro is an interactive simulation and visualization app for exploring how operating conditions affect motor performance. It is designed for lab demonstrations, student learning, and quick scenario analysis.

## Features
- Induction and synchronous motor simulation
 codex/add-new-features-to-motorsim-pro-0tc7fg
- DC motor studio (speed, torque, efficiency, stall metrics, torque-speed curve, voltage sweep, energy/cost, CSV export)

- DC motor calculator module (speed, torque, efficiency, step response)
 main
- Interactive controls (voltage, frequency, poles, load torque, slip/excitation, rheostat)
- Fault scenarios (voltage drop, overload, over-frequency, high rheostat)
- Real-time KPIs (speed, torque, current, power factor, efficiency)
- Gauge cards and rotor animation
- Performance plots and waveform visualization
- Comparison mode and CSV export

## Project Structure
```text
MotorSim-Pro/
├── app.py
├── dc_motor.py
├── motor_model.py
├── tests/
│   └── test_dc_motor.py
├── requirements.txt
├── README.md
└── docs/
    └── executive_summary.md
```

## Quick Start
1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
2. Run the app:
   ```bash
   streamlit run app.py
   ```
3. In the sidebar, choose **Simulation Domain**:
   - **AC Motors** for induction/synchronous dashboard
   - **DC Motor** for DC calculator and step-response view

## Documentation
- Executive summary and proposed roadmap: [`docs/executive_summary.md`](docs/executive_summary.md)

## Notes
This project uses simplified analytical models and is intended for educational and analytical use.
