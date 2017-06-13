from critics_movies import critics

from math import sqrt
def sim_distance(prefs, person1, person2):
    sim = {}

    for item in prefs[person1]:
        if item in prefs[person2]:
            sim[item] = 1

    if len(sim) == 0:
        return 0

    sum_of_squares = sum( [ pow( prefs[person1][item] - prefs[person2][item], 2) for item in sim.keys()] )

    return 1 / (1 + sqrt(sum_of_squares))


print sim_distance(critics, 'Jack Matthews', 'Mick LaSalle')