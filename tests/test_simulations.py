import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import numpy as np
import pytest
from simulations.base import Barnacle, Patch
from simulations import sim1_mendelian, sim2_es_bitflip, sim3_es_gaussian

def test_barnacle_morph_logic():
    b = Barnacle([1]*20)
    assert b.determine_morph(True, t0=6, t1=14) == 'bent'
    assert b.determine_morph(False, t0=6, t1=14) == 'bent'

    b = Barnacle([0]*20)
    assert b.determine_morph(True, t0=6, t1=14) == 'conic'
    assert b.determine_morph(False, t0=6, t1=14) == 'conic'

    b = Barnacle([1,0]*10)
    assert b.determine_morph(True, t0=6, t1=14) == 'bent'
    assert b.determine_morph(False, t0=6, t1=14) == 'conic'

def test_patch_expose_and_cull():
    patch = Patch(1.0)  # always cue
    patch.add(Barnacle([1]*20))
    patch.add(Barnacle([0]*20))
    patch.expose()
    patch.cull()
    assert all(b.morph == 'bent' for b in patch.barnacles)

def test_sim1_runs_fast():
    progress = []
    sim1_mendelian.run(generations=10, track_callback=progress.append)
    assert len(progress) == 10
    assert all(0 <= val <= 100 for val in progress)

def test_sim2_runs_fast():
    progress = []
    sim2_es_bitflip.run(generations=10, track_callback=progress.append)
    assert len(progress) == 10
    assert all(0 <= val <= 100 for val in progress)

def test_sim3_runs_fast():
    progress = []
    sim3_es_gaussian.run(generations=10, track_callback=progress.append)
    assert len(progress) == 10
    assert all(0 <= val <= 100 for val in progress)
