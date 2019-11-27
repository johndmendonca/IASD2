import probability
import sys


class Problem:

    def __init__(self, fh):
        """ Place here your code to load problem from opened file object fh
            and use probability.BayesNet() to create the Bayesian network"""
        self.building = {}
        self.alarms = {}
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
                    aux.append(self.meas_cnt)
                    meas_t.append(aux)
                self.measurements.append(meas_t)

            else:
                raise RuntimeError("Bad Format Error")

        var = []
        t = 0
        # for each time instant
        for meas_t in self.measurements:
            t += 1
            measured_rooms = {}
            # Formatting for BayesNet()
            for meas in meas_t:
                sensor_room = self.alarms[meas[0]][0]

                if meas[1] == 'F':
                    meas[2] = 0
                elif meas[1] == 'T':
                    meas[2] = 1
                else:
                    raise RuntimeError("Bad Format Error")
                meas[0] = meas[0] + '_' + str(t)
                meas[1] = ''
                measured_rooms[sensor_room] = meas[0]
                self.net.add(meas)
                var.append(meas)

            parents = []
            # Check each room for incoming prob at this, and previous time instants
            for room_name, room in self.building.items():
                # Check if the room has been estimated at t-1
                if room_name + '_' + str(t-1) in var:
                    parents.append(room_name + '_' + str(t-1))
                # Check if adjacent rooms have been estimated at t-1
                for adj_room in room.connections:
                    if adj_room + '_' + str(t-1) in var:
                        parents.append(adj_room + '_' + str(t-1))
                # Check if sensor exists at t
                if room_name in measured_rooms.keys():
                    parents.append(measured_rooms[room_name])

                if len(parents) > 0:
                    # TODO: Add room inference to net. implies calculating intersection probabilities below:
                    """ P(room_t | room_(t-1)) = 1
                        P(room_t | adj_room_(t-1)) = P
                        P(room_t | sx_t) = TPR
                        P(room_t | ¬sx_t) = FPR """
                    self.net.add(room_name + '_' + str(t), parents, {})
                    var.append(room_name + '_' + str(t))

    def solve(self):
        """ Place here your code to determine the maximum likelihood solution
            returning the solution room name and likelihood
            use probability.elimination_ask() to perform probabilistic inference"""
        likelihood = 0
        highest_p_room = None

        for room in self.building.keys():
            # TODO: seems this only calculates a conditional probability depending on parents nodes
            res = probability.elimination_ask(room + ' ' + str(self.meas_cnt), ' ', self.net).show_approx()
            if likelihood <= res.prob:
                highest_p_room = room
                likelihood = res.prob

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
