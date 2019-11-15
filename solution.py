import probability


class Problem:

    def __init__(self, fh):
        """ Place here your code to load problem from opened file object fh
            and use probability.BayesNet() to create the Bayesian network"""

    def solve(self):
        """ Place here your code to determine the maximum likelihood solution
            returning the solution room name and likelihood
            use probability.elimination_ask() to perform probabilistic inference"""

        return (room, likelihood)


def solver(input_file):
    return Problem(input_file).solve()


"""main"""


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            sol = solver(f)
            f.close()

    else:
        print("Usage:", sys.argv[0], "<filename>")


if __name__ == '__main__':
    main()
