# Robin Space: Phased Array Tool - Manual

## 🛰️ Project Objective
The Phased Array Tool is a Python-based electromagnetic simulation suite designed for **Robin Space**. Its primary purpose is to perform **Floquet Analysis** on periodic antenna structures to predict and mitigate **Scan Blindness** and **Grating Lobes** in satellite phased arrays.

---

## 🚀 Core Methodology
The tool utilizes the **Floquet Unit Cell** approach:
1. **Periodic Boundaries:** Instead of simulating a full array, we simulate a single antenna element (unit cell).
2. **Bloch Phase Shifts:** We apply phase-shifted boundary conditions (Bloch k-points) to emulate an infinite array scanning at specific angles ($\theta, \phi$).
3. **Modal Decomposition:** The reflected fields are decomposed into **Floquet Modes** (diffraction orders) to identify exactly where power is being lost.

---

## 🛠️ Components
### 1. `floquet_prototype.py`
The "Engine" of the tool.
- **Solver:** Meep (FDTD).
- **Functionality:** 
    - Calculates the necessary k-point for a given steering angle.
    - Sets up the unit cell geometry and ports.
    - Extracts complex S-parameters using Eigenmode Decomposition.
    - Calculates the **Active Reflection Coefficient (ARC)**.

### 2. Visualization Module
Generates engineering-grade plots for design certification.
- **ARC vs. Scan Angle:** A dB-scale plot showing the input match as the beam steers.
- **Blindness Detection:** Automatically highlights regions where ARC > -10dB.

---

## 📖 Usage (Beta)
*Current status: Research & Prototype*

### Running a Scan
To generate a reflection profile across a range of angles:
```python
# Coming soon: CLI interface
python floquet_prototype.py --start 0 --end 60 --step 5
```

---

## 🗺️ Roadmap
- [ ] **Phase 1:** S-Parameter Extraction & ARC Plotting (In Progress)
- [ ] **Phase 2:** Scikit-rf integration for Touchstone (.s1p) export.
- [ ] **Phase 3:** Multi-modal analysis for Grating Lobe level prediction.
- [ ] **Phase 4:** Support for stacked/multi-layer structures (Generalized Scattering Matrix).

---
*Created by Jarvis for Robin Space.*
