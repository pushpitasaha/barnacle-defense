import numpy as np

# barnacle individual with genome and sensitivity traits
class Barnacle:
    def __init__(self, genome):
        self.genome = np.array(genome)
        self.sensitivity = sum(genome)
        self.morph = None

    # determine morph based on sensitivity thresholds
    def determine_morph(self, cue, t0=6, t1=14):
        if self.sensitivity < t0:
            self.morph = 'conic'
        elif self.sensitivity > t1:
            self.morph = 'bent'
        else:
            self.morph = 'bent' if cue else 'conic'
        return self.morph

# patch containing multiple barnacles and environmental cue
class Patch:
    def __init__(self, cue_prob):
        self.barnacles = []
        self.cue_prob = cue_prob

    # expose barnacles to environmental cue
    def expose(self):
        for b in self.barnacles:
            cue = np.random.rand() < self.cue_prob
            b.determine_morph(cue)

    # cull barnacles that are not bent morph
    def cull(self):
        self.barnacles = [b for b in self.barnacles if b.morph == 'bent']

    # add a new barnacle to the patch
    def add(self, barnacle):
        self.barnacles.append(barnacle)
