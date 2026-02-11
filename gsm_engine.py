import numpy as np

class GSMEngine:
    """
    Generalized Scattering Matrix (GSM) Engine for cascading antenna layers.
    Uses the Redheffer Star Product to combine multi-modal S-parameters.
    """

    @staticmethod
    def star_product(SA, SB):
        """
        Calculates the Redheffer Star Product of two scattering matrices SA and SB.
        SA and SB are dictionaries containing the four blocks of a GSM:
        S11, S12, S21, S22 (each a 2D numpy array of Floquet modes).
        """
        # Identity matrix for the dimension of the Floquet modes
        I = np.eye(SA['S22'].shape[0], dtype=complex)

        # Precompute the inversion term: (I - SA_22 * SB_11)^-1
        # This represents the infinite internal reflections between the two layers
        inv_term = np.linalg.inv(I - np.dot(SA['S22'], SB['S11']))

        # Calculate the four blocks of the combined matrix (S_AB)
        S11_AB = SA['S11'] + np.dot(np.dot(SA['S12'], SB['S11']), np.dot(inv_term, SA['S21']))
        S12_AB = np.dot(np.dot(SA['S12'], inv_term), SB['S12'])
        S21_AB = np.dot(np.dot(SB['S21'], np.linalg.inv(I - np.dot(SA['S22'], SB['S11']))), SA['S21'])
        S22_AB = SB['S22'] + np.dot(np.dot(SB['S21'], SA['S22']), np.dot(inv_term, SB['S12']))

        return {
            'S11': S11_AB,
            'S12': S12_AB,
            'S21': S21_AB,
            'S22': S22_AB
        }

if __name__ == "__main__":
    # Quick Test: Cascade two identical layers (dummy identity matrices)
    # If we cascade two "transparent" layers, the result should be transparent.
    dim = 3 # 3 Floquet modes
    I = np.eye(dim, dtype=complex)
    Z = np.zeros((dim, dim), dtype=complex)

    layer = {'S11': Z, 'S12': I, 'S21': I, 'S22': Z} # Transparent layer
    
    combined = GSMEngine.star_product(layer, layer)
    
    print("GSM Test: Cascading two transparent layers...")
    print("Combined S21 (should be Identity):\n", combined['S21'])
    assert np.allclose(combined['S21'], I)
    print("Test Passed.")
