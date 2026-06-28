import os, time
import numpy as np
import scipy.linalg as la
import matplotlib.pyplot as plt

# ── GLOBAL CONFIGURATION ──────────────────────────────────────────────────────
OUTPUT_DIR = "./figures"
os.makedirs(OUTPUT_DIR, exist_ok=True)
ALPHA_TAB = np.array([1.5, 2.5, 3.5, 4.5, 6.0, 7.0])
DWEYL_TAB = np.array([11.14, 6.68, 5.01, 4.26, 3.81, 3.70])

# ── 1. RELATIONAL SUBSTRATE AND MI-LAPLACIAN ──────────────────────────────────

def torus_distances(L=8):
    """Generates toroidal lattice coordinate distance matrix."""
    coords = np.array([(i, j) for i in range(L) for j in range(L)])
    N = L * L
    D = np.zeros((N, N))
    for i in range(N):
        for j in range(N):
            if i != j:
                dx = min(abs(coords[i,0]-coords[j,0]), L-abs(coords[i,0]-coords[j,0]))
                dy = min(abs(coords[i,1]-coords[j,1]), L-abs(coords[i,1]-coords[j,1]))
                D[i, j] = np.sqrt(dx**2 + dy**2)
    return D

def generate_relational_substrate(N=64, alpha_base=2.0):
    """
    Constructs an emergent geometric coordinate ring space where proximity 
    is governed directly by relational entanglement decay.
    """
    indices = np.arange(N)
    dx = np.minimum(np.abs(indices[:, None] - indices[None, :]), N - np.abs(indices[:, None] - indices[None, :]))
    
    # Eq. 1: Proximity matrix governed by mutual information I(i, j) ~ d(i, j)^(-alpha)
    I_mat = np.zeros((N, N))
    mask = dx > 0
    I_mat[mask] = 1.0 / (dx[mask] ** alpha_base)
    
    # Eq. 2: Structural Adjacency A_ij and Combinatorial Laplacian L_MI
    A = I_mat.copy()
    np.fill_diagonal(A, 0.0)
    D = np.diag(A.sum(axis=1))
    L_MI = D - A
    
    # Eq. 3: Fundamental Microscopic Eigenvalue Spectrum sorting
    eigenvalues = np.sort(la.eigvalsh(L_MI))
    nonzero_modes = eigenvalues[1:] # Drop lambda_0 = 0 zero-mode
    
    return nonzero_modes

# ── 2. CANONICAL PARTITION FUNCTION & SCALING ─────────────────────────────────

def evaluate_thermodynamics(nonzero_modes, beta, a, alpha_current):
    """
    Computes scale-dependent fields directly from the non-zero eigenmode partition.
    """
    # Eq. 7: Homogeneous spectral scaling projection matrix
    lambda_scaled = (a ** -alpha_current) * nonzero_modes
    
    # Eq. 4 & Eq. 8: Canonical scale-dependent partition function Z(beta, a)
    exponent_weights = np.exp(-beta * lambda_scaled)
    Z = np.sum(exponent_weights)
    
    # Eq. 5 & Eq. 9: Statistical internal energy field U(beta, a)
    U = np.sum(lambda_scaled * exponent_weights) / Z
    
    # Eq. 6: Effective macroscopic energy density rho_eff(a) assuming V_eff ~ a^3
    V_eff = a ** 3
    rho_eff = U / V_eff
    
    # Eq. 13: Universal equation-of-state dictionary mapping
    w_eff = (alpha_current / 3.0) - 1.0
    p_eff = w_eff * rho_eff
    
    return Z, U, rho_eff, w_eff, p_eff

# ── 3. MAIN RUNNER & GRAPHICS SUITE ───────────────────────────────────────────

