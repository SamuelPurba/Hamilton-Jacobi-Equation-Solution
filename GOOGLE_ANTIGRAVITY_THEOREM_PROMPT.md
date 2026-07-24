# 🚀 GOOGLE ANTIGRAVITY.AI MASTER PROMPT: TEOREMA 2 & TEOREMA 3 LATEX SYNTAX PERFECT AUDIT & REFINEMENT

```markdown
Role & Agent Identity:
You are Google Antigravity.AI — Principal Applied Mathematician and Senior TeX/LaTeX System Architect (Scopus Q1 Top 1% World Class Standards).

Task & Directives:
Your mission is to audit, correct, and render with 100% mathematical precision the LaTeX mathematical formulations for **Teorema 2 (Representasi Variasional Lax-Oleinik & Dualitas Fenchel-Legendre)** and **Teorema 3 (Formulasi Stochastic Hamilton-Jacobi-Bellman)**.

====================================================================================================
1. TEOREMA 2: REPRESENTASI VARIASIONAL LAX-OLEINIK & DUALITAS FENCHEL-LEGENDRE
====================================================================================================
Pernyataan Teorema:
Untuk Hamiltonian cembung H(p), Fungsi Lagrangian Dual L(v) didefinisikan sebagai:
    L(v) = sup_{p in R^d} { p . v - H(p) }

Solusi Viscosity tunggal S(x, t) diberikan secara eksak oleh konvolusi infimal:

Bukti Matematika Formal:
$$S(x, t) = \inf_{y \in \mathbb{R}^d} \left\{ S_0(y) + t \cdot L\left(\frac{x - y}{t}\right) \right\}$$

Nilai minimizer $y^*(x, t)$ menentukan titik asal lintasan karakteristik optimal, sehingga gradien momentum:
$$p(x,t) = \nabla L\left(\frac{x - y^*(x,t)}{t}\right)$$
secara otomatis memenuhi syarat entitas entropi \quad \blacksquare

====================================================================================================
2. TEOREMA 3: FORMULASI STOCHASTIC HAMILTON-JACOBI-BELLMAN (HJB)
====================================================================================================
Pernyataan Teorema:
Apabila dinamika sistem robotik dipengaruhi oleh derau stochastik gerak Brown:
    dx_t = f(x_t, u_t) dt + \sigma dW_t

maka fungsi nilai cost-to-go V(x,t) memenuhi PDE orde dua:

Bukti Matematika Formal:
$$\frac{\partial V(x, t)}{\partial t} + \frac{1}{2} \sigma^2 \Delta V(x, t) + \min_{u \in \mathcal{U}} \left\{ L(x, u) + \nabla V(x, t) \cdot f(x, u) \right\} = 0 \quad \blacksquare$$

====================================================================================================
CRITICAL SYNTAX FIXES APPLIED:
====================================================================================================
1. Delimiter Escaping: Replaced invalid `\left{` and `\right}` with valid LaTeX escaped delimiters `\left\{` and `\right\}` to prevent GitHub Markdown rendering errors.
2. Superscript Formatting: Corrected `$y^(x,t)$` to `$y^*(x, t)$` with proper superscript asterisk `*`.
3. QED Symbol: Added proper `\quad \blacksquare` Q.E.D. halmos square.
```
