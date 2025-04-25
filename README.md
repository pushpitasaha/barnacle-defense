# Barnacle Defense Evolution Simulations

Simulating how inducible defense traits evolve in barnacle populations over time using evolutionary algorithms.

---

## About

This project reimplements and optimizes the computational models from the paper:
**"Relationship of Reproduction and Evolutionary Computation to Analytical Modeling of the Ecological Genetics of Inducible Defenses" (Townsend et al., SAC 2012).**

It uses Python, NumPy, and Flask to simulate and visualize how barnacle morphs like "bent" shells emerge under predator pressure.

---

## Models Implemented

- **Mendelian Recombination (Baseline)**
- **Evolution Strategies (Bit-flip Mutation)**
- **Evolution Strategies (Gaussian Mutation)**
- **Patch-local mating models**
- **Nearest Neighbor mating models**

---

## Optimizations

- JIT compilation (Numba)
- Vectorized genome operations
- Parallel execution 

---

## Web UI

An interactive Flask app to configure and visualize simulations live.

---

## Setup

```bash
    git clone https://github.com/pushpitasaha/barnacle-defense.git
    cd barnacle-defense
    pip install -r requirements.txt
```

---

## Tests

```bash
    pytest tests/
```

---

## Contributors

- In 2012, Dr. Gloria Childress Townsend, Ph.D., Chair of the Computer Science Department at DePauw University, developed the original computational simulation based on the mathematical model by Prof. Wade N. Hazel (Biological Sciences, DePauw University) and Prof. Benjamin Steffen (Integrative Biology, University of California, Berkeley).

- In April 2025, Pushpita Saha, as an undergraduate student at DePauw University, independently took on the project after Dr. Townsend introduced it, and is now the primary developer focused on optimizing and speeding up the simulation.