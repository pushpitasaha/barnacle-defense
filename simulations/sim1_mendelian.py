import numpy as np
from simulations.base import Barnacle, Patch

# mendelian recombination simulation
def run(generations=10000, track_callback=None):
    np.random.seed(42)

    # model parameters
    t0, t1 = 6, 14
    pop_size = 5000
    gene_pairs = 10
    p, G, F = 0.5, 0.5, 0.5

    # create habitat patches with different cue probabilities
    patches = [Patch(F * p), Patch((1-F)*p), Patch(G*(1-p)), Patch((1-G)*(1-p))]

    # initialize barnacle population
    barnacles = []
    for _ in range(pop_size):
        genome = np.random.randint(0, 2, gene_pairs * 2)
        b = Barnacle(genome)
        patch = np.random.choice(patches, p=[F*p, (1-F)*p, G*(1-p), (1-G)*(1-p)])
        patch.add(b)

    # main simulation loop
    for gen in range(generations):
        for patch in patches:
            patch.expose()
        # for patch in patches:
        #     patch.cull()

        # track percentage of bent morphs
        all_barnacles = [b for patch in patches for b in patch.barnacles]
        if track_callback and all_barnacles:
            bent_count = sum(1 for b in all_barnacles if b.morph == 'bent')
            track_callback(bent_count / len(all_barnacles) * 100)

        # create new generation via random mating
        new_barnacles = []
        while len(new_barnacles) < pop_size:
            p1, p2 = np.random.choice(all_barnacles, 2)
            genome = []
            for i in range(0, len(p1.genome), 2):
                # randomly inherit one gene pair from either parent
                gene_pair = p1.genome[i:i+2] if np.random.rand() < 0.5 else p2.genome[i:i+2]
                genome.extend(gene_pair)
            new_barnacles.append(Barnacle(genome))

        # distribute new generation into patches
        for patch in patches:
            patch.barnacles = []
        for b in new_barnacles:
            patch = np.random.choice(patches, p=[F*p, (1-F)*p, G*(1-p), (1-G)*(1-p)])
            patch.add(b)

    print(f"Finished {generations} generations of Mendelian simulation.")
