from recommendations import Recommendation, transform_data

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
    import time

    start = time.clock()
    print recommend.getRecommendations('87')[0:30]
    elapsed = (time.clock() - start)
    print elapsed

    recommand_elements = Recommendation(transform_data(prefs))

    recommand_elements.set_similarity_calculator("sim_distance")

    recommand_elements.update_sim_elememts()
    start = time.clock()
    print recommand_elements.getRecommendedElements(prefs, '1633')[0:30]
    elapsed = (time.clock() - start)
    print elapsed

    recommand_elements.set_similarity_calculator("sim_tanimoto")

    recommand_elements.update_sim_elememts()
    start = time.clock()
    print recommand_elements.getRecommendedElements(prefs, '1633')[0:30]
    elapsed = (time.clock() - start)
    print elapsed