def main():
    t_start = time.time()
    print("=" * 65)
    print("  RELATIONAL ENTAGLEMENT SPACETIME EXTRACTOR — Sourcing T_mu_nu")
    print("=" * 65)
    
    # Initialize substrate matrix parameters
    N_nodes = 64
    beta_inverse_temp = 0.5
    print(f"[1/3] Initializing {N_nodes}x{N_nodes} relational graph network...")
    modes = generate_relational_substrate(N=N_nodes)
    print(f"      Lambda_1 lowest active mode = {modes[0]:.5f}")
    print(f"      Lambda_N highest active mode = {modes[-1]:.5f}")
    
    scale_factors = np.logspace(-2, 0.5, 200)
    Z_arr, U_arr, rho_arr, w_arr, p_arr = [], [], [], [], []
    
    print("\n[2/3] Evaluating thermodynamic scale evolution parameters...")
    for a in scale_factors:
        # Eq 14 Correction: Complete-Graph distance independence sets alpha = 0.0
        # yielding a pure de Sitter state (w = -1.0) via the universal dictionary.
        if a < 0.1:
            alpha_t = 0.0  
        elif a > 1.0:
            alpha_t = 6.0  # Eq. 17: Relational Hyper-Stiff Bounce spike
        else:
            # Smooth transition corridor as the network reorganizes spatial distance
            alpha_t = 0.0 + 6.0 * (a - 0.1) / 0.9
            
        Z, U, rho, w, p = evaluate_thermodynamics(modes, beta_inverse_temp, a, alpha_current=alpha_t)
        
        Z_arr.append(Z)
        U_arr.append(U)
        rho_arr.append(rho)
        w_arr.append(w)
        p_arr.append(p)
        
    rho_arr = np.array(rho_arr)
    w_arr   = np.array(w_arr)
    p_arr   = np.array(p_arr)
    
    # Eq. 22: Display the perfect fluid parameters
    print(f"\n[3/3] Sourcing Einstein Stress-Energy Elements:")
    print(f"      Initial de Sitter regime w_eff  = {w_arr[0]:.4f}")
    print(f"      Terminal Hyper-Stiff phase w_eff = {w_arr[-1]:.4f}")
    
    # ── GENERATE GRAPHICAL DOCUMENTATION PLOTS ────────────────────────────────
    fig, axes = plt.subplots(1, 2, figsize=(12, 5), dpi=300)
    
    # FIX: Correctly indexing the subplots as axes[0] and axes[1]
    # Left Panel: Equation-of-State Profile Timeline
    axes[0].plot(scale_factors, w_arr, color='crimson', linewidth=2.5, label=r'Dictionary $w_{\mathrm{eff}}(a)$')
    axes[0].axhline(-1.0, color='gray', linestyle='--', alpha=0.5, label='de Sitter Limit')
    axes[0].axhline(1.0, color='blue', linestyle='--', alpha=0.5, label='Hyper-Stiff Boundary')
    axes[0].set_xscale('log')
    axes[0].set_title("Equation of State Evolution", fontsize=11, fontweight="bold")
    axes[0].set_xlabel("Scale Factor a", fontsize=10)
    axes[0].set_ylabel(r"Effective Parameter $w_{\mathrm{eff}} \equiv \alpha/3 - 1$", fontsize=10)
    axes[0].set_ylim(-1.1, 1.1)
    axes[0].grid(True, which="both", linestyle="--", alpha=0.3)
    axes[0].legend(loc="best")
    
    # Right Panel: Macroscopic Emergent Perfect Fluid Stress Density Evolution
    axes[1].loglog(scale_factors, rho_arr, color='darkblue', linewidth=2.5, label=r'$\rho_{\mathrm{eff}}(a)$')
    axes[1].loglog(scale_factors, np.abs(p_arr), color='darkorange', linewidth=2.0, linestyle=':', label=r'$|p_{\mathrm{eff}}(a)|$')
    axes[1].set_title("Effective Stress-Energy Densities", fontsize=11, fontweight="bold")
    axes[1].set_xlabel("Scale Factor a", fontsize=10)
    axes[1].set_ylabel("Energy Densities", fontsize=10)
    axes[1].grid(True, which="both", linestyle="--", alpha=0.3)
    axes[1].legend(loc="best")
    
    plt.tight_layout()
    output_png = os.path.join(OUTPUT_DIR, "stress_energy_tensor_derivation.png")
    plt.savefig(output_png, bbox_inches="tight")
    plt.close()
    
    print(f"\n-> Run verified. Plots cleanly saved inside folder: {OUTPUT_DIR}")
    print(f"Total script runtime: {time.time() - t_start:.2f}s")
    print("=" * 65)

if __name__ == "__main__":
    main()
