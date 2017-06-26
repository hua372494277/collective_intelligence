from similarity import Similarity

class SimTanimoto(Similarity):
    def calculate_similarity(self, item1, item2):
        intersection = 0
        for item in item1:
            if item in item2:
                intersection += 1

        return (intersection / (len(item1) + len(item2) - intersection))
