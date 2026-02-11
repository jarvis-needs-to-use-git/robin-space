# Robin Space: Phased Array Tool - Manual

## 🛰️ Project Objective
The Phased Array Tool is a Python-based electromagnetic simulation suite designed for **Robin Space**. Its primary purpose is to perform **Floquet Analysis** on periodic antenna structures to predict and mitigate **Scan Blindness** and **Grating Lobes** in satellite phased arrays.

---

## 🚀 Core Methodology
The tool utilizes the **Floquet Unit Cell** approach:
1. **Periodic Boundaries:** Instead of simulating a full array, we simulate a single antenna element (unit cell).
2. **Bloch Phase Shifts:** We apply phase-shifted boundary conditions (Bloch k-points) to emulate an infinite array scanning at specific angles ($\theta, \phi$).
3. **Modal Decomposition:** The reflected fields are decomposed into **Floquet Modes** (diffraction orders) to identify exactly where power is being lost via **Flux Plane** integration.

---

## 🛠️ Components
### 1. `app.py` (Streamlit Dashboard)
The primary user interface for simulation control.
- **Interactive Control:** Adjust frequency, element spacing, and scan range via sidebar.
- **GSM Cascade:** Supports multi-layer superstrate analysis using the Redheffer Star Product.
- **Real-time Visualization:** Displays Active Reflection Coefficient (ARC) vs. Scan Angle with blindness thresholding.

### 2. `floquet_prototype.py` (Meep Engine)
The physics engine that executes the FDTD simulation.
- **Solver:** Meep (FDTD) v1.31.0.
- **Functionality:** 
    - Bloch-periodic boundary conditions for arbitrary steering.
    - Steady-state flux extraction for physics-validated ARC.
    - CLI-ready for integration with the Streamlit frontend.

### 3. `gsm_engine.py`
The mathematical engine for the Generalized Scattering Matrix (GSM).
- Performs the Redheffer Star Product to cascade S-parameters of multiple layers without re-running full 3D simulations.

---

## 📖 Usage
### Running the Dashboard
1. Activate the environment: `conda activate ./meep_env`
2. Launch Streamlit: `streamlit run app.py`

### CLI Simulation
To run a specific physics-validated point:
```bash
python floquet_prototype.py --theta 30.0 --freq 10.0 --json
```

---

## 🗺️ Roadmap
- [x] **Phase 1:** Environment & Meep Setup (v1.31.0).
- [x] **Phase 2:** Streamlit GUI & GSM Engine Integration.
- [x] **Phase 3:** Physics-Validated Flux Extraction (FDTD Steady-State).
- [ ] **Phase 4:** Scikit-rf integration for automatic Touchstone (.s1p) generation.
- [ ] **Phase 5:** Full Dual-Polarization (TE/TM) support.

---
*Created by Jarvis for Robin Space.*
