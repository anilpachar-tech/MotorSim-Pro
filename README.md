# ⚙️ MotorSim Pro

Advanced Streamlit-based motor simulation dashboard for induction and synchronous AC motors.

## Overview
MotorSim Pro is an interactive simulation and visualization app for exploring how operating conditions affect motor performance. It is designed for lab demonstrations, student learning, and quick scenario analysis.

## Features
- Induction and synchronous motor simulation
- DC motor calculator module (speed, torque, efficiency, step response)
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

## Documentation
- Executive summary and proposed roadmap: [`docs/executive_summary.md`](docs/executive_summary.md)

## Notes
This project uses simplified analytical models and is intended for educational and analytical use.
