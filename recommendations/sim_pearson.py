from similarity import Similarity
from math import sqrt

class SimPearson(Similarity):
    def calculate_similarity(self, item1, item2):
        sim = {}

        for item in item1:
            if item in item2:
                sim[item] = 1

        n = len(sim)
        if n == 0:
            return 0

        sum_item1 = sum([item1[it] for it in sim])
        sum_item2 = sum([item2[it] for it in sim])

        sum_item1_sq = sum([pow(item1[it], 2) for it in sim])
        sum_item2_sq = sum([pow(item2[it], 2) for it in sim])

        pearson_sum = sum([ item1[it]*item2[it] for it in sim ])

        num = pearson_sum - (sum_item1 * sum_item2 / n)
        den = sqrt( (sum_item1_sq - pow(sum_item1, 2)/n) * (sum_item2_sq - pow(sum_item2, 2)/n))
        if den == 0:
            return 0

        return num/den



