from similarity import Similarity
from math import sqrt

class SimDistance(Similarity):
    def calculate_similarity(self, item1, item2):
        sim = []

        for item in item1:
            if item in item2:
                sim.append(pow( item1[item] - item2[item], 2))

        if len(sim) == 0:
            return 0

        sum_of_squares = sum( sim )

        return 1 / (1 + sqrt(sum_of_squares))  

