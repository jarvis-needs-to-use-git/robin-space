import meep as mp
import numpy as np
import matplotlib.pyplot as plt
import skrf as rf

def run_floquet_simulation(theta_deg, freq=1.0):
    """
    Skeleton for a Floquet Unit Cell simulation in Meep.
    theta_deg: Scanning angle in degrees.
    freq: Frequency of interest.
    """
    # 1. Constants and Geometry
    L = 0.5 
    cell = mp.Vector3(L, L, 2.0) 
    theta = np.radians(theta_deg)
    
    # 2. Bloch-periodic boundary conditions (k_point)
    k_x = 2 * np.pi * freq * np.sin(theta)
    k_point = mp.Vector3(k_x, 0, 0)
    
    # 3. Simulation Setup
    boundary_layers = [mp.PML(1.0, direction=mp.Z)]
    sources = [mp.Source(mp.ContinuousSource(frequency=freq),
                         component=mp.Ey,
                         center=mp.Vector3(0, 0, -0.5),
                         size=mp.Vector3(L, L, 0))]

    sim = mp.Simulation(cell_size=cell,
                        boundary_layers=boundary_layers,
                        sources=sources,
                        k_point=k_point,
                        resolution=20)

    # 4. S-Parameter Extraction (Diffraction Orders)
    orders = [-1, 0, 1]
    res_list = []
    
    # 5. Calculation of Active Reflection Coefficient (ARC)
    arc_power = 0
    s_params = []
    
    for item in res_list:
        m = item["order"]
        b_m = item["coeff"]
        power = np.abs(b_m)**2
        arc_power += power
        s_params.append({"m": m, "s_parameter": b_m, "power_fraction": power})
    
    return {
        "theta_deg": theta_deg,
        "active_reflection_coefficient": np.sqrt(arc_power),
        "total_reflected_power": arc_power,
        "modal_details": s_params
    }

def plot_arc_results(angles, arc_te, arc_tm=None):
    """
    Visualization module for Active Reflection Coefficient (ARC).
    Supports dual-polarization (TE/TM).
    """
    plt.figure(figsize=(10, 6))
    plt.plot(angles, 10 * np.log10(arc_te), 'b-o', label='ARC (TE / s-pol)')
    if arc_tm is not None:
        plt.plot(angles, 10 * np.log10(arc_tm), 'g-s', label='ARC (TM / p-pol)')
        
    plt.axhline(y=-10, color='r', linestyle='--', label='Scan Blindness Threshold (-10dB)')
    plt.title('Active Reflection Coefficient vs. Scan Angle')
    plt.xlabel('Scan Angle (Degrees)')
    plt.ylabel('ARC (dB)')
    plt.grid(True, which='both', linestyle='--', alpha=0.5)
    plt.legend()
    plt.ylim(-40, 0)
    plt.savefig('projects/robin-space/arc_scan_plot.png')
    print("Dual-pol visualization saved to projects/robin-space/arc_scan_plot.png")

def export_to_touchstone(freq, s11_complex, filename="projects/robin-space/results.s1p"):
    """
    Export simulation results to a standard Touchstone file via scikit-rf.
    """
    freq_obj = rf.Frequency(freq, freq, 1, 'ghz')
    s_array = np.array([[[s11_complex]]])
    ntw = rf.Network(frequency=freq_obj, s=s_array, name='Floquet_Result')
    ntw.write_touchstone(filename)
    print(f"Touchstone file exported to {filename}")

if __name__ == "__main__":
    # Mock data for dual-pol visualization testing
    test_angles = np.linspace(0, 60, 7)
    test_arc_te = [0.01, 0.02, 0.05, 0.4, 0.08, 0.05, 0.04]
    test_arc_tm = [0.015, 0.025, 0.04, 0.35, 0.07, 0.045, 0.035]
    
    plot_arc_results(test_angles, test_arc_te, test_arc_tm)
    print("Testing Touchstone export...")
    export_to_touchstone(10.0, 0.4 + 0.1j)
