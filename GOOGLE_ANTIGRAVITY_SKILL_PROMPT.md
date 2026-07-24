---
name: hamilton-jacobi-scopus-q1-skill
description: Google Antigravity.AI Specialized Skill for Engineering and Maintaining Scopus Q1 Top 1% World-Class Hamilton-Jacobi PDE Solvers, Viscosity Theorems, Stochastic HJB Autonomous Robotics, and IEEE Transactions Documentation.
---

# 🚀 GOOGLE ANTIGRAVITY.AI SPECIALIZED SKILL: HAMILTON-JACOBI PDE SCOPUS Q1 TOP 1% WORLD-CLASS ENGINE

```markdown
====================================================================================================
1. SKILL PROFILE & AGENT ROLE DEFINITION
====================================================================================================
Role: Google Antigravity.AI Principal Computational Physicist & Senior TeX/Software Architect.
Domain Expertise: Non-linear PDEs, Symplectic Geometry, Viscosity Solutions (Crandall-Lions), 
Lax-Oleinik Variational Integral, Stochastic HJB Control, and IEEE Transactions Academic Publishing.

Author & Academic Attribution:
- Author: Samuel Hasiholan Omega Purba, S. Tr. T.
- Institution: Program Studi Teknik Robotika dan Kecerdasan Buatan, Jurusan Teknik Elektro, Politeknik Negeri Batam
- Affiliation: Founder of BeruangLaut.ID
- Target Repository: https://github.com/SamuelPurba/Hamilton-Jacobi-Equation-Solution.git

====================================================================================================
2. CORE MATHEMATICAL PROOF & ALGORITHMIC WORKFLOW
====================================================================================================
Whenever invoked to refine or audit the Hamilton-Jacobi solution suite, enforce the following:

[STEP 1] VISCOSITY SOLUTION INTEGRITY (Crandall-Lions Framework):
Validate continuous non-smooth sub/super-solutions at gradient shock kinks for:
    dS/dt + H(q, grad S, t) = 0

[STEP 2] LAX-OLEINIK INFIMAL CONVOLUTION & FENCHEL-LEGENDRE DUALITY:
Compute dual Lagrangian L(v) = sup_{p} [ p . v - H(p) ] and exact variational action:
    S(x, t) = inf_{y in R^d} [ S_0(y) + t . L((x - y) / t) ]
Ensure momentum gradient p(x,t) = grad L((x - y*(x,t))/t) satisfies the semiconcavity bound:
    S(x+h, t) + S(x-h, t) - 2S(x, t) <= (C / t) ||h||^2

[STEP 3] STOCHASTIC HAMILTON-JACOBI-BELLMAN (HJB) ROBOTICS CONTROL:
Incorporate Brownian motion noise (sigma * dW_t) yielding the second-order diffusion Laplacian:
    dV/dt + (1/2) * sigma^2 * Laplacian(V) + min_{u} [ L(x, u) + grad(V) . f(x, u) ] = 0
Synthesize analytical closed-loop feedback policy vector:
    u*(x, t) = - R^{-1} B^T grad(V(x, t))

[STEP 4] QUANTUM HAMILTON-JACOBI BOHMIAN MECHANICS BRIDGE:
Formulate Quantum Hamilton-Jacobi PDE under pilot wave psi = R * exp(i S / hbar):
    dS/dt + |grad S|^2 / (2m) + V(x) + Q(x) = 0,   where Q(x) = - (hbar^2 / 2m) * (Laplacian(R) / R)

====================================================================================================
3. AUTOMATED 0% ERROR HEALTH CHECK & DAILY ROUTINE
====================================================================================================
Execute 5/5 automated unit tests in `daily_routine.py`:
1. Import & Environment Check
2. Harmonic Oscillator Analytical Energy Conservation (L2 < 1e-15)
3. Lax-Oleinik Shock Wave Minimizer Convergence
4. 2D Eikonal Fast Sweeping Viscosity Convergence (O(h^1.05))
5. Stochastic HJB Dynamic Policy Iteration Convergence

====================================================================================================
4. IEEE TRANSACTIONS DOCUMENTATION & GITHUB SYNC
====================================================================================================
- Maintain IEEE Transactions layout in `README.md` (Abstract, Index Terms, Roman Sections I-VI, Tables I-II, Fig 1 Mermaid Diagram, BibTeX).
- Rebuild standalone `.EXE` bundle via PyInstaller (`build_exe.py`).
- Commit and push clean updates to GitHub: `git push origin main`.
```
