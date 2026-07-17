# Relational Quantum Cosmology: An Effective Stress-Energy Tensor from an Assumed Entanglement-Decay Ansatz

This repository works out the macroscopic perfect-fluid stress-energy tensor implied by a specific ansatz for a background-independent quantum mutual-information substrate: that mutual information decays with relational distance as a power law, `I(i,j) ~ d(i,j)^-alpha`.

## Theoretical Overview

Given that ansatz, the cosmic stress-energy tensor follows as an exact algebraic consequence of a canonical partition function over the substrate's MI-Laplacian spectrum - no inflaton field or hand-fit fluid parameters needed. The dictionary `w_eff = alpha/3 - 1` links the assumed entanglement-decay exponent directly to the macroscopic equation of state.

This is a conditional, model-dependent result: the algebra connecting the ansatz to the equation of state is exact and holds at any system size, but the power-law ansatz itself is not derived here (it is motivated by analogy to modular Hamiltonians) and is the open assumption the framework rests on. See `main.tex` (Sections "Homogeneous spectral scaling" and "Illustrative phase mapping and code self-consistency") for the honest scope of what is and isn't established.

## Core Simulation Features

The background pipeline illustrates the dictionary across an imposed (not measured or derived) phase schedule spanning three named regimes:
* **The Ultraviolet Attractor Phase:** Information saturation over a complete-graph topology sets alpha -> 0, giving the de Sitter cosmological constant baseline (w = -1.0) by construction.
* **The Relational Corridor:** The imposed schedule sweeps through alpha = 3, the pressureless matter dust value (w = 0).
* **The Causal Bounce Barrier:** The schedule terminates at alpha = 6, a hyper-stiff phase (w = 1.0).

## Repository Layout

* `/main.tex`: LaTeX manuscript file.
* `/main.pdf`: PDF manuscript file.
* `/code/background_builder.py`: Generates the illustrative phase-schedule figure.
* `/code/spectral_scaling_check.py`: Self-consistency check confirming the code correctly implements the exact eigenvalue-scaling identity of Sec. "Homogeneous spectral scaling" - not independent physical evidence (that identity is exact algebra given the ansatz, so it cannot fail; see the paper for why an earlier version of this repo mistakenly described it as a "non-circular" test).
* `/figures/stress_energy_tensor_derivation.png`: Output dual-panel figure showing the illustrative phase trajectory.

## Usage and Dependencies

The simulation engine is fully self-contained and relies only on standard scientific python arrays.

### Requirements
* Python 3.8+
* numpy
* scipy
* matplotlib

### Execution
Generate the illustrative phase-schedule figure:
```bash
python code/background_builder.py
```
Run the self-consistency check (matplotlib not required):
```bash
python code/spectral_scaling_check.py
```

## Contact and Portfolio Summary

* **Author:** Paul Jarvis (Independent Theoretical Physics Researcher, UK)
* **Email:** mrpaulwjarvis@gmail.com
