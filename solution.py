import probability
import sys


class Problem:

    def __init__(self, fh):
        """ Place here your code to load problem from opened file object fh
            and use probability.BayesNet() to create the Bayesian network"""

        building = Building()

        for ln in (ln for ln in fh.readlines() if len(ln.split()) > 0):
            l_array = ln.split()
            # Set of Rooms
            if l_array[0] == 'R':
                return NotImplementedError

            # Set of connections
            elif l_array[0] == 'C':
                return NotImplementedError

            # Set of sensors
            elif l_array[0] == 'S':
                return NotImplementedError

            # Propagation Probabilities
            elif l_array[0] == 'P':
                return NotImplementedError

            # Measurement
            elif l_array[0] == 'M':
                return NotImplementedError

            else:
                raise RuntimeError("Bad Format Error")


        net = probability.BayesNet(node_specs)

    def solve(self):
        """ Place here your code to determine the maximum likelihood solution
            returning the solution room name and likelihood
            use probability.elimination_ask() to perform probabilistic inference"""
        prob = 0
        likelihood = 0

        for rooms in museum:
            res = probability.elimination_ask(rooms).show_approx()
            if prob <= res.prob:
                room = rooms
                likelihood = res.prob

        return (room, likelihood)


def solver(input_file):
    return Problem(input_file).solve()


class Building:

    def __init__(self):
        self.rooms = []
        self.connections = []
        self.sensors = []

    def add_room(self,room):
        self.room.add(room)

    def add_connection(self,connection):
        self.connections.add(connection)


"""main"""


def main():
    if len(sys.argv) > 1:
        with open(sys.argv[1], 'r') as f:
            sol = solver(f)
            f.close()
            print("Solution:", sol)
    else:
        print("Usage:", sys.argv[0], "<filename>")


if __name__ == '__main__':
    main()
