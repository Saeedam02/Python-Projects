#!/usr/bin/env python3
"""
Double Pendulum Chaos Simulator
===============================

A single-file, nonlinear double-pendulum simulator that demonstrates sensitive
dependence on initial conditions. Two pendulums are released only a tiny angle
apart and integrated with a fourth-order Runge-Kutta (RK4) solver.

Features
--------
- Full nonlinear coupled equations of motion
- Two nearly identical initial conditions
- Fixed-step RK4 integration
- Rainbow, fading trajectory trails
- Real-time separation/chaos indicator
- Optional GIF or MP4 export
- Command-line configuration

Examples
--------
Run interactively:
    python double_pendulum_chaos.py

Use a smaller initial difference:
    python double_pendulum_chaos.py --delta-deg 0.0001

Save an MP4:
    python double_pendulum_chaos.py --save double_pendulum_chaos.mp4

Save a GIF:
    python double_pendulum_chaos.py --save double_pendulum_chaos.gif
"""

from __future__ import annotations

import argparse
import math
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import matplotlib.animation as animation
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import LineCollection
from matplotlib.colors import Normalize


@dataclass(frozen=True)
class PendulumParameters:
    """Physical parameters for a planar double pendulum."""

    m1: float = 1.0
    m2: float = 1.0
    l1: float = 1.0
    l2: float = 1.0
    gravity: float = 9.81

    def validate(self) -> None:
        values = {
            "m1": self.m1,
            "m2": self.m2,
            "l1": self.l1,
            "l2": self.l2,
            "gravity": self.gravity,
        }
        for name, value in values.items():
            if not math.isfinite(value) or value <= 0.0:
                raise ValueError(f"{name} must be a positive finite number.")


@dataclass(frozen=True)
class SimulationSettings:
    """Numerical and animation settings."""

    duration: float = 30.0
    dt: float = 0.002
    fps: int = 50
    trail_seconds: float = 7.0

    def validate(self) -> None:
        if not math.isfinite(self.duration) or self.duration <= 0.0:
            raise ValueError("duration must be a positive finite number.")
        if not math.isfinite(self.dt) or self.dt <= 0.0:
            raise ValueError("dt must be a positive finite number.")
        if self.fps <= 0:
            raise ValueError("fps must be positive.")
        if not math.isfinite(self.trail_seconds) or self.trail_seconds <= 0.0:
            raise ValueError("trail_seconds must be a positive finite number.")
        if self.dt >= 1.0 / self.fps:
            raise ValueError(
                "dt should be smaller than one animation frame interval "
                f"(1/fps = {1.0 / self.fps:.6f} s)."
            )


def equations_of_motion(
    state: np.ndarray,
    params: PendulumParameters,
) -> np.ndarray:
    """
    Return the state derivative for the full nonlinear double pendulum.

    State vector:
        [theta_1, omega_1, theta_2, omega_2]

    Angles are measured from the downward vertical direction.
    No small-angle approximation is used.
    """

    theta1, omega1, theta2, omega2 = state
    m1, m2 = params.m1, params.m2
    l1, l2 = params.l1, params.l2
    g = params.gravity

    delta = theta1 - theta2
    denominator_common = 2.0 * m1 + m2 - m2 * np.cos(2.0 * delta)

    alpha1_numerator = (
        -g * (2.0 * m1 + m2) * np.sin(theta1)
        - m2 * g * np.sin(theta1 - 2.0 * theta2)
        - 2.0
        * m2
        * np.sin(delta)
        * (
            omega2 * omega2 * l2
            + omega1 * omega1 * l1 * np.cos(delta)
        )
    )
    alpha1 = alpha1_numerator / (l1 * denominator_common)

    alpha2_numerator = (
        2.0
        * np.sin(delta)
        * (
            omega1 * omega1 * l1 * (m1 + m2)
            + g * (m1 + m2) * np.cos(theta1)
            + omega2 * omega2 * l2 * m2 * np.cos(delta)
        )
    )
    alpha2 = alpha2_numerator / (l2 * denominator_common)

    return np.array([omega1, alpha1, omega2, alpha2], dtype=float)


