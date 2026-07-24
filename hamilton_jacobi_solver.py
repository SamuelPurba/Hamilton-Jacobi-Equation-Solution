"""
====================================================================================================
HAMILTON-JACOBI PDE PERFECT SOLVER & RESEARCH SUITE (SCOPUS Q1 TOP 1% WORLD CLASS)
Author: Samuel Hasiholan Omega Purba, S. Tr. T.
Prodi Teknik Robotika dan Kecerdasan Buatan, Jurusan Teknik Elektro, Politeknik Negeri Batam
Founder: BeruangLaut.ID
Quote: "don't be doubt to be Great" [1 Thessalonians 2:15]
====================================================================================================
"""

import sys
import os
import numpy as np
import matplotlib
matplotlib.use('QtAgg')
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qtagg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QTabWidget, QLabel, QPushButton, QComboBox, QDoubleSpinBox,
    QSpinBox, QGroupBox, QFormLayout, QTextEdit, QFileDialog, QSplitter,
    QMessageBox, QProgressBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal
from PyQt6.QtGui import QFont, QIcon

class HamiltonJacobiEngine:
    """
    Core Mathematical Engine for Hamilton-Jacobi PDE:
    dS/dt + H(q, dS/dq, t) = 0
    """

    @staticmethod
    def solve_harmonic_oscillator_analytical(q, t, m=1.0, omega=1.0, E=1.0):
        """
        Analytical solution for 1D Harmonic Oscillator Hamilton-Jacobi equation:
        H(q, p) = p^2 / (2m) + 1/2 m w^2 q^2 = E
        S(q, E, t) = -E t + int sqrt(2m(E - 1/2 m w^2 q^2)) dq
        """
        p_q = np.sqrt(np.maximum(0.0, 2 * m * (E - 0.5 * m * (omega**2) * (q**2))))
        # Integral of sqrt(a^2 - q^2) dq = 0.5 * (q * sqrt(a^2 - q^2) + a^2 * arcsin(q/a))
        a = np.sqrt(2 * E / (m * omega**2))
        q_clamped = np.clip(q / a, -1.0, 1.0)
        spatial_action = 0.5 * np.sqrt(2 * m * E) * (q * np.sqrt(np.maximum(0.0, 1 - (q/a)**2)) + a * np.arcsin(q_clamped))
        time_action = -E * t
        return spatial_action + time_action, p_q

    @staticmethod
    def solve_eikonal_2d_fmm(grid_size=100, source=(50, 50), obstacle_type="circle"):
        """
        Solves 2D Eikonal Hamilton-Jacobi Equation: |grad S|^2 = 1 / f(x, y)^2
        using Fast Sweeping / Viscosity Iteration method for Robot Navigation.
        """
        N = grid_size
        dx = 1.0 / N
        S = np.full((N, N), 1e6)
        S[source[0], source[1]] = 0.0

        # Speed function f(x,y)
        speed = np.ones((N, N))
        X, Y = np.meshgrid(np.linspace(0, 1, N), np.linspace(0, 1, N))
        if obstacle_type == "circle":
            mask = (X - 0.5)**2 + (Y - 0.5)**2 < 0.04
            speed[mask] = 0.01
        elif obstacle_type == "slits":
            speed[(X > 0.4) & (X < 0.45) & ((Y < 0.4) | (Y > 0.6))] = 0.01

        # Lax-Friedrichs / Fast Sweeping Gauss-Seidel iterations
        for sweep in range(15):
            for i in range(1, N - 1):
                for j in range(1, N - 1):
                    if (i, j) == source:
                        continue
                    s_min_x = min(S[i-1, j], S[i+1, j])
                    s_min_y = min(S[i, j-1], S[i, j+1])
                    f_val = speed[i, j]
                    
                    if abs(s_min_x - s_min_y) >= dx / f_val:
                        val = min(s_min_x, s_min_y) + dx / f_val
                    else:
                        val = 0.5 * (s_min_x + s_min_y + np.sqrt(2 * (dx / f_val)**2 - (s_min_x - s_min_y)**2))
                    S[i, j] = min(S[i, j], val)

        # Gradient momentum field p = grad S
        Sy, Sx = np.gradient(S, dx)
        return X, Y, S, Sx, Sy, speed

    @staticmethod
    def method_of_characteristics_1d(q0_array, t_max=5.0, steps=200, m=1.0, omega=1.0):
        """
        Method of Characteristics for Hamilton-Jacobi:
        dq/dt = dH/dp = p/m
        dp/dt = -dH/dq = -m w^2 q
        dS/dt = p dq/dt - H = p^2/(2m) - 1/2 m w^2 q^2
        """
        dt = t_max / steps
        trajectories = []
        for q0 in q0_array:
            p0 = np.sqrt(max(0.1, 2.0 - m * omega**2 * q0**2))
            S0 = 0.0
            
            q_hist, p_hist, S_hist, t_hist = [q0], [p0], [S0], [0.0]
            q, p, S_val = q0, p0, S0
            for k in range(steps):
                t = k * dt
                # RK4 integration
                def derivatives(curr_q, curr_p):
                    dqdt = curr_p / m
                    dpdt = -m * (omega**2) * curr_q
                    dSdt = 0.5 * (curr_p**2) / m - 0.5 * m * (omega**2) * (curr_q**2)
                    return dqdt, dpdt, dSdt

                k1_q, k1_p, k1_S = derivatives(q, p)
                k2_q, k2_p, k2_S = derivatives(q + 0.5*dt*k1_q, p + 0.5*dt*k1_p)
                k3_q, k3_p, k3_S = derivatives(q + 0.5*dt*k2_q, p + 0.5*dt*k2_p)
                k4_q, k4_p, k4_S = derivatives(q + dt*k3_q, p + dt*k3_p)

                q += (dt / 6.0) * (k1_q + 2*k2_q + 2*k3_q + k4_q)
                p += (dt / 6.0) * (k1_p + 2*k2_p + 2*k3_p + k4_p)
                S_val += (dt / 6.0) * (k1_S + 2*k2_S + 2*k3_S + k4_S)

                q_hist.append(q)
                p_hist.append(p)
                S_hist.append(S_val)
                t_hist.append(t + dt)

            trajectories.append((np.array(t_hist), np.array(q_hist), np.array(p_hist), np.array(S_hist)))
        return trajectories

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hamilton-Jacobi Equation Solver & Research Suite (Scopus Q1 Top 1% World Class)")
        self.resize(1300, 850)
        self.setStyleSheet("""
            QMainWindow { background-color: #0f172a; color: #f8fafc; }
            QTabWidget::pane { border: 1px solid #334155; background-color: #1e293b; }
            QTabBar::tab { background: #0f172a; color: #94a3b8; padding: 10px 20px; font-weight: bold; border-top-left-radius: 6px; border-top-right-radius: 6px; }
            QTabBar::tab:selected { background: #1e293b; color: #38bdf8; border-bottom: 3px solid #38bdf8; }
            QGroupBox { color: #38bdf8; font-weight: bold; border: 1px solid #334155; border-radius: 8px; margin-top: 10px; padding-top: 10px; }
            QGroupBox::title { subcontrol-origin: margin; left: 10px; padding: 0 5px; }
            QLabel { color: #e2e8f0; font-size: 13px; }
            QPushButton { background-color: #2563eb; color: white; font-weight: bold; border-radius: 6px; padding: 8px 16px; font-size: 13px; }
            QPushButton:hover { background-color: #1d4ed8; }
            QPushButton:pressed { background-color: #1e40af; }
            QDoubleSpinBox, QSpinBox, QComboBox { background-color: #0f172a; color: white; border: 1px solid #475569; border-radius: 4px; padding: 4px; }
            QTextEdit { background-color: #0f172a; color: #e2e8f0; border: 1px solid #334155; font-family: 'Consolas', 'Courier New'; font-size: 13px; }
        """)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

        # Header banner
        header_box = QHBoxLayout()
        title_label = QLabel("⚡ HAMILTON-JACOBI PDE PERFECT SOLVER & RESEARCH SUITE")
        title_label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        title_label.setStyleSheet("color: #38bdf8;")
        
        subtitle_label = QLabel("Author: Samuel Hasiholan Omega Purba, S. Tr. T. | Politeknik Negeri Batam (BeruangLaut.ID)")
        subtitle_label.setStyleSheet("color: #94a3b8; font-style: italic;")
        
        header_vbox = QVBoxLayout()
        header_vbox.addWidget(title_label)
        header_vbox.addWidget(subtitle_label)
        header_box.addLayout(header_vbox)
        header_box.addStretch()
        
        quote_label = QLabel('"don\'t be doubt to be Great" [1 Thessalonians 2:15]')
        quote_label.setStyleSheet("color: #f59e0b; font-weight: bold;")
        header_box.addWidget(quote_label)
        
        layout.addLayout(header_box)

        # Tabs
        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self.tab_analytical = QWidget()
        self.tab_characteristics = QWidget()
        self.tab_hjb_robotics = QWidget()
        self.tab_monograph = QWidget()

        self.tabs.addTab(self.tab_analytical, "1. Analytical Action & Viscosity Surface")
        self.tabs.addTab(self.tab_characteristics, "2. Method of Characteristics & Phase Space")
        self.tabs.addTab(self.tab_hjb_robotics, "3. Optimal Control & Robotics HJB (2D Eikonal)")
        self.tabs.addTab(self.tab_monograph, "4. Scopus Q1 Mathematical Monograph & Proofs")

        self.init_tab_analytical()
        self.init_tab_characteristics()
        self.init_tab_hjb_robotics()
        self.init_tab_monograph()

    def init_tab_analytical(self):
        layout = QHBoxLayout(self.tab_analytical)

        # Left Controls
        controls = QGroupBox("Simulation Parameters")
        ctrl_layout = QFormLayout(controls)

        self.spin_m = QDoubleSpinBox()
        self.spin_m.setValue(1.0)
        self.spin_m.setSingleStep(0.1)

        self.spin_omega = QDoubleSpinBox()
        self.spin_omega.setValue(1.0)
        self.spin_omega.setSingleStep(0.1)

        self.spin_energy = QDoubleSpinBox()
        self.spin_energy.setValue(1.5)
        self.spin_energy.setSingleStep(0.1)

        self.spin_time = QDoubleSpinBox()
        self.spin_time.setValue(2.0)
        self.spin_time.setSingleStep(0.5)

        btn_run = QPushButton("🚀 Compute Solution Surface")
        btn_run.clicked.connect(self.update_analytical_plot)

        ctrl_layout.addRow("Mass (m):", self.spin_m)
        ctrl_layout.addRow("Frequency (ω):", self.spin_omega)
        ctrl_layout.addRow("Energy Constant (E):", self.spin_energy)
        ctrl_layout.addRow("Time (t):", self.spin_time)
        ctrl_layout.addRow(btn_run)

        layout.addWidget(controls, 1)

        # Right Plots
        self.fig_analytical = plt.figure(figsize=(8, 6), facecolor='#1e293b')
        self.canvas_analytical = FigureCanvas(self.fig_analytical)
        layout.addWidget(self.canvas_analytical, 3)

        self.update_analytical_plot()

    def update_analytical_plot(self):
        self.fig_analytical.clear()

        m = self.spin_m.value()
        omega = self.spin_omega.value()
        E = self.spin_energy.value()
        t_val = self.spin_time.value()

        q_max = np.sqrt(2 * E / (m * omega**2)) * 0.99
        q = np.linspace(-q_max, q_max, 200)

        S_val, p_val = HamiltonJacobiEngine.solve_harmonic_oscillator_analytical(q, t_val, m, omega, E)

        # Plot Action S(q, t)
        ax1 = self.fig_analytical.add_subplot(2, 1, 1)
        ax1.set_facecolor('#0f172a')
        ax1.plot(q, S_val, color='#38bdf8', lw=2.5, label=f'Action S(q, t={t_val:.1f})')
        ax1.set_title("Hamilton's Principal Action S(q, t)", color='white', fontsize=12, fontweight='bold')
        ax1.set_xlabel("Generalized Coordinate q", color='#94a3b8')
        ax1.set_ylabel("Action S", color='#94a3b8')
        ax1.tick_params(colors='#94a3b8')
        ax1.grid(True, linestyle='--', alpha=0.3)
        ax1.legend(facecolor='#1e293b', edgecolor='#334155', labelcolor='white')

        # Plot Momentum Field p(q) = dS/dq
        ax2 = self.fig_analytical.add_subplot(2, 1, 2)
        ax2.set_facecolor('#0f172a')
        ax2.plot(q, p_val, color='#10b981', lw=2.5, label='Momentum p(q) = +∂S/∂q')
        ax2.plot(q, -p_val, color='#ef4444', lw=2.5, linestyle='--', label='Momentum p(q) = -∂S/∂q')
        ax2.set_title("Momentum Field p = ∂S/∂q (Phase Contour)", color='white', fontsize=12, fontweight='bold')
        ax2.set_xlabel("Generalized Coordinate q", color='#94a3b8')
        ax2.set_ylabel("Momentum p", color='#94a3b8')
        ax2.tick_params(colors='#94a3b8')
        ax2.grid(True, linestyle='--', alpha=0.3)
        ax2.legend(facecolor='#1e293b', edgecolor='#334155', labelcolor='white')

        self.fig_analytical.tight_layout()
        self.canvas_analytical.draw()

    def init_tab_characteristics(self):
        layout = QHBoxLayout(self.tab_characteristics)

        controls = QGroupBox("Characteristics Configuration")
        ctrl_layout = QFormLayout(controls)

        self.spin_rays = QSpinBox()
        self.spin_rays.setRange(5, 30)
        self.spin_rays.setValue(12)

        self.spin_tmax = QDoubleSpinBox()
        self.spin_tmax.setValue(6.28)

        btn_run = QPushButton("⚡ Trace Phase Space Characteristics")
        btn_run.clicked.connect(self.update_characteristics_plot)

        ctrl_layout.addRow("Number of Characteristic Rays:", self.spin_rays)
        ctrl_layout.addRow("Max Simulation Time (t_max):", self.spin_tmax)
        ctrl_layout.addRow(btn_run)

        layout.addWidget(controls, 1)

        self.fig_char = plt.figure(figsize=(8, 6), facecolor='#1e293b')
        self.canvas_char = FigureCanvas(self.fig_char)
        layout.addWidget(self.canvas_char, 3)

        self.update_characteristics_plot()

    def update_characteristics_plot(self):
        self.fig_char.clear()

        num_rays = self.spin_rays.value()
        t_max = self.spin_tmax.value()

        q0_arr = np.linspace(-1.2, 1.2, num_rays)
        trajectories = HamiltonJacobiEngine.method_of_characteristics_1d(q0_arr, t_max=t_max)

        ax1 = self.fig_char.add_subplot(1, 2, 1)
        ax1.set_facecolor('#0f172a')
        for t_h, q_h, p_h, S_h in trajectories:
            ax1.plot(q_h, p_h, alpha=0.7, lw=1.5)
        ax1.set_title("Phase Space Trajectories (q vs p)", color='white', fontweight='bold')
        ax1.set_xlabel("q", color='#94a3b8')
        ax1.set_ylabel("p", color='#94a3b8')
        ax1.tick_params(colors='#94a3b8')
        ax1.grid(True, linestyle='--', alpha=0.3)

        ax2 = self.fig_char.add_subplot(1, 2, 2, projection='3d')
        ax2.set_facecolor('#0f172a')
        for t_h, q_h, p_h, S_h in trajectories:
            ax2.plot(q_h, t_h, S_h, alpha=0.8, lw=1.5)
        ax2.set_title("Action Evolution along Characteristics (q, t, S)", color='white', fontweight='bold')
        ax2.set_xlabel("q", color='#94a3b8')
        ax2.set_ylabel("t", color='#94a3b8')
        ax2.set_zlabel("S", color='#94a3b8')
        ax2.tick_params(colors='#94a3b8')

        self.fig_char.tight_layout()
        self.canvas_char.draw()

    def init_tab_hjb_robotics(self):
        layout = QHBoxLayout(self.tab_hjb_robotics)

        controls = QGroupBox("Robotics & AI Environment")
        ctrl_layout = QFormLayout(controls)

        self.combo_obs = QComboBox()
        self.combo_obs.addItems(["Circle Obstacle", "Slits / Barriers"])

        self.spin_grid = QSpinBox()
        self.spin_grid.setRange(40, 150)
        self.spin_grid.setValue(80)

        btn_run = QPushButton("🎯 Compute Viscosity Solution (FMM)")
        btn_run.clicked.connect(self.update_hjb_plot)

        ctrl_layout.addRow("Obstacle Configuration:", self.combo_obs)
        ctrl_layout.addRow("Grid Resolution (N x N):", self.spin_grid)
        ctrl_layout.addRow(btn_run)

        layout.addWidget(controls, 1)

        self.fig_hjb = plt.figure(figsize=(8, 6), facecolor='#1e293b')
        self.canvas_hjb = FigureCanvas(self.fig_hjb)
        layout.addWidget(self.canvas_hjb, 3)

        self.update_hjb_plot()

    def update_hjb_plot(self):
        self.fig_hjb.clear()

        grid_size = self.spin_grid.value()
        obs_type = "circle" if self.combo_obs.currentIndex() == 0 else "slits"

        X, Y, S, Sx, Sy, speed = HamiltonJacobiEngine.solve_eikonal_2d_fmm(grid_size=grid_size, obstacle_type=obs_type)

        ax1 = self.fig_hjb.add_subplot(1, 2, 1)
        ax1.set_facecolor('#0f172a')
        c1 = ax1.contourf(X, Y, S, 25, cmap='viridis')
        self.fig_hjb.colorbar(c1, ax=ax1, label='Action / Value Function V(x,y)')
        ax1.set_title("Viscosity Solution S(x,y) for Eikonal PDE", color='white', fontweight='bold')
        ax1.tick_params(colors='#94a3b8')

        ax2 = self.fig_hjb.add_subplot(1, 2, 2)
        ax2.set_facecolor('#0f172a')
        ax2.imshow(speed, extent=[0, 1, 0, 1], origin='lower', cmap='plasma', alpha=0.5)
        # Quiver plot for optimal control directions -grad S
        skip = max(1, grid_size // 20)
        ax2.quiver(X[::skip, ::skip], Y[::skip, ::skip], -Sx[::skip, ::skip], -Sy[::skip, ::skip], color='cyan')
        ax2.set_title("Optimal Control Feedback Vector Field u* = -∇S", color='white', fontweight='bold')
        ax2.tick_params(colors='#94a3b8')

        self.fig_hjb.tight_layout()
        self.canvas_hjb.draw()

    def init_tab_monograph(self):
        layout = QVBoxLayout(self.tab_monograph)

        txt = QTextEdit()
        txt.setReadOnly(True)
        txt.setHtml("""
        <h2 style='color:#38bdf8;'>Rigorous Mathematical Derivations & Scopus Q1 Proof Monograph</h2>
        <p><b>1. Fundamental Equation Formulation:</b></p>
        <p>The Hamilton-Jacobi Partial Differential Equation is defined on phase manifold M:</p>
        <pre style='color:#a7f3d0;'> ∂S/∂t + H(q, ∇_q S, t) = 0 </pre>

        <p><b>2. Viscosity Solution Framework (Crandall & Lions Theorem):</b></p>
        <p>Because characteristic lines intersect, smooth solutions S(q,t) develop gradient discontinuities (shocks/kinks). A bounded continuous function <i>S</i> is defined as a <b>Viscosity Subsolution</b> if for any C^1 test function φ:</p>
        <pre style='color:#fde047;'> φ_t + H(q, ∇ φ, t) ≤ 0  at local maxima </pre>

        <p><b>3. Lax-Oleinik Variational Formula:</b></p>
        <p>For convex Hamiltonians <i>H(p)</i> with Lagrangian dual <i>L(v) = sup_p { p·v - H(p) }</i>, the explicit viscosity solution is given by the infimal convolution:</p>
        <pre style='color:#f472b6;'> S(x, t) = inf_{y ∈ ℝ^d} { S_0(y) + t · L((x - y) / t) } </pre>

        <p><b>4. Application to Autonomous Robotics & AI Optimal Control (Politeknik Negeri Batam):</b></p>
        <p>In optimal robot trajectory planning, the Hamilton-Jacobi-Bellman (HJB) equation yields the Value Function V(x,t). The optimal control feedback policy is synthesized continuously via:</p>
        <pre style='color:#38bdf8;'> u*(x, t) = argmin_{u ∈ U} { L(x, u) + ∇V(x, t) · f(x, u) } </pre>

        <hr style='border: 1px solid #334155;'>
        <p style='color:#94a3b8;'><i>Authored by Samuel Hasiholan Omega Purba, S. Tr. T. — Teknik Robotika dan Kecerdasan Buatan, Politeknik Negeri Batam.</i></p>
        """)
        layout.addWidget(txt)

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()
