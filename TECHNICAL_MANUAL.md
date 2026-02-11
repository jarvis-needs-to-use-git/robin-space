# Robin Space | Phased Array Tool - Technical Manual

## Overview
The **Robin Space Phased Array Tool** is a web-based application designed for the analysis and simulation of phased array antennas. It provides an interactive interface for configuring simulation parameters, visualizing Active Reflection Coefficients (ARC), and performing underlying physics simulations using `meep` (or a mock engine if `meep` is unavailable).

## System Architecture
The application is built using **Streamlit** for the frontend and integrates with custom Python modules for the physics engine:

-   **`app.py`**: The main entry point and UI controller. Handles user input, visualization, and simulation orchestration.
-   **`gsm_engine.py`**: Implements the Generalized Scattering Matrix (GSM) algorithm using the Redheffer Star Product to cascade multiple antenna layers.
-   **`floquet_prototype.py`**: Wraps the `meep` FDTD solver to perform Floquet unit cell simulations. Includes a fallback mock mode for environments without `meep`.

## Installation & Setup

### Prerequisites
-   Python 3.8+
-   `pip` package manager

### Dependencies
The project uses an **`environment.yml`** file for Conda-based dependency management (recommended for `meep` support).

**For Cloud Deployment (Streamlit Cloud):**
No action required. The platform will detect `environment.yml` and install all dependencies, including `meep`.

**For Local Development:**
```bash
conda env create -f environment.yml
conda activate robin-space-env
streamlit run app.py
```

### Environment Configuration
The application uses environment variables to locate the `meep` simulation environment (optional, for full physics simulation):

-   `MEEP_CONDA_PATH`: Path to the conda executable (default: `conda`).
-   `MEEP_ENV_PATH`: Name or path of the conda environment containing `meep` (default: `robin-space-env`).

**Windows Note:** If `meep` is not installed, the application will automatically degrade to "Mock Mode," providing simulated data for UI testing.

## User Interface (UI) Guide

### 1. Simulation Parameters (Sidebar)
Located in the left sidebar, these controls define the physical properties of the array:
-   **Frequency (GHz)**: Operating frequency of the array (Range: 1.0 - 30.0 GHz).
-   **Element Spacing Dx (λ)**: Spacing between elements in the X-dimension, normalized to wavelength (Step: 0.01).
-   **Element Spacing Dy (λ)**: Spacing between elements in the Y-dimension, normalized to wavelength (Step: 0.01).

### 2. Scan Control
-   **Scan Angle (Degrees)**: The target angle ($\theta$) for the beam steering. This updates the visualization and is passed to the simulation engine.

### 3. GSM Cascade
Configures the multi-layer simulation:
-   **Number of Superstrate Layers**: Number of dielectric layers to cascade (1-10).
-   **Recalculate GSM Button**: Triggers the `GSMEngine` to compute the combined S-parameters of the cascaded layers.

### 4. Main Dashboard
#### Active Reflection Coefficient (ARC)
-   Displays a plot of ARC (dB) vs. Scan Angle.
-   **Blue Line**: The calculated ARC profile.
-   **Red Line**: Blindness Threshold (-10 dB).
-   **Visual Feedback**:
    -   **System Optimized**: Max ARC is below -10 dB (Green success message).
    -   **SCAN BLINDNESS DETECTED**: Max ARC exceeds -10 dB (Red error message).

#### Simulation & Export
-   **Run Meep Simulation (Single Point)**: Executes `floquet_prototype.py` for the current $\theta$ and Frequency. Displays the JSON result from the simulation engine.
-   **Export to .s1p**: (Placeholder) functionality to export S-parameter data.

## Physics Engines

### GSM Engine (`gsm_engine.py`)
Implements the **Redheffer Star Product** to combine scattering matrices ($S_A, S_B$):
$$S_{11}^{AB} = S_{11}^A + S_{12}^A (I - S_{11}^B S_{22}^A)^{-1} S_{11}^B S_{21}^A$$
...and corresponding terms for $S_{12}, S_{21}, S_{22}$.

### Floquet Prototype (`floquet_prototype.py`)
Performs a Unit Cell simulation:
1.  **Geometry**: Sets up a 3D cell with periodic boundary conditions.
2.  **Source**: Planewave source at the specified frequency and angle.
3.  **Boundary**: Perfectly Matched Layers (PML) in the Z-direction.
4.  **Falback**: If `meep` import fails, returns a mock JSON response with status `meep_not_found_mock_data`.

## Troubleshooting
-   **"ModuleNotFoundError: No module named 'meep'"**: The application is running in Mock Mode. Install `meep` via conda to enable full physics simulations.
-   **Use on Windows**: Ensure `MEEP_CONDA_PATH` is set if you have a wsl/conda setup, otherwise rely on the built-in mock mode.

## Appendix: Enabling MEEP Physics Engine

To get the full physics simulations working (instead of the "Mock Mode"), you need to install **Meep**. 

> **Note for Windows Users**: Meep **does not** run natively on Windows. You must use **WSL (Windows Subsystem for Linux)**.

### Step 1: Install WSL (Windows Only)
1.  Open PowerShell as Administrator.
2.  Run: `wsl --install`
3.  Restart your computer.
4.  Open the "Ubuntu" app from your customized Start menu to finish setup.

### Step 2: Install Conda in WSL
1.  In your WSL terminal (Ubuntu), download Miniconda:
    ```bash
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
    ```
2.  Install it:
    ```bash
    bash Miniconda3-latest-Linux-x86_64.sh
    ```
3.  Follow the prompts and restart your terminal.

### Step 3: Create the Meep Environment
1.  Create a fresh environment with Meep (via the pymeep package):
    ```bash
    conda create -n robin-space-env -c conda-forge pymeep python=3.10
    ```
2.  Activate it to verify:
    ```bash
    conda activate robin-space-env
    python -c "import meep; print('Meep installed!')"
    ```

### Step 4: Configure the App
You need to tell the Windows app where to find the WSL Conda environment.
Set the following environment variables (or update `app.py` defaults):

-   **`MEEP_CONDA_PATH`**: The path to your WSL conda executable.
    -   Example: `wsl /home/your_user/miniconda3/bin/conda`
-   **`MEEP_ENV_PATH`**: The name of your environment.
    -   Example: `robin-space-env`

*Alternatively, you can run the entire `app.py` **inside** WSL by cloning the repo into your WSL file system and running `streamlit run app.py` there.*
