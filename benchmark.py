import time
from simulations import sim1_mendelian, sim2_es_bitflip, sim3_es_gaussian, sim3_es_gaussian_optimized

SIMULATIONS = {
    "sim1_mendelian": sim1_mendelian.run,
    "sim2_es_bitflip": sim2_es_bitflip.run,
    "sim3_gaussian_baseline": sim3_es_gaussian.run,
    "sim3_gaussian_optimized": sim3_es_gaussian_optimized.run,
}

def benchmark(model_name, generations=100):
    print(f"Benchmarking {model_name} for {generations} generations...")
    start = time.time()
    SIMULATIONS[model_name](generations=generations)
    duration = time.time() - start
    print(f"⏱ {model_name} took {duration:.2f} seconds\n")

def run_all():
    for name in SIMULATIONS:
        benchmark(name)

if __name__ == "__main__":
    run_all()
