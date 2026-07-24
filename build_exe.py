import os
import sys
import subprocess

print("=== BUILDING STANDALONE EXE FOR HAMILTON-JACOBI SOLVER ===")

cmd = [
    "py", "-3", "-m", "PyInstaller",
    "--noconfirm",
    "--onedir",
    "--windowed",
    "--name", "Hamilton_Jacobi_Solver",
    "hamilton_jacobi_solver.py"
]

print("Running command:", " ".join(cmd))
result = subprocess.run(cmd, cwd=r"D:\Rumus\Rumus Word\Hamilton-Jacobi Equation Solution")

if result.returncode == 0:
    print("SUCCESS: Standalone bundle created in dist/Hamilton_Jacobi_Solver!")
else:
    print("FAILED with exit code:", result.returncode)
