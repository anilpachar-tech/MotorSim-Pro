import numpy as np

# ============================================================
# MotorSim Pro Premium - Core Motor Models
# ============================================================

def _health_status(efficiency, current, torque, voltage, rheostat_resistance):
    score = 0

    if efficiency < 50:
        score += 2
    elif efficiency < 70:
        score += 1

    if current > 35:
        score += 2
    elif current > 25:
        score += 1

    if torque < 3:
        score += 1

    if voltage < 250:
        score += 1

    if rheostat_resistance > 3.5:
        score += 1

    if score <= 1:
        return "Normal"
    elif score <= 3:
        return "Warning"
    else:
        return "Critical"


def induction_motor_simulation(voltage, frequency, poles, slip, load_torque, rheostat_resistance):
    """
    Simulates induction motor behavior.
    """

    # Synchronous speed
    ns = (120 * frequency) / poles

    # Rotor speed
    nr = ns * (1 - slip)

    # Base current
    base_current = (load_torque * 0.8 + voltage * 0.02)

    # Rheostat effect (more resistance -> less current)
    current = base_current / (1 + rheostat_resistance)

    # Torque
    torque = (slip * voltage**2) / (1000 + 50 * slip)
    torque = torque * (1 / (1 + rheostat_resistance))

    # Power factor
    pf = 0.8 - slip * 0.2
    pf = max(0.6, pf)

    # Power calculations
    input_power = np.sqrt(3) * voltage * current * pf / 1000  # kW
    output_power = (2 * np.pi * nr * load_torque) / 60000  # kW
    apparent_power = np.sqrt(3) * voltage * current / 1000  # kVA
    reactive_power = np.sqrt(max(apparent_power**2 - input_power**2, 0))  # kVAr

    # Losses
    stator_loss = input_power * 0.05
    rotor_loss = input_power * slip
    total_loss = stator_loss + rotor_loss

    # Efficiency
    efficiency = (output_power / input_power) * 100 if input_power != 0 else 0
    efficiency = max(0, min(efficiency, 100))

    health = _health_status(efficiency, current, torque, voltage, rheostat_resistance)

    return {
        "Motor Type": "Induction Motor",
        "Voltage (V)": round(voltage, 2),
        "Frequency (Hz)": round(frequency, 2),
        "Poles": poles,
        "Slip": round(slip, 4),
        "Rheostat Resistance (Ohm)": round(rheostat_resistance, 2),
        "Synchronous Speed (RPM)": round(ns, 2),
        "Speed (RPM)": round(nr, 2),
        "Load Torque (Nm)": round(load_torque, 2),
        "Torque (Nm)": round(torque, 2),
        "Current (A)": round(current, 2),
        "Power Factor": round(pf, 2),
        "Input Power (kW)": round(input_power, 2),
        "Output Power (kW)": round(output_power, 2),
        "Apparent Power (kVA)": round(apparent_power, 2),
        "Reactive Power (kVAr)": round(reactive_power, 2),
        "Stator Loss (kW)": round(stator_loss, 2),
        "Rotor Loss (kW)": round(rotor_loss, 2),
        "Total Loss (kW)": round(total_loss, 2),
        "Efficiency (%)": round(efficiency, 2),
        "Health Status": health
    }


def synchronous_motor_simulation(voltage, frequency, poles, load_torque, excitation_factor, rheostat_resistance):
    """
    Simulates synchronous motor behavior.
    """

    # Synchronous speed
    ns = (120 * frequency) / poles

    # Base current
    base_current = (load_torque * 0.6 + voltage * 0.015)

    # Rheostat effect
    current = base_current / (1 + rheostat_resistance)

    # Torque
    torque = load_torque * (1 / (1 + rheostat_resistance))

    # Power factor depending on excitation
    pf = 0.85 + (excitation_factor - 1) * 0.1
    pf = max(0.7, min(pf, 1.0))

    # Power calculations
    input_power = np.sqrt(3) * voltage * current * pf / 1000  # kW
    output_power = (2 * np.pi * ns * torque) / 60000  # kW
    apparent_power = np.sqrt(3) * voltage * current / 1000  # kVA
    reactive_power = np.sqrt(max(apparent_power**2 - input_power**2, 0))  # kVAr

    # Losses
    stator_loss = input_power * 0.04
    total_loss = stator_loss

    # Efficiency
    efficiency = (output_power / input_power) * 100 if input_power != 0 else 0
    efficiency = max(0, min(efficiency, 100))

    health = _health_status(efficiency, current, torque, voltage, rheostat_resistance)

    return {
        "Motor Type": "Synchronous Motor",
        "Voltage (V)": round(voltage, 2),
        "Frequency (Hz)": round(frequency, 2),
        "Poles": poles,
        "Excitation Factor": round(excitation_factor, 2),
        "Rheostat Resistance (Ohm)": round(rheostat_resistance, 2),
        "Speed (RPM)": round(ns, 2),
        "Load Torque (Nm)": round(load_torque, 2),
        "Torque (Nm)": round(torque, 2),
        "Current (A)": round(current, 2),
        "Power Factor": round(pf, 2),
        "Input Power (kW)": round(input_power, 2),
        "Output Power (kW)": round(output_power, 2),
        "Apparent Power (kVA)": round(apparent_power, 2),
        "Reactive Power (kVAr)": round(reactive_power, 2),
        "Stator Loss (kW)": round(stator_loss, 2),
        "Total Loss (kW)": round(total_loss, 2),
        "Efficiency (%)": round(efficiency, 2),
        "Health Status": health
    }