import argparse
from simulations import sim1_mendelian

# available simulation models
models = {
    'sim1': sim1_mendelian.run,
}

# entry point for running simulations from cli
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--model', required=True, help='model to run: sim1')
    parser.add_argument('--generations', type=int, default=1000)
    args = parser.parse_args()

    if args.model not in models:
        raise ValueError("invalid model. choose sim1.")
    
    models[args.model](generations=args.generations)

if __name__ == "__main__":
    main()
