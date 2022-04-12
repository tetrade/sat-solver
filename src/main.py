import argparse
from new_solve import *

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='SAT-SOLVER')
    parser.add_argument("--i", type=str, required=True)
    parser.add_argument("--o", type=str)
    args = parser.parse_args()
    print(Cnf(pars_file(args.i)).get_solution())


