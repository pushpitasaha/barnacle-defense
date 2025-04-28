import argparse
from simulations import sim1_mendelian, sim2_es_bitflip, sim3_es_gaussian, sim3_es_gaussian_optimized

# available simulation models
models = {
    'sim1': sim1_mendelian.run,
    'sim2': sim2_es_bitflip.run,
    'sim3': sim3_es_gaussian.run,
    'sim3_optimized': sim3_es_gaussian_optimized.run
}

# entry point for running simulations from cli
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True, help='model to run: sim1, sim2, sim3, sim3_optimized')
    parser.add_argument('--generations', type=int, default=100)
    args = parser.parse_args()

    if args.model not in models:
        raise ValueError("invalid model. choose sim1, sim2, sim3, or sim3_optimized.")
    
    models[args.model](generations=args.generations)

if __name__ == "__main__":
    main()
