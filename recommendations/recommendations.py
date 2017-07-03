from critics_movies import critics

from similarity import Similarity
from sim_distance import SimDistance
from sim_pearson import SimPearson
from sim_tanimoto import SimTanimoto

# Data structures:
#           feature 1   feature 2 ...
#   item1     3.0         4.5     ...
#   item2     2.5         5.0     ...
# Class Recommendation could calculate the similarity between users
#                                  and the similarity between features
# If you transpose the data set, the features seem as item, then items are features.
class Recommendation(object):
    def __init__(self, items_data, similarity_method = "sim_pearson"):
        self.similarity_calculator = Similarity()
        self.set_similarity_calculator(similarity_method)        
        self.items_data = items_data     

    #If one item is rated by only one user
    # Or this user only rated one item,
    # the simularity will be significantly affected 
    # such as "User1" rated "Movie1" with 3.0.
    # And "User2" also gave 3.0 to "Movie1"
    # So the similarity between "User1" and "User2" is 1.
    # It is possible, but not that much.
    # Another example, 
    # The movie1 is rated by only User 1.
    # So, when calculating the similarity about movie1, only those ones are 
    # rated by the same user. Because other users never gave points on this movie.
    # If the user1 gave same points on many movies, then they will have 1.0 on 
    # similarity.
    def filter_only_one_rating(self):
        for (item, value) in self.items_data.items():
            if len(value) == 1:
                print "There is one item", item, " only rated one feature, so move it out"
                del self.items_data[item]

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
        elif similarity_method.lower() == "sim_tanimoto":
            self.similarity_calculator = SimTanimoto()
        else:
            raise Exception("So far, there are 3 similarity calculation methods:" + \
                            "sim_distance, sim_pearson and sim_tanimoto") 

    def top_matches(self, item_id, num = 5):
            # When there are millions lots of data would cost much memory        
        scores = [ (self.cal_sim_between_2_items(item_id, another_id), another_id)  \
                                                for another_id in self.items_data if another_id != item_id]
        scores.sort()
        scores.reverse()
        return scores[0:num]

    def get_recommendations(self, item_id):
        totals = {}
        sim_sums = {}

        for other_id in self.items_data:
            if other_id == item_id: continue

            sim = self.cal_sim_between_2_items(item_id, other_id)

            # Ignore the one of similarity less than 0
            if sim <= 0: continue

            for feature in self.items_data[other_id]:
                if feature not in self.items_data[item_id] or self.items_data[item_id] == 0:
                    totals.setdefault(feature, 0)
                    totals[feature] += sim * self.items_data[other_id][feature]

                    sim_sums.setdefault(feature, 0)
                    sim_sums[feature] += sim

        rankings = [(total/sim_sums[feature], feature)  for feature, total in totals.items() if total > 0]
        rankings.sort()
        rankings.reverse()

        return rankings


if __name__ == '__main__':

    recommend = Recommendation(critics)
    recommend.set_similarity_calculator("sim_distance")

    print recommend.cal_sim_between_2_items("Lisa Rose", "Gene Seymour")

    recommend.set_similarity_calculator("sim_pearson")

    print recommend.cal_sim_between_2_items("Lisa Rose", "Gene Seymour")

    print recommend.top_matches("Toby", num = 3)

    recommend.set_similarity_calculator("sim_distance")
    print recommend.get_recommendations('Toby')

    # recommend_elements.set_similarity_calculator("sim_distance")


    # print "similarity between 2 movies"
    # print recommend_elements.cal_sim_between_2_items("Snakes on a Plane", "Lady in the Water")

    # print "---------------------"
    # print "recommend some commenters"
    # print recommend_elements.getRecommendations('Just My Luck')

    # print "---------------------"
    # elementMatch = recommend_elements.update_sim_elememts()

    # print recommend_elements.getRecommendedElements(critics, 'Toby')

    # print "------Tanimoto Similarity -- "
    # tanimoto = SimTanimoto()
    # print critics['Lisa Rose']
    # print critics['Toby']
    # print tanimoto.calculate_similarity(critics['Lisa Rose'], critics['Toby'])