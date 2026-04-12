"""DC motor utility functions for MotorSim Pro."""

from __future__ import annotations

import numpy as np
from scipy.integrate import solve_ivp


def calculate_speed(voltage: float, current: float, resistance: float, flux: float, motor_const: float) -> float:
    """Return motor speed in RPM using a simplified DC motor relation."""
    if voltage < 0 or current < 0 or resistance < 0 or flux <= 0 or motor_const <= 0:
        raise ValueError("Invalid inputs for speed calculation.")

    omega = (voltage - current * resistance) / (motor_const * flux)  # rad/s
    return float(omega * 60 / (2 * np.pi))


def calculate_torque(current: float, torque_const: float) -> float:
    """Return developed torque in N·m."""
    if current < 0 or torque_const <= 0:
        raise ValueError("Invalid inputs for torque calculation.")
    return float(current * torque_const)


def calculate_efficiency(voltage: float, current: float, torque: float, speed_rpm: float) -> float:
    """Return efficiency percentage using mechanical output / electrical input."""
    if voltage < 0 or current < 0 or torque < 0 or speed_rpm < 0:
        raise ValueError("Invalid inputs for efficiency calculation.")

    pin = voltage * current
    if pin == 0:
        return 0.0

    omega = speed_rpm * (2 * np.pi / 60)
    pout = torque * omega
codex/add-new-features-to-motorsim-pro-0tc7fg
    efficiency = float((pout / pin) * 100)
    return max(0.0, min(efficiency, 100.0))


def calculate_stall_current(voltage: float, resistance: float) -> float:
    """Return stall current in ampere."""
    if voltage < 0 or resistance < 0:
        raise ValueError("Invalid inputs for stall current calculation.")
    if resistance == 0:
        return float("inf")
    return float(voltage / resistance)


def calculate_stall_torque(voltage: float, resistance: float, torque_const: float) -> float:
    """Return stall torque in N·m."""
    if torque_const <= 0:
        raise ValueError("Invalid torque constant for stall torque calculation.")
    current = calculate_stall_current(voltage, resistance)
    return float(current * torque_const) if np.isfinite(current) else float("inf")
=======
    return float((pout / pin) * 100)
 main


def simulate_step_response(
    resistance: float,
    inductance: float,
    back_emf_const: float,
    inertia: float,
    damping: float,
    voltage_step: float,
    t_end: float = 2.0,
) -> tuple[np.ndarray, np.ndarray]:
    """Solve a simple DC motor electrical-mechanical step response."""
    if (
        resistance < 0
        or inductance <= 0
        or back_emf_const <= 0
        or inertia <= 0
        or damping < 0
        or voltage_step < 0
        or t_end <= 0
    ):
        raise ValueError("Invalid inputs for step response simulation.")

    def deriv(_: float, y: np.ndarray) -> list[float]:
        i, omega = y
        di_dt = (voltage_step - resistance * i - back_emf_const * omega) / inductance
        domega_dt = (back_emf_const * i - damping * omega) / inertia
        return [di_dt, domega_dt]

    sol = solve_ivp(deriv, [0, t_end], [0, 0], max_step=0.01)
    return sol.t, sol.y[1] * 60 / (2 * np.pi)
