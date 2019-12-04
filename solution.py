import probability
import sys
from itertools import product
from math import factorial as fact


class Problem:

    def __init__(self, fh):
        """ Place here your code to load problem from opened file object fh
            and use probability.BayesNet() to create the Bayesian network"""
        self.building = {}
        self.alarms = {}
        self.evidence = {}
        self.p = 1  # Reasonable default
        self.measurements = []
        self.net = probability.BayesNet()
        self.meas_cnt = 0

        for ln in (ln for ln in fh.readlines() if len(ln.split()) > 0):
            l_array = ln.split()
            # Set of Rooms
            if l_array[0] == 'R':
                for room in l_array[1:]:
                    self.building[room] = Room()

            # Set of connections
            elif l_array[0] == 'C':
                for word in l_array[1:]:
                    connection = word.split(',')
                    self.building[connection[0]].connections.add(connection[1])
                    self.building[connection[1]].connections.add(connection[0])

            # Set of sensors
            elif l_array[0] == 'S':
                for info in l_array[1:]:
                    sensor = info.split(':')
                    self.alarms[sensor[0]] = sensor[1:]

            # Propagation Probabilities
            elif l_array[0] == 'P':
                self.p = float(l_array[1])

            # Measurement
            elif l_array[0] == 'M':
                self.meas_cnt += 1
                meas_t = []
                for meas in l_array[1:]:
                    aux = meas.split(':')
                    meas_t.append(aux)
                self.measurements.append(meas_t)

            else:
                raise RuntimeError("Bad Format Error")

        t = 0
        # for each time instant
        for meas_t in self.measurements:
            t += 1
            for room_name, room in self.building.items():
                parents = []
                # unknown prior at start
                if t == 1:
                    self.net.add((room_name + '_1', '', 0.5))
                else:
                    # Add previous room to parents nodes
                    parents.append(room_name+'_' + str(t-1))
                    # Adds adjacent rooms
                    for adj_room in room.connections:
                        parents.append(adj_room + '_' + str(t - 1))
                    # Build truth table
                    truth_table = {}
                    for p in product((True, False), repeat=len(parents)):
                        # previous room on fire
                        if p[0] is True:
                            truth_table[p] = 1
                        else:
                            truth_table[p] = self.p if p.count(True) > 0 else 0
                    # Add room to net
                    self.net.add((room_name + '_' + str(t), parents, truth_table))

            # Inserts sensor and adds measurement to evidence pool
            for meas in meas_t:
                sensor_room = self.alarms[meas[0]][0] + '_' + str(t)
                # True: TPR , False: FPR
                self.net.add((meas[0] + '_' + str(t), sensor_room,
                              {True: float(self.alarms[meas[0]][1]), False: float(self.alarms[meas[0]][2])}))
                self.evidence[meas[0] + '_' + str(t)] = True if meas[1] == 'T' else False

    def solve(self):
        """ Place here your code to determine the maximum likelihood solution
            returning the solution room name and likelihood
            use probability.elimination_ask() to perform probabilistic inference"""
        likelihood = 0
        highest_p_room = None

        # calculates P(room_fire | sensor_readings)
        for room in self.building.keys():
            res = probability.elimination_ask(room + '_' + str(self.meas_cnt),
                                              self.evidence, self.net)[True]
            if likelihood <= res:
                highest_p_room = room
                likelihood = res

        return highest_p_room, likelihood


def solver(input_file):
    return Problem(input_file).solve()


class Room:

    def __init__(self):
        self.connections = set()


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
