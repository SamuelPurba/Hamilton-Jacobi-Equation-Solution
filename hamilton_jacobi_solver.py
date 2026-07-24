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
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class HamiltonJacobiEngine:
    """
    Core Mathematical Engine for Hamilton-Jacobi PDE & HJB Optimal Control:
    dS/dt + H(q, dS/dq, t) = 0
    """

    @staticmethod
    def solve_harmonic_oscillator_analytical(q, t, m=1.0, omega=1.0, E=1.0):
        p_q = np.sqrt(np.maximum(0.0, 2 * m * (E - 0.5 * m * (omega**2) * (q**2))))
        a = np.sqrt(2 * E / (m * omega**2))
        q_clamped = np.clip(q / a, -1.0, 1.0)
        spatial_action = 0.5 * np.sqrt(2 * m * E) * (q * np.sqrt(np.maximum(0.0, 1 - (q/a)**2)) + a * np.arcsin(q_clamped))
        time_action = -E * t
        return spatial_action + time_action, p_q

    @staticmethod
    def solve_lax_oleinik_variational(x_grid, t, s0_func="abs", m=1.0):
        N = len(x_grid)
        y_grid = np.linspace(x_grid[0] - 5.0, x_grid[-1] + 5.0, 1000)
        
        if s0_func == "abs":
            S0_y = np.abs(y_grid)
        elif s0_func == "sin":
            S0_y = np.sin(y_grid)
        else:
            S0_y = np.maximum(0.0, 1.0 - y_grid**2)

        S_val = np.zeros(N)
        minimizer_y = np.zeros(N)

        for i, x in enumerate(x_grid):
            vel = (x - y_grid) / max(1e-4, t)
            L_val = 0.5 * m * (vel**2)
            total_action = S0_y + t * L_val
            idx_min = np.argmin(total_action)
            S_val[i] = total_action[idx_min]
            minimizer_y[i] = y_grid[idx_min]

        dx = x_grid[1] - x_grid[0]
        p_val = np.gradient(S_val, dx)
        return S_val, p_val, minimizer_y

    @staticmethod
    def solve_eikonal_2d_fmm(grid_size=100, source=None, obstacle_type="circle"):
        """
        Solves 2D Eikonal Hamilton-Jacobi Equation: |grad S|^2 = 1 / f(x, y)^2
        using Fast Sweeping / Viscosity Iteration method for Robot Navigation.
        """
        N = grid_size
        if source is None:
            source = (N // 2, N // 2)

        dx = 1.0 / N
        S = np.full((N, N), 1e6)
        S[source[0], source[1]] = 0.0

        speed = np.ones((N, N))
        X, Y = np.meshgrid(np.linspace(0, 1, N), np.linspace(0, 1, N))
        if obstacle_type == "circle":
            mask = (X - 0.5)**2 + (Y - 0.5)**2 < 0.04
            speed[mask] = 0.001
        elif obstacle_type == "slits":
            speed[(X > 0.4) & (X < 0.45) & ((Y < 0.35) | (Y > 0.65))] = 0.001

        for sweep in range(25):
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

        Sy, Sx = np.gradient(S, dx)
        return X, Y, S, Sx, Sy, speed

    @staticmethod
    def solve_stochastic_hjb_robotics(grid_size=80, noise_sigma=0.05):
        N = grid_size
        dx = 1.0 / N
        V = np.zeros((N, N))
        X, Y = np.meshgrid(np.linspace(-1, 1, N), np.linspace(-1, 1, N))
        
        target = (0.8, 0.8)
        running_cost = (X - target[0])**2 + (Y - target[1])**2 + 2.0 * np.exp(-15.0 * (X**2 + Y**2))

        for it in range(40):
            Vy, Vx = np.gradient(V, dx)
            u_x = -Vx
            u_y = -Vy
            u_norm = np.sqrt(u_x**2 + u_y**2) + 1e-6
            u_x = u_x / u_norm
            u_y = u_y / u_norm
            
            Vxx = np.gradient(Vx, dx, axis=1)
            Vyy = np.gradient(Vy, dx, axis=0)
            laplacian = Vxx + Vyy

            hjb_rhs = running_cost + (Vx * u_x + Vy * u_y) + 0.5 * (noise_sigma**2) * laplacian
            V -= 0.005 * hjb_rhs
            V[int(0.9*N), int(0.9*N)] = 0.0

        return X, Y, V, u_x, u_y

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Hamilton-Jacobi PDE Perfect Solver & Research Suite (Scopus Q1 Top 1% World Class)")
        self.resize(1350, 900)
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
            QDoubleSpinBox, QSpinBox, QComboBox { background-color: #0f172a; color: white; border: 1px solid #475569; border-radius: 4px; padding: 4px; }
            QTextEdit { background-color: #0f172a; color: #e2e8f0; border: 1px solid #334155; font-family: 'Consolas', 'Courier New'; font-size: 13px; }
        """)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)

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

        self.tabs = QTabWidget()
        layout.addWidget(self.tabs)

        self.tab_analytical = QWidget()
        self.tab_lax_oleinik = QWidget()
        self.tab_hjb_robotics = QWidget()
        self.tab_stochastic_hjb = QWidget()
        self.tab_monograph = QWidget()

        self.tabs.addTab(self.tab_analytical, "1. Analytical Action & Viscosity Surface")
        self.tabs.addTab(self.tab_lax_oleinik, "2. Lax-Oleinik Variational Formula & Shocks")
        self.tabs.addTab(self.tab_hjb_robotics, "3. Autonomous Robotics HJB (2D Eikonal)")
        self.tabs.addTab(self.tab_stochastic_hjb, "4. Stochastic HJB Optimal Control")
        self.tabs.addTab(self.tab_monograph, "5. Scopus Q1 Mathematical Monograph")

        self.init_tab_analytical()
        self.init_tab_lax_oleinik()
        self.init_tab_hjb_robotics()
        self.init_tab_stochastic_hjb()
        self.init_tab_monograph()

    def init_tab_analytical(self):
        layout = QHBoxLayout(self.tab_analytical)

        controls = QGroupBox("Simulation Parameters")
        ctrl_layout = QFormLayout(controls)

        self.spin_m = QDoubleSpinBox()
        self.spin_m.setValue(1.0)
        self.spin_omega = QDoubleSpinBox()
        self.spin_omega.setValue(1.0)
        self.spin_energy = QDoubleSpinBox()
        self.spin_energy.setValue(1.5)
        self.spin_time = QDoubleSpinBox()
        self.spin_time.setValue(2.0)

        btn_run = QPushButton("🚀 Compute Solution Surface")
        btn_run.clicked.connect(self.update_analytical_plot)

        ctrl_layout.addRow("Mass (m):", self.spin_m)
        ctrl_layout.addRow("Frequency (ω):", self.spin_omega)
        ctrl_layout.addRow("Energy Constant (E):", self.spin_energy)
        ctrl_layout.addRow("Time (t):", self.spin_time)
        ctrl_layout.addRow(btn_run)

        layout.addWidget(controls, 1)

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

        ax1 = self.fig_analytical.add_subplot(2, 1, 1)
        ax1.set_facecolor('#0f172a')
        ax1.plot(q, S_val, color='#38bdf8', lw=2.5, label=f'Action S(q, t={t_val:.1f})')
        ax1.set_title("Hamilton's Principal Action S(q, t)", color='white', fontsize=12, fontweight='bold')
        ax1.set_xlabel("q", color='#94a3b8')
        ax1.set_ylabel("Action S", color='#94a3b8')
        ax1.tick_params(colors='#94a3b8')
        ax1.grid(True, linestyle='--', alpha=0.3)
        ax1.legend(facecolor='#1e293b', edgecolor='#334155', labelcolor='white')

        ax2 = self.fig_analytical.add_subplot(2, 1, 2)
        ax2.set_facecolor('#0f172a')
        ax2.plot(q, p_val, color='#10b981', lw=2.5, label='Momentum p(q) = +∂S/∂q')
        ax2.plot(q, -p_val, color='#ef4444', lw=2.5, linestyle='--', label='Momentum p(q) = -∂S/∂q')
        ax2.set_title("Momentum Field p = ∂S/∂q (Phase Contour)", color='white', fontsize=12, fontweight='bold')
        ax2.set_xlabel("q", color='#94a3b8')
        ax2.set_ylabel("Momentum p", color='#94a3b8')
        ax2.tick_params(colors='#94a3b8')
        ax2.grid(True, linestyle='--', alpha=0.3)
        ax2.legend(facecolor='#1e293b', edgecolor='#334155', labelcolor='white')

        self.fig_analytical.tight_layout()
        self.canvas_analytical.draw()

    def init_tab_lax_oleinik(self):
        layout = QHBoxLayout(self.tab_lax_oleinik)

        controls = QGroupBox("Lax-Oleinik Configuration")
        ctrl_layout = QFormLayout(controls)

        self.combo_s0 = QComboBox()
        self.combo_s0.addItems(["Absolute Kink (|x|)", "Sinusoidal Wave (sin x)", "Parabolic Bump (1 - x^2)"])

        self.spin_lax_t = QDoubleSpinBox()
        self.spin_lax_t.setValue(1.5)
        self.spin_lax_t.setRange(0.1, 10.0)

        btn_run = QPushButton("⚡ Compute Lax-Oleinik Viscosity Solution")
        btn_run.clicked.connect(self.update_lax_plot)

        ctrl_layout.addRow("Initial Condition S0(y):", self.combo_s0)
        ctrl_layout.addRow("Evolution Time (t):", self.spin_lax_t)
        ctrl_layout.addRow(btn_run)

        layout.addWidget(controls, 1)

        self.fig_lax = plt.figure(figsize=(8, 6), facecolor='#1e293b')
        self.canvas_lax = FigureCanvas(self.fig_lax)
        layout.addWidget(self.canvas_lax, 3)

        self.update_lax_plot()

    def update_lax_plot(self):
        self.fig_lax.clear()

        idx = self.combo_s0.currentIndex()
        s0_type = "abs" if idx == 0 else ("sin" if idx == 1 else "bump")
        t_val = self.spin_lax_t.value()

        x_grid = np.linspace(-4.0, 4.0, 300)
        S_val, p_val, minimizer_y = HamiltonJacobiEngine.solve_lax_oleinik_variational(x_grid, t_val, s0_func=s0_type)

        ax1 = self.fig_lax.add_subplot(2, 1, 1)
        ax1.set_facecolor('#0f172a')
        ax1.plot(x_grid, S_val, color='#f59e0b', lw=2.5, label=f'Lax-Oleinik S(x, t={t_val:.1f})')
        ax1.set_title("Lax-Oleinik Variational Action S(x,t) [Viscosity Solution]", color='white', fontweight='bold')
        ax1.set_xlabel("x", color='#94a3b8')
        ax1.set_ylabel("S(x,t)", color='#94a3b8')
        ax1.tick_params(colors='#94a3b8')
        ax1.grid(True, linestyle='--', alpha=0.3)
        ax1.legend(facecolor='#1e293b', edgecolor='#334155', labelcolor='white')

        ax2 = self.fig_lax.add_subplot(2, 1, 2)
        ax2.set_facecolor('#0f172a')
        ax2.plot(x_grid, p_val, color='#ef4444', lw=2.0, label='Shock Wave p(x,t) = ∂S/∂x')
        ax2.set_title("Momentum Discontinuity & Shock Front p = ∂S/∂x", color='white', fontweight='bold')
        ax2.set_xlabel("x", color='#94a3b8')
        ax2.set_ylabel("p", color='#94a3b8')
        ax2.tick_params(colors='#94a3b8')
        ax2.grid(True, linestyle='--', alpha=0.3)
        ax2.legend(facecolor='#1e293b', edgecolor='#334155', labelcolor='white')

        self.fig_lax.tight_layout()
        self.canvas_lax.draw()

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
        skip = max(1, grid_size // 20)
        ax2.quiver(X[::skip, ::skip], Y[::skip, ::skip], -Sx[::skip, ::skip], -Sy[::skip, ::skip], color='cyan')
        ax2.set_title("Optimal Control Feedback Vector Field u* = -∇S", color='white', fontweight='bold')
        ax2.tick_params(colors='#94a3b8')

        self.fig_hjb.tight_layout()
        self.canvas_hjb.draw()

    def init_tab_stochastic_hjb(self):
        layout = QHBoxLayout(self.tab_stochastic_hjb)

        controls = QGroupBox("Stochastic HJB Parameters")
        ctrl_layout = QFormLayout(controls)

        self.spin_sigma = QDoubleSpinBox()
        self.spin_sigma.setValue(0.08)
        self.spin_sigma.setSingleStep(0.01)

        btn_run = QPushButton("🤖 Solve Stochastic HJB Value Field")
        btn_run.clicked.connect(self.update_stochastic_hjb_plot)

        ctrl_layout.addRow("Sensor/Actuator Noise (σ):", self.spin_sigma)
        ctrl_layout.addRow(btn_run)

        layout.addWidget(controls, 1)

        self.fig_shjb = plt.figure(figsize=(8, 6), facecolor='#1e293b')
        self.canvas_shjb = FigureCanvas(self.fig_shjb)
        layout.addWidget(self.canvas_shjb, 3)

        self.update_stochastic_hjb_plot()

    def update_stochastic_hjb_plot(self):
        self.fig_shjb.clear()

        sigma = self.spin_sigma.value()
        X, Y, V, u_x, u_y = HamiltonJacobiEngine.solve_stochastic_hjb_robotics(grid_size=70, noise_sigma=sigma)

        ax1 = self.fig_shjb.add_subplot(1, 2, 1, projection='3d')
        ax1.set_facecolor('#0f172a')
        ax1.plot_surface(X, Y, V, cmap='magma', edgecolor='none', alpha=0.9)
        ax1.set_title(f"Stochastic Value Surface V(x,y) [σ={sigma:.2f}]", color='white', fontweight='bold')
        ax1.set_xlabel("x", color='#94a3b8')
        ax1.set_ylabel("y", color='#94a3b8')
        ax1.set_zlabel("V", color='#94a3b8')
        ax1.tick_params(colors='#94a3b8')

        ax2 = self.fig_shjb.add_subplot(1, 2, 2)
        ax2.set_facecolor('#0f172a')
        c = ax2.contourf(X, Y, V, 20, cmap='magma')
        self.fig_shjb.colorbar(c, ax=ax2, label='Value Function V')
        skip = 4
        ax2.quiver(X[::skip, ::skip], Y[::skip, ::skip], u_x[::skip, ::skip], u_y[::skip, ::skip], color='cyan')
        ax2.set_title("Stochastic Optimal Policy Field u*(x,y)", color='white', fontweight='bold')
        ax2.tick_params(colors='#94a3b8')

        self.fig_shjb.tight_layout()
        self.canvas_shjb.draw()

    def init_tab_monograph(self):
        layout = QVBoxLayout(self.tab_monograph)

        txt = QTextEdit()
        txt.setReadOnly(True)
        txt.setHtml("""
        <h2 style='color:#38bdf8;'>Rigorous Mathematical Derivations & Scopus Q1 Proof Monograph</h2>
        <p><b>1. Fundamental Equation Formulation:</b></p>
        <p>The Hamilton-Jacobi Partial Differential Equation is defined on phase manifold M:</p>
        <pre style='color:#a7f3d0;'> ∂S/∂t + H(q, ∇_q S, t) = 0 </pre>

        <p><b>2. Lax-Oleinik Variational Representation & Legendre Duality:</b></p>
        <p>For convex Hamiltonians H(p), the Lagrangian L(v) is defined via Fenchel-Legendre transform:</p>
        <pre style='color:#fde047;'> L(v) = sup_{p ∈ ℝ^d} { p · v - H(p) } </pre>
        <p>The unique viscosity solution S(x,t) is given by the infimal convolution:</p>
        <pre style='color:#f472b6;'> S(x, t) = inf_{y ∈ ℝ^d} { S_0(y) + t · L((x - y) / t) } </pre>

        <p><b>3. Stochastic Hamilton-Jacobi-Bellman (HJB) for Autonomous Robotics:</b></p>
        <p>Under system dynamics dx = f(x, u) dt + σ dW_t, the Value Function V(x,t) satisfies:</p>
        <pre style='color:#38bdf8;'> ∂V/∂t + ½ σ² ΔV + min_{u ∈ 𝒰} { L(x, u) + ∇V · f(x, u) } = 0 </pre>
        <p>The continuous optimal control policy is given by <i>u*(x,t) = -R⁻¹ Bᵀ ∇V(x,t)</i>.</p>

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
