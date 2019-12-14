# IASD2
Museum fire Detection

**Explain how the problem was modelled with a Bayesian network.**

The Bayesian network is constructed in "time-layers", with each layer representing a time instant of a measurement, thus having N layers, with N equaling to M, the number of time instants of measurement in the problem. In each layer, there are two types of nodes: (1) Represents the state of a room (on fire); (2) Represents the state of sensor (active). In (1), the first layer (initial state) contains the prior nodes and (1) have a probability of 0.5 since we do not have any knowledge of the room state (if it is on fire or not).

Room nodes in layer t(1) have as parent nodes the same room and all adjacent rooms in the previous time instant (layer t-1). Sensor nodes (2) have as parents the room nodes (1) they measure at that time instant. That means if a sensor does not provide a measurement in t, then it's corresponding node (2) doesn't appear in layer t. 

The truth table of (1) is as follows: if the room is on fire at the previous time instant, then the conditional probability is always 1, irrespective of the state of the other parent nodes. If at least one adjacent room is on fire, then the conditional probability is always P, irrespective of the number of adjacent rooms on fire. If none of the parent rooms are on fire, then the conditional probability is 0.

The truth table of (2) is as follows: if the room the sensor measures is on fire, then P(sensor_t | room_t) = TPR(sensor_t). Conversely, P(sensor_t | ¬ room_t) = FPR(sensor_t).

In order to calculate the room with the highest probability of being on fire on time instant T, we calculate for each room P(room_T | evidence) using variable elimination function elimination_ask(), with the evidence being the results of the measurements made during the problem.


**Perform a quantitative experimental evaluation of the performance improvement achieved by the variable elimination algorithm, when compared to the enumeration one (function enumeration_ask() of probability.py).**

Our solution to the problem using elimination_ask() can correctly solve all of the public tests in 321ms. Meanwhile, the same solution using enumeration_ask() times out. Taking a closer look at each problem being solved, we identified the following tests that the enumeration algorithm wasn't able to solve in a reasonable time: P5_1_8 , P4_1_8, P5_3_4, P3_3_8, P 5_5_4. Removing these from the test pool, elimination finishes in 243 ms while elimination finishes in 43 271 ms.

Both algorithms compute the distribution of the variable. Enumeration does this by iterating all values that the variable can have and computing the probability for each value and the evidence, that is, P(e, X=xi).  Enumerate_all() calculates P(e) recursively for each variable in the network until all variable have been checked. This results in time complexity of O(d^n). While enumeration has a top-down approach, elimination improves enumeration using a bottom-up approach. In elimination, the probabilities are computed first and then the other terms that depend on them are computed, simplifying the expression until it is in terms of only the asked variable. This is a better solution than enumeration because it saves time by marginalizing variables as soon as possible rather than at the end. This is done using factors, containing the CPT for each variable given the evidence. The algorithm, for all variables except the query variable and the evidence, takes all factors containing the given variable and replaces them by a single factor that does not depend on the variable. In the end, all variables have been called, so the required distribution is calculated multiplying all factors and normalizing. The resulting time complexity is exponential, O(2^n) to the size of the largest factor.

Further profiling the solution using enumeration we detect that enumerate_all() occupies 99.6% of run time, confirming the limitations of the elimination ask algorithm. This is further confirmed when looking at the examples it timed out, all of them having a larger amount of evidence and variable nodes compared to the other tests.
