import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import sys
import os
import subprocess
import json

# Import the core engine logic
from gsm_engine import GSMEngine

st.set_page_config(page_title="Robin Space | Phased Array Tool", layout="wide")

# Constants
import floquet_prototype

# Constants
# Try to find conda in standard locations or use a default
MEEP_CONDA_PATH = os.environ.get("MEEP_CONDA_PATH", "conda")
MEEP_ENV_PATH = os.environ.get("MEEP_ENV_PATH", "robin-space-env")

def run_meep_sim(theta, freq):
    """Bridge to the Meep environment."""
    
    # STRATEGY 1: Direct Module Call (Preferred for Cloud/Local Native)
    # If floquet_prototype successfully imported meep, just call it.
    if floquet_prototype.mp is not None:
        try:
            return floquet_prototype.run_floquet_simulation(theta, freq)
        except Exception as e:
            return {"error": f"Direct execution failed: {str(e)}", "status": "error"}

    # STRATEGY 2: Subprocess via 'conda run' (For Windows -> WSL cross-calling)
    # If we are here, it means we are likely on Windows without meep installed locally,
    # and we want to try to reach into WSL.
    
    cmd = [
        MEEP_CONDA_PATH, "run", "-p", MEEP_ENV_PATH, "python", 
        "floquet_prototype.py", "--theta", str(theta), "--freq", str(freq), "--json"
    ]
    try:
        # On Windows, 'conda' might be a batch file or executable, requiring shell=True or full path
        # But for robustness, let's try direct execution first.
        # If conda is not found, this will raise FileNotFoundError
        result = subprocess.run(cmd, capture_output=True, text=True, check=True, cwd=".")
        return json.loads(result.stdout)
    except FileNotFoundError:
        return {"error": "Conda/Meep not found. Please configure MEEP_CONDA_PATH.", "status": "mock"}
    except Exception as e:
        return {"error": str(e), "status": "error"}

# Sidebar for Input Parameters
st.sidebar.header("📡 Simulation Parameters")
freq = st.sidebar.slider("Frequency (GHz)", 1.0, 30.0, 10.0)
dx = st.sidebar.number_input("Element Spacing Dx (λ)", value=0.5, step=0.01)
dy = st.sidebar.number_input("Element Spacing Dy (λ)", value=0.5, step=0.01)

st.sidebar.header("🔍 Scan Control")
theta_target = st.sidebar.slider("Scan Angle (Degrees)", 0.0, 80.0, 30.0)

st.sidebar.header("🔄 GSM Cascade")
n_layers = st.sidebar.number_input("Number of Superstrate Layers", min_value=1, max_value=10, value=1)

# Engine Logic
if st.sidebar.button("🛠️ Recalculate GSM"):
    # Mock GSM creation for UI testing
    dim = 1 
    I = np.eye(dim, dtype=complex)
    layer = {'S11': I * 0.1, 'S12': I * 0.9, 'S21': I * 0.9, 'S22': I * 0.1}
    combined = layer
    for _ in range(n_layers - 1):
        combined = GSMEngine.star_product(combined, layer)
    st.sidebar.success(f"Cascaded {n_layers} layers.")

# Main Dashboard
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("Active Reflection Coefficient (ARC)")
    
    # Placeholder/Simulation Plot
    angles = np.linspace(0, 80, 20)
    mock_arc = np.exp(-((angles - theta_target)**2) / 50) * 0.4 + 0.02
    
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.plot(angles, 10 * np.log10(mock_arc), 'b-o', label='ARC (dB)')
    ax.axhline(y=-10, color='r', linestyle='--', label='Blindness Threshold')
    ax.set_xlabel("Scan Angle (Degrees)")
    ax.set_ylabel("ARC (dB)")
    ax.set_ylim(-40, 0)
    ax.grid(True, linestyle='--', alpha=0.5)
    ax.legend()
    st.pyplot(fig)

with col2:
    st.subheader("🚩 System Status")
    max_arc = 10 * np.log10(np.max(mock_arc))
    
    if max_arc > -10:
        st.error(f"SCAN BLINDNESS DETECTED!\nMax ARC: {max_arc:.2f} dB")
    else:
        st.success(f"System Optimized\nMax ARC: {max_arc:.2f} dB")
        
    st.info(f"Frequency: {freq} GHz\nGrid: {dx}λ x {dy}λ")

st.markdown("---")
if st.button("🚀 Run Meep Simulation (Single Point)"):
    with st.spinner(f"Running Meep simulation at {theta_target}°..."):
        res = run_meep_sim(theta_target, freq)
        if "error" in res:
            st.error(f"Simulation failed: {res['error']}")
        else:
            st.success("Simulation Complete")
            st.json(res)

st.button("💾 Export to .s1p")
st.caption("Developed by Jarvis for Robin Space.")
