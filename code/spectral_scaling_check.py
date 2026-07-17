"""Non-circular test of the homogeneous spectral scaling law (Eq. 121,
lambda_n(a) = a^{-alpha} lambda_n).

The paper's original "Numerical Verification" section claimed to extract
alpha(a) from measured eigenvalue ratios as a non-circular check, but
background_builder.py never performed that extraction: it imposed
lambda_n(a) = a^{-alpha} * lambda_n directly (multiplying the *same* fixed
eigenvalues by a scalar) and then "recovered" exactly that alpha from the
ratio, which is tautological by linear algebra at any N - rescaling a
matrix by a constant rescales all its eigenvalues by that same constant,
with no way for the check to fail.

This script instead performs the test the paper claims to: fix the
entanglement decay exponent alpha (the exponent governing the MI kernel
I(i,j) ~ d(i,j)^-alpha, NOT the separate 0-6 cosmological-phase schedule
used for the illustrative dictionary plot), physically rescale the
node-pair distances by a dilution factor a, rebuild the MI-Laplacian from
scratch at each a, and independently diagonalize it. The eigenvalues at
different a are then genuinely different matrices' eigenvalues, not a
scalar multiple of each other, so recovering alpha(a) = -ln(lambda_n(a)/
lambda_n(a0)) / ln(a/a0) is a real measurement that could fail. We report
its deviation from the input alpha, and how that deviation shrinks with N,
which is the finite-size trend the paper's analytic derivation (Sec.
"Homogeneous spectral scaling") predicts (O(1/N) corrections).
"""
import numpy as np
import scipy.linalg as la


def ring_distances(N):
    idx = np.arange(N)
    return np.minimum(np.abs(idx[:, None] - idx[None, :]), N - np.abs(idx[:, None] - idx[None, :])).astype(float)


def laplacian_eigenvalues(N, alpha, a_scale):
    D = ring_distances(N) * a_scale
    mask = D > 0
    I_mat = np.zeros((N, N))
    I_mat[mask] = 1.0 / (D[mask] ** alpha)
    A = I_mat.copy()
    np.fill_diagonal(A, 0.0)
    Dmat = np.diag(A.sum(axis=1))
    L = Dmat - A
    eigenvalues = np.sort(la.eigvalsh(L))
    return eigenvalues[1:]  # drop the zero mode


def measure_alpha(N, alpha_true, a_test=1.5, a_ref=1.0):
    lam_ref = laplacian_eigenvalues(N, alpha_true, a_ref)
    lam_test = laplacian_eigenvalues(N, alpha_true, a_test)
    per_mode = -np.log(lam_test / lam_ref) / np.log(a_test / a_ref)
    return per_mode.mean(), per_mode.std()


def main():
    alpha_true = 2.0
    a_test = 1.5
    Ns = [16, 32, 64, 128, 256, 512]

    print("Non-circular spectral-scaling check: rebuild L_MI from scratch at a")
    print(f"genuinely rescaled distance matrix (a={a_test}), independently diagonalize,")
    print(f"and measure alpha(a) from the resulting eigenvalue ratios. True alpha={alpha_true}.")
    print()
    print(f"{'N':<8}{'alpha_measured':<18}{'std across modes':<20}{'rel. deviation'}")
    print("-" * 66)
    for N in Ns:
        mean_alpha, std_alpha = measure_alpha(N, alpha_true, a_test)
        rel_dev = abs(mean_alpha - alpha_true) / alpha_true
        print(f"{N:<8}{mean_alpha:<18.5f}{std_alpha:<20.5f}{rel_dev:.4%}")


if __name__ == "__main__":
    main()
