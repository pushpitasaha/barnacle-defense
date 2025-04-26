import random
import numpy as np
from simulations.base import Barnacle, Patch

# recombine two parents with gaussian averaging
def recombine_gaussian(p1, p2, s1, s2):
    genome = np.array([(g1 + g2)/2 for g1, g2 in zip(p1.genome, p2.genome)])
    sigma = np.array([(v1 + v2)/2 for v1, v2 in zip(s1, s2)])
    return genome, sigma

# mutate genome with gaussian noise
def mutate_gaussian(genome, sigma, delta_sigma=0.0001):
    sigma_prime = sigma * np.exp(np.random.normal(0, delta_sigma, size=len(sigma)))
    genome_prime = genome + np.random.normal(0, sigma_prime)
    genome_prime = np.clip(np.round(genome_prime), 0, 1).astype(int)
    return genome_prime, sigma_prime

# evolution strategy with gaussian mutation
def run(generations=10000, track_callback=None):
    np.random.seed(42)

    # model parameters
    t0, t1 = 6, 14
    genome_length = 20
    p, G, F = 0.5, 0.5, 0.5
    mu, lam = 100, 500
    init_sigma = np.full(genome_length, 0.005)

    patches = [Patch(F * p), Patch((1-F)*p), Patch(G*(1-p)), Patch((1-G)*(1-p))]

    # initialize parent population
    population = [(Barnacle(np.random.randint(0, 2, genome_length)), init_sigma.copy()) for _ in range(mu)]

    # main simulation loop
    for gen in range(generations):
        offspring = []
        for _ in range(lam):
            p1s1, p2s2 = random.sample(population, 2)
            p1, s1 = p1s1
            p2, s2 = p2s2
            genome, sigma = recombine_gaussian(p1, p2, s1, s2)
            genome, sigma = mutate_gaussian(genome, sigma)
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

        # select next generation
        if len(survivors) >= mu:
            population = list(random.sample(survivors, mu))
        else:
            fill = [(Barnacle(np.random.randint(0, 2, genome_length)), init_sigma.copy()) for _ in range(mu - len(survivors))]
            population = survivors + fill

    print(f"Finished {generations} generations of (μ,λ)-ES Gaussian simulation.")
