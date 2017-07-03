from recommendations import Recommendation
from critics_movies import critics

# Data structures:
#           feature 1   feature 2 ...
#   item1     3.0         4.5     ...
#   item2     2.5         5.0     ...
# Class Recommendation could calculate the similarity between users
#                                  and the similarity between features
# If you transpose the data set, the features seem as item, then items are features.
class RecommendationBaseItems(object):
    def __init__(self, items_data, similarity_method = "sim_pearson"): 
        self.recommend_based_item = Recommendation(items_data, similarity_method = similarity_method)
        self.recommend_based_feature =  Recommendation(self.transform_data(items_data), similarity_method = similarity_method)
        self.update_sim_features()           
            
    def transform_data(self, items_data):
        result = {}

        for item in items_data:
            for feature in items_data[item]:
                result.setdefault(feature, {})
                result[feature][item]= items_data[item][feature]

        return result

    def update_sim_features(self, num = 10):
        result = {}

        c = 0
        for feature in self.recommend_based_feature.items_data:
            c += 1
            if c%100 == 0: print "%d / %d" % (c, len(self.recommend_based_feature.items_data))
            scores = self.recommend_based_feature.top_matches(feature, num = num)
            result[feature] = scores

        self.features_match = result

    def set_similarity_calculator(self, similarity_method):
        self.recommend_based_item.set_similarity_calculator(similarity_method)
        self.recommend_based_feature.set_similarity_calculator(similarity_method)

    def top_matches(self, feature_id, num = 5):
        return self.recommend_based_feature.top_matches(feature_id, num = num)

    def get_recommendations(self, feature_id):
        return self.recommend_based_feature.get_recommendations(feature_id)

    
    def get_recommended_items(self, item_id, update = False, num = 5):        
        itemRatings = self.recommend_based_item.items_data[item_id]
        scores = {}
        totalSim = {}

        if update:
            self.update_sim_features(num = num)

        for (feature, rating) in itemRatings.items():
            for (similarity, feature_1) in self.features_match[feature]:
                if feature_1 in itemRatings: continue

                scores.setdefault(feature_1, 0)
                scores[feature_1] += similarity * rating

                totalSim.setdefault(feature_1, 0)
                totalSim[feature_1] += similarity

        try:
            rankings = [ (score/totalSim[f], f) for f, score in scores.items() if score != 0]
        except ZeroDivisionError:
            print it

        rankings.sort()
        rankings.reverse()
        return rankings


if __name__ == '__main__':

    recommend = RecommendationBaseItems(critics)
    print recommend.get_recommendations('Just My Luck')
    print recommend.get_recommended_items("Toby")

    print "sim_distance"
    recommend.set_similarity_calculator("sim_distance")
    print recommend.get_recommended_items("Toby", update = True)