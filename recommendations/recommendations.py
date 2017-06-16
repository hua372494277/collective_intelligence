from critics_movies import critics

from similarity import Similarity
from sim_distance import SimDistance
from sim_pearson import SimPearson

class Recommendation(object):
    def __init__(self, items_data, similarity_method = "sim_pearson"):
        self.similarity_calculator = Similarity()
        self.set_similarity_calculator(similarity_method)        
        self.items_data = items_data


    def cal_sim_between_2_items(self, item_id_1, item_id_2):
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
        # When there are millions lots of data would cost much memory        
        scores = [ (self.cal_sim_between_2_items(item_id, another_id), another_id)  \
                                                for another_id in self.items_data if another_id != item_id]

        scores.sort()
        scores.reverse()
        return scores[0:num]

    def getRecommendations(self, item_id):
        totals = {}
        sim_sums = {}

        for other_id in self.items_data:
            if other_id == item_id: continue

            sim = self.cal_sim_between_2_items(item_id, other_id)

            # Ignore the one of similarity less than 0
            if sim <= 0: continue

            for element in self.items_data[other_id]:
                if element not in self.items_data[item_id] or self.items_data[item_id] == 0:
                    totals.setdefault(element, 0)
                    totals[element] += sim * self.items_data[other_id][element]

                    sim_sums.setdefault(element, 0)
                    sim_sums[element] += sim

        rankings = [(total/sim_sums[element], element)  for element, total in totals.items()]
        rankings.sort()
        rankings.reverse()

        return rankings

    

def transformData(prefs):
    result = {}

    for item in prefs:
        for element in prefs[item]:
            result.setdefault(element, {})
            result[element][item]= prefs[item][element]

    return result



if __name__ == '__main__':
    person1 = critics['Lisa Rose']
    person2 = critics['Gene Seymour']

    print person1
    print person2 

    sim = SimPearson()
    print sim.calculate_similarity(person1, person2)

    recommend = Recommendation(critics)
    print recommend.cal_sim_between_2_items('Lisa Rose', 'Gene Seymour')

    sim = SimDistance()
    print sim.calculate_similarity(person1, person2)
    recommend.set_similarity_calculator("Sim_distance")
    print recommend.cal_sim_between_2_items('Lisa Rose', 'Gene Seymour')


    recommend.set_similarity_calculator("sim_pearson")

    print recommend.topMatches('Toby', num = 5)

    print recommend.getRecommendations('Toby')

    recommend.set_similarity_calculator("sim_distance")
    print recommend.getRecommendations('Toby')

    print "------------------"
    recommend = Recommendation( transformData(recommend.items_data))

    print recommend.topMatches('Superman Returns')
    recommend.set_similarity_calculator("sim_pearson")
    print recommend.getRecommendations('Just My Luck')
    print "similarity between 2 movies"
    print recommend.cal_sim_between_2_items("Snakes on a Plane", "Lady in the Water")

    print "---------------------"
    print "recommend some commenters"
    print recommend.getRecommendations('Just My Luck')
