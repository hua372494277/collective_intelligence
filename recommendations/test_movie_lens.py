from recommendations import Recommendation
from recommend_base_items import RecommendationBaseItems

def load_movies_lens(path=""):
    # get the info of movies
    movies = {}
    for line in open(path + "\u.item"):
        (id, title) = line.split("|")[0:2]
        movies[id] = title

    prefs = {}
    for line in open(path + "\u.data"):
        (user, movie_id, rating, ts) = line.split("\t")
        prefs.setdefault(user, {})
        prefs[user][movies[movie_id]] = float(rating)

    return prefs

if __name__ == '__main__':
    prefs = load_movies_lens("C:\\Users\\huab\\Downloads\\ml-100k\\ml-100k")
    recommend = Recommendation(prefs)
    rec_base_item = RecommendationBaseItems(prefs)
    
    import time
    start = time.clock()
    print recommend.get_recommendations('87')[0:30]
    elapsed = (time.clock() - start)
    print elapsed

    #print recommend_elements
    start = time.clock()
    print rec_base_item.get_recommended_items("87", update = True, num = 50)[0:30]
    elapsed = (time.clock() - start)
    print elapsed
    
    rec_base_item.set_similarity_calculator("sim_distance")
    start = time.clock()
    print rec_base_item.get_recommended_items("87", update = True, num = 50)[0:30]
    elapsed = (time.clock() - start)
    print elapsed
    
    print "recommend Ripe (1996)"
    start = time.clock()
    print rec_base_item.get_recommendations('Ripe (1996)')[0:30]
    elapsed = (time.clock() - start)
    print elapsed

    rec_base_item.set_similarity_calculator("sim_tanimoto")
    start = time.clock()
    print rec_base_item.get_recommended_items("87", update = True, num = 50)[0:30]
    elapsed = (time.clock() - start)
    print elapsed

    rec_base_item.features_match["Brother's Kiss, A (1997)"]

    rec_base_item.get_recommended_items("87")

    for (feature, rating) in itemRating.items():
        for (similarity, feature_1) in rec_base_item.features_match[feature]:
            if feature_1 in itemRating: continue
            scores.setdefault(feature_1, 0)
            scores[feature_1] += similarity * rating
            totalSim.setdefault(feature_1, 0)
            totalSim[feature_1] += similarity


    for user in rec_base_item.recommend_based_item.items_data.keys():
        result = rec_base_item.get_recommended_items(user)
        if len(result) > 1:
            print user, result

