from pulp import lpSum


def distances_camion(x, y, distances, c, j):
    """
    Distance parcourue par un camion c le jour j
    """
    return lpSum(2 * x[c][f][v][j] * distances[v][len(distances) - 1] +
                 y[c][f][v][j] * (distances[v][0] + distances[0][len(distances) - 1] - distances[v][len(distances) - 1])
                 for f in range(len(x[0]))
                 for v in range(len(distances))
                 )


def salary(x, y, distances, V_moy):
    alpha = 13  # Paie par l'heure
    print("in salary")
    res = 0
    for c in range(len(x)):
        for j in range(len(x[0][0][0])):
            res += distances_camion(x, y, distances, c, j) / V_moy
            for v in range(len(x[0][0])):
                for f in range(len(x[0])):
                    res += x[c][f][v][j]
    return res * alpha


def maintainance(n):
    return 1000 * n

def compute_quantity(semesters, ville, max_times_in_city, business_days, x, z, m, type1_max_trucks, type2_max_trucks):
    res = 0
    for f in range(max_times_in_city):
        for j in range(business_days):
            for c in range(type1_max_trucks):
                a = 1
            for c in range(type2_max_trucks):
                a = 1


def fuel(x, y, distances):
    l = 0.35  # consommation d'essence par kilomètre
    c_e = 1.5  # Prix du litre
    print("in fuel")
    return lpSum(l * c_e * distances_camion(x, y, distances, c, j)
                 for c in range(len(x))
                 for j in range(len(x[0][0][0])))


def buying_trucks(A, semesters, type1_max_trucks, type2_max_trucks):
    res = 0
    for s in semesters:
        for c in range(type1_max_trucks):
            res += A[c][s]*40000
        for c in range(type2_max_trucks):
            res += A[c][s]*50000
    return res


def selling_trucks():
    # todo
    return None