def rk4_step(
    state: np.ndarray,
    dt: float,
    params: PendulumParameters,
) -> np.ndarray:
    """Advance one fixed RK4 step."""

    k1 = equations_of_motion(state, params)
    k2 = equations_of_motion(state + 0.5 * dt * k1, params)
    k3 = equations_of_motion(state + 0.5 * dt * k2, params)
    k4 = equations_of_motion(state + dt * k3, params)
    return state + (dt / 6.0) * (k1 + 2.0 * k2 + 2.0 * k3 + k4)


def simulate(
    initial_state: Sequence[float],
    params: PendulumParameters,
    duration: float,
    dt: float,
) -> tuple[np.ndarray, np.ndarray]:
    """Integrate the double pendulum and return time and state arrays."""

    step_count = int(round(duration / dt))
    times = np.linspace(0.0, step_count * dt, step_count + 1)
    states = np.empty((step_count + 1, 4), dtype=float)
    states[0] = np.asarray(initial_state, dtype=float)

    if states[0].shape != (4,):
        raise ValueError("initial_state must contain exactly four values.")

    for index in range(step_count):
        states[index + 1] = rk4_step(states[index], dt, params)

    return times, states


def cartesian_positions(
    states: np.ndarray,
    params: PendulumParameters,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Convert angular states into Cartesian bob coordinates."""

    theta1 = states[:, 0]
    theta2 = states[:, 2]

    x1 = params.l1 * np.sin(theta1)
    y1 = -params.l1 * np.cos(theta1)
    x2 = x1 + params.l2 * np.sin(theta2)
    y2 = y1 - params.l2 * np.cos(theta2)
    return x1, y1, x2, y2


def total_energy(states: np.ndarray, params: PendulumParameters) -> np.ndarray:
    """Compute total mechanical energy for integration diagnostics."""

    theta1 = states[:, 0]
    omega1 = states[:, 1]
    theta2 = states[:, 2]
    omega2 = states[:, 3]

    m1, m2 = params.m1, params.m2
    l1, l2 = params.l1, params.l2
    g = params.gravity

    kinetic = (
        0.5 * (m1 + m2) * l1 * l1 * omega1 * omega1
        + 0.5 * m2 * l2 * l2 * omega2 * omega2
        + m2
        * l1
        * l2
        * omega1
        * omega2
        * np.cos(theta1 - theta2)
    )

    # Zero potential energy is chosen at the lowest possible configuration.
    potential = (
        (m1 + m2) * g * l1 * (1.0 - np.cos(theta1))
        + m2 * g * l2 * (1.0 - np.cos(theta2))
    )
    return kinetic + potential


def make_segments(x: np.ndarray, y: np.ndarray) -> np.ndarray:
    """Convert a polyline into segments suitable for LineCollection."""

    points = np.column_stack((x, y)).reshape(-1, 1, 2)
    if len(points) < 2:
        return np.empty((0, 2, 2), dtype=float)
    return np.concatenate((points[:-1], points[1:]), axis=1)


def trail_colors(
    count: int,
    phase: float = 0.0,
    alpha_start: float = 0.02,
    alpha_end: float = 0.95,
) -> np.ndarray:
    """Create rainbow RGBA colors that become brighter toward the newest point."""

    if count <= 0:
        return np.empty((0, 4), dtype=float)

    normalized_age = np.linspace(0.0, 1.0, count)
    color_position = np.mod(normalized_age + phase, 1.0)
    colors = plt.get_cmap("turbo")(Normalize(0.0, 1.0)(color_position))
    colors[:, 3] = np.linspace(alpha_start, alpha_end, count)
    return colors


def build_animation(
    times: np.ndarray,
    states_a: np.ndarray,
    states_b: np.ndarray,
    params: PendulumParameters,
    settings: SimulationSettings,
) -> tuple[plt.Figure, animation.FuncAnimation]:
    """Create the Matplotlib animation."""

    x1_a, y1_a, x2_a, y2_a = cartesian_positions(states_a, params)
    x1_b, y1_b, x2_b, y2_b = cartesian_positions(states_b, params)

    sample_stride = max(1, int(round(1.0 / (settings.fps * settings.dt))))
    frame_indices = np.arange(0, len(times), sample_stride, dtype=int)
    if frame_indices[-1] != len(times) - 1:
        frame_indices = np.append(frame_indices, len(times) - 1)

    sampled_times = times[frame_indices]
    sampled_x1_a = x1_a[frame_indices]
    sampled_y1_a = y1_a[frame_indices]
    sampled_x2_a = x2_a[frame_indices]
    sampled_y2_a = y2_a[frame_indices]
    sampled_x1_b = x1_b[frame_indices]
    sampled_y1_b = y1_b[frame_indices]
    sampled_x2_b = x2_b[frame_indices]
    sampled_y2_b = y2_b[frame_indices]

    trail_frames = max(2, int(round(settings.trail_seconds * settings.fps)))
    arm_reach = params.l1 + params.l2
    axis_limit = 1.12 * arm_reach

    fig, ax = plt.subplots(figsize=(9, 9), facecolor="#05050a")
    ax.set_facecolor("#05050a")
    ax.set_aspect("equal")
    ax.set_xlim(-axis_limit, axis_limit)
    ax.set_ylim(-axis_limit, axis_limit)
    ax.axis("off")

    ax.text(
        0.5,
        0.965,
        "DOUBLE PENDULUM CHAOS",
        transform=ax.transAxes,
        ha="center",
        va="top",
        color="white",
        fontsize=18,
        fontweight="bold",
    )
    ax.text(
        0.5,
        0.925,
        "Two initial angles separated by a microscopic perturbation",
        transform=ax.transAxes,
        ha="center",
        va="top",
        color="#b8b8c8",
        fontsize=10,
    )

    pivot_glow, = ax.plot(
        [0.0],
        [0.0],
        marker="o",
        markersize=15,
        color="white",
        alpha=0.12,
        zorder=7,
    )
    pivot, = ax.plot(
        [0.0],
        [0.0],
        marker="o",
        markersize=5,
        color="white",
        zorder=8,
    )

    trail_a = LineCollection([], linewidths=2.8, capstyle="round", zorder=1)
    trail_b = LineCollection([], linewidths=2.0, capstyle="round", zorder=2)
    ax.add_collection(trail_a)
    ax.add_collection(trail_b)

    rod_a, = ax.plot(
        [],
        [],
        "o-",
        linewidth=2.2,
        markersize=8,
        color="#f5f7ff",
        markerfacecolor="#4ef5ff",
        markeredgecolor="white",
        markeredgewidth=0.8,
        alpha=0.92,
        zorder=6,
    )
    rod_b, = ax.plot(
        [],
        [],
        "o-",
        linewidth=1.7,
        markersize=7,
        color="#ff69f8",
        markerfacecolor="#ff69f8",
        markeredgecolor="white",
        markeredgewidth=0.6,
        alpha=0.58,
        zorder=5,
    )

    bob_a_glow, = ax.plot(
        [],
        [],
        marker="o",
        linestyle="None",
        markersize=24,
        color="#4ef5ff",
        alpha=0.12,
        zorder=4,
    )
    bob_b_glow, = ax.plot(
        [],
        [],
        marker="o",
        linestyle="None",
        markersize=24,
        color="#ff69f8",
        alpha=0.10,
        zorder=3,
    )

    status_text = ax.text(
        0.025,
        0.035,
        "",
        transform=ax.transAxes,
        ha="left",
        va="bottom",
        color="white",
        fontsize=10,
        family="monospace",
    )

    energy_a = total_energy(states_a, params)
    energy_reference = energy_a[0]
    relative_energy_error = np.max(
        np.abs((energy_a - energy_reference) / max(abs(energy_reference), 1e-12))
    )

    artists = (
        trail_a,
        trail_b,
        rod_a,
        rod_b,
        bob_a_glow,
        bob_b_glow,
        pivot_glow,
        pivot,
        status_text,
    )

    def init() -> tuple:
        rod_a.set_data([], [])
        rod_b.set_data([], [])
        bob_a_glow.set_data([], [])
        bob_b_glow.set_data([], [])
        trail_a.set_segments([])
        trail_b.set_segments([])
        status_text.set_text("")
        return artists

    def update(frame: int) -> tuple:
        rod_a.set_data(
            [0.0, sampled_x1_a[frame], sampled_x2_a[frame]],
            [0.0, sampled_y1_a[frame], sampled_y2_a[frame]],
        )
        rod_b.set_data(
            [0.0, sampled_x1_b[frame], sampled_x2_b[frame]],
            [0.0, sampled_y1_b[frame], sampled_y2_b[frame]],
        )
        bob_a_glow.set_data([sampled_x2_a[frame]], [sampled_y2_a[frame]])
        bob_b_glow.set_data([sampled_x2_b[frame]], [sampled_y2_b[frame]])

        start = max(0, frame - trail_frames)
        xa = sampled_x2_a[start : frame + 1]
        ya = sampled_y2_a[start : frame + 1]
        xb = sampled_x2_b[start : frame + 1]
        yb = sampled_y2_b[start : frame + 1]

        segments_a = make_segments(xa, ya)
        segments_b = make_segments(xb, yb)
        trail_a.set_segments(segments_a)
        trail_b.set_segments(segments_b)
        trail_a.set_color(trail_colors(len(segments_a), phase=0.00))
        trail_b.set_color(
            trail_colors(
                len(segments_b),
                phase=0.48,
                alpha_start=0.015,
                alpha_end=0.72,
            )
        )

        separation = math.hypot(
            sampled_x2_a[frame] - sampled_x2_b[frame],
            sampled_y2_a[frame] - sampled_y2_b[frame],
        )
        normalized_separation = separation / arm_reach

        status_text.set_text(
            f"time          {sampled_times[frame]:7.2f} s\n"
            f"bob separation {separation:7.4f} m\n"
            f"normalized     {normalized_separation:7.4f}\n"
            f"max RK4 ΔE/E   {relative_energy_error:7.2e}"
        )
        return artists

    ani = animation.FuncAnimation(
        fig,
        update,
        init_func=init,
        frames=len(frame_indices),
        interval=1000.0 / settings.fps,
        blit=True,
        repeat=True,
        cache_frame_data=False,
    )
    fig.tight_layout(pad=0)
    return fig, ani


def save_animation(
    ani: animation.FuncAnimation,
    output_path: Path,
    fps: int,
    dpi: int,
) -> None:
    """Save the animation as GIF or MP4."""

    suffix = output_path.suffix.lower()
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if suffix == ".gif":
        try:
            writer = animation.PillowWriter(fps=fps)
        except Exception as exc:
            raise RuntimeError(
                "GIF export requires Pillow. Install it with: pip install pillow"
            ) from exc
    elif suffix == ".mp4":
        if not animation.writers.is_available("ffmpeg"):
            raise RuntimeError(
                "MP4 export requires FFmpeg to be installed and available on PATH."
            )
        writer = animation.FFMpegWriter(
            fps=fps,
            bitrate=4500,
            metadata={
                "title": "Double Pendulum Chaos",
                "artist": "Python / Matplotlib",
            },
        )
    else:
        raise ValueError("Output file must end in .gif or .mp4.")

    ani.save(str(output_path), writer=writer, dpi=dpi)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Animate two nonlinear double pendulums whose initial angles differ "
            "by a tiny amount."
        )
    )
    parser.add_argument(
        "--theta1-deg",
        type=float,
        default=120.0,
        help="Initial first-arm angle in degrees (default: 120).",
    )
    parser.add_argument(
        "--theta2-deg",
        type=float,
        default=-10.0,
        help="Initial second-arm angle in degrees (default: -10).",
    )
    parser.add_argument(
        "--omega1",
        type=float,
        default=0.0,
        help="Initial first-arm angular velocity in rad/s.",
    )
    parser.add_argument(
        "--omega2",
        type=float,
        default=0.0,
        help="Initial second-arm angular velocity in rad/s.",
    )
    parser.add_argument(
        "--delta-deg",
        type=float,
        default=0.001,
        help=(
            "Perturbation added to the second pendulum's first angle, "
            "in degrees (default: 0.001)."
        ),
    )
    parser.add_argument(
        "--duration",
        type=float,
        default=30.0,
        help="Simulated duration in seconds (default: 30).",
    )
    parser.add_argument(
        "--dt",
        type=float,
        default=0.002,
        help="RK4 time step in seconds (default: 0.002).",
    )
    parser.add_argument(
        "--fps",
        type=int,
        default=50,
        help="Animation frames per second (default: 50).",
    )
    parser.add_argument(
        "--trail-seconds",
        type=float,
        default=7.0,
        help="Visible trail history in seconds (default: 7).",
    )
    parser.add_argument(
        "--m1",
        type=float,
        default=1.0,
        help="Mass of the first bob in kilograms.",
    )
    parser.add_argument(
        "--m2",
        type=float,
        default=1.0,
        help="Mass of the second bob in kilograms.",
    )
    parser.add_argument(
        "--l1",
        type=float,
        default=1.0,
        help="Length of the first rod in metres.",
    )
    parser.add_argument(
        "--l2",
        type=float,
        default=1.0,
        help="Length of the second rod in metres.",
    )
    parser.add_argument(
        "--gravity",
        type=float,
        default=9.81,
        help="Gravitational acceleration in m/s².",
    )
    parser.add_argument(
        "--save",
        type=Path,
        default=None,
        help="Optional output file ending in .gif or .mp4.",
    )
    parser.add_argument(
        "--dpi",
        type=int,
        default=130,
        help="Export resolution in dots per inch (default: 130).",
    )
    parser.add_argument(
        "--no-show",
        action="store_true",
        help="Do not open an interactive window after rendering.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_arguments()

    params = PendulumParameters(
        m1=args.m1,
        m2=args.m2,
        l1=args.l1,
        l2=args.l2,
        gravity=args.gravity,
    )
    settings = SimulationSettings(
        duration=args.duration,
        dt=args.dt,
        fps=args.fps,
        trail_seconds=args.trail_seconds,
    )
    params.validate()
    settings.validate()

    initial_state_a = np.array(
        [
            np.deg2rad(args.theta1_deg),
            args.omega1,
            np.deg2rad(args.theta2_deg),
            args.omega2,
        ],
        dtype=float,
    )
    initial_state_b = initial_state_a.copy()
    initial_state_b[0] += np.deg2rad(args.delta_deg)

    print("Simulating nonlinear double pendulums...")
    print(f"Initial angular difference: {args.delta_deg:.9f}°")

    times, states_a = simulate(
        initial_state=initial_state_a,
        params=params,
        duration=settings.duration,
        dt=settings.dt,
    )
    _, states_b = simulate(
        initial_state=initial_state_b,
        params=params,
        duration=settings.duration,
        dt=settings.dt,
    )

    fig, ani = build_animation(
        times=times,
        states_a=states_a,
        states_b=states_b,
        params=params,
        settings=settings,
    )

    if args.save is not None:
        print(f"Saving animation to: {args.save}")
        save_animation(ani, args.save, settings.fps, args.dpi)
        print("Export complete.")

    if not args.no_show:
        plt.show()
    else:
        plt.close(fig)


if __name__ == "__main__":
    main()
