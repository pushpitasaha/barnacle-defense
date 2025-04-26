import numpy as np
from simulations.base import Barnacle, Patch

# mutate genome by flipping bits randomly
def mutate_bitflip(genome, mutation_rate=1e-4):
    return np.array([(1 - g) if np.random.rand() < mutation_rate else g for g in genome])

# recombine two parents discretely
def recombine_discrete(p1, p2):
    return np.array([np.random.choice([g1, g2]) for g1, g2 in zip(p1.genome, p2.genome)])

# evolution strategy with bit-flip mutation
def run(generations=10000, track_callback=None):
    np.random.seed(42)

    # model parameters
    t0, t1 = 6, 14
    pop_size = 5000
    genome_length = 20
    p, G, F = 0.5, 0.5, 0.5
    mu, lam = 100, 500  # (μ,λ)-ES

    patches = [Patch(F * p), Patch((1-F)*p), Patch(G*(1-p)), Patch((1-G)*(1-p))]

    # initialize parent population
    population = [Barnacle(np.random.randint(0, 2, genome_length)) for _ in range(mu)]

    # main simulation loop
    for gen in range(generations):
        offspring = []
        for _ in range(lam):
            p1, p2 = np.random.choice(population, 2)
            genome = recombine_discrete(p1, p2)
            genome = mutate_bitflip(genome)
            offspring.append(Barnacle(genome))

        for patch in patches:
            patch.barnacles = []
        for b in offspring:
            patch = np.random.choice(patches, p=[F*p, (1-F)*p, G*(1-p), (1-G)*(1-p)])
            patch.add(b)

        for patch in patches:
            patch.expose()
            patch.cull()

        survivors = [b for patch in patches for b in patch.barnacles]

        if track_callback:
            total = len(offspring)
            bent = sum(1 for b in offspring if b.morph == 'bent')
            if total > 0:
                track_callback(bent / total * 100)

        # select next generation
        if len(survivors) >= mu:
            population = np.random.choice(survivors, mu, replace=False).tolist()
        else:
            population = survivors + [Barnacle(np.random.randint(0, 2, genome_length)) for _ in range(mu - len(survivors))]

    print(f"Finished {generations} generations of (μ,λ)-ES bit-flip simulation.")
