import numpy as np
import random
from numba import njit
from simulations.base import Barnacle, Patch

# recombine two parents using gaussian mean
@njit
def recombine_gaussian_numba(g1, g2, s1, s2):
    genome = (g1 + g2) / 2
    sigma = (s1 + s2) / 2
    return genome, sigma

# mutate genome using gaussian noise
@njit
def gaussian_mutation_numba(genome, sigma, delta_sigma):
    sigma_prime = sigma * np.exp(np.random.normal(0.0, delta_sigma, sigma.shape[0]))
    noise = np.random.normal(0.0, 1.0, sigma.shape[0]) * sigma_prime
    genome_prime = genome + noise
    genome_prime = np.clip(np.round(genome_prime), 0, 1).astype(np.int32)
    return genome_prime, sigma_prime

# optimized gaussian evolution strategy
def run(generations=10000, track_callback=None):
    np.random.seed(42)

    t0, t1 = 6, 14
    genome_length = 20
    p, G, F = 0.5, 0.5, 0.5
    mu, lam = 100, 500
    delta_sigma = 0.0001
    init_sigma = np.full(genome_length, 0.005)

    patches = [Patch(F * p), Patch((1-F)*p), Patch(G*(1-p)), Patch((1-G)*(1-p))]

    population = [(Barnacle(np.random.randint(0, 2, genome_length)), init_sigma.copy()) for _ in range(mu)]

    for gen in range(generations):
        offspring = []
        for _ in range(lam):
            p1s1, p2s2 = random.sample(population, 2)
            p1, s1 = p1s1
            p2, s2 = p2s2
            genome, sigma = recombine_gaussian_numba(p1.genome.astype(np.float32), p2.genome.astype(np.float32), s1, s2)
            genome, sigma = gaussian_mutation_numba(genome, sigma, delta_sigma)
            offspring.append((Barnacle(genome), sigma))

        for patch in patches:
            patch.barnacles = []
        for b, _ in offspring:
            patch = np.random.choice(patches, p=[F*p, (1-F)*p, G*(1-p), (1-G)*(1-p)])
            patch.add(b)

        for patch in patches:
            patch.expose()
            patch.cull()

        survivors = [(b, sigma) for b, sigma in offspring if b.morph == 'bent']

        if track_callback:
            total = len(offspring)
            bent = len(survivors)
            if total > 0:
                track_callback(bent / total * 100)

        if len(survivors) >= mu:
            population = list(random.sample(survivors, mu))
        else:
            fill = [(Barnacle(np.random.randint(0, 2, genome_length)), init_sigma.copy()) for _ in range(mu - len(survivors))]
            population = survivors + fill

    print(f"[OPTIMIZED] Finished {generations} generations of (μ,λ)-ES Gaussian simulation with Numba.")