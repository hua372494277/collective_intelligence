from critics_movies import critics

from similarity import Similarity
from sim_distance import SimDistance
from sim_pearson import SimPearson

class Recommendation(object):
    def __init__(self, items_data, similarity_method = "sim_pearson"):
        self.similarity_calculator = Similarity()
        self.set_similarity_calculator(similarity_method)        
        self.items_data = items_data


    def similarity_between_2_items(self, item_id_1, item_id_2):
        if item_id_1 not in self.items_data or item_id_2 not in self.items_data:
            raise Exception(str(item_id_1) + ' or ' + str(item_id_2) + ' is not existed in data')

        return self.similarity_calculator.calculate_similarity(self.items_data[item_id_1], \
                                                               self.items_data[item_id_2])
    
    def set_similarity_calculator(self, similarity_method):
        if similarity_method.lower() == "sim_pearson":
            self.similarity_calculator = SimPearson()
        elif similarity_method.lower() == "sim_distance":
            self.similarity_calculator = SimDistance()
        else:
            raise Exception("So far, there are 2 similarity calculation methods: sim_distance and sim_pearson")

    def topMatches(self, item_id, num = 5):
        # avoid lots of data would cost much memory
        min_similarity
        
        scores = [ (self.similarity_between_2_items(item_id, another_id), another_id)  \
                                                for another_id in self.items_data if another_id != item_id])

        scores.sort()
        scores.reverse()
        return scores[0:n]


if __name__ == '__main__':
    person1 = critics['Lisa Rose']
    person2 = critics['Gene Seymour']

    print person1
    print person2 

    sim = SimPearson()
    print sim.calculate_similarity(person1, person2)

    recommend = Recommendation(critics)
    print recommend.similarity_between_2_items('Lisa Rose', 'Gene Seymour')

    sim = SimDistance()
    print sim.calculate_similarity(person1, person2)
    recommend.set_similarity_calculator("Sim_distance")
    print recommend.similarity_between_2_items('Lisa Rose', 'Gene Seymour')


    recommend.set_similarity_calculator("sim_distance")

