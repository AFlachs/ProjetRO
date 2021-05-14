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


def compute_qtt_liege(max_times_in_city, business_days, x, z, type1_max_trucks, type2_max_trucks):
    res = 0
    for f in range(max_times_in_city):
        for j in range(business_days):
            for c in range(type1_max_trucks):
                res += 16.5 * z[c][f][0][j]
            for c in range(type2_max_trucks):
                    res += 5.5 * x[c][f][0][j] - 11 * z[c][f][0][j]
    return res


def compute_qtt_anvers(max_times_in_city, business_days, x, y, z, m, type1_max_trucks, type2_max_trucks):
    res = 0
    for f in range(max_times_in_city):
        for j in range(business_days):
            for c in range(type1_max_trucks):
                res += 16.5 * x[c][f][0][j] - 16.5 * z[c][f][0][j]
            for c in range(type2_max_trucks):
                res += 16.5 * x[c][f][0][j] - 11 * z[c][f][0][j] - lpSum(16.5*y[c][f][v][j] - 11*m[c][f][v][j]
                                                                         for v in range(1, 6))
    return res


def compute_quantity(ville, max_times_in_city, business_days, x, y, z, m, type1_max_trucks, type2_max_trucks):
    res = 0
    if ville == 0:
        res = compute_qtt_anvers(max_times_in_city, business_days, x, y, z, m, type1_max_trucks, type2_max_trucks)
    elif ville == 5:
        res = compute_qtt_liege(max_times_in_city, business_days, x, z, type1_max_trucks, type2_max_trucks)
    else:
        for f in range(max_times_in_city):
            for j in range(business_days):
                for c in range(type1_max_trucks):
                    res += 16.5*x[c][f][ville][j] - 16.5*z[c][f][ville][j]
                for c in range(type2_max_trucks):
                    res += 16.5*x[c][f][ville][j] - 11*z[c][f][ville][j]
    return res


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


def selling_trucks(V, semesters, type1_max_trucks, type2_max_trucks, prix_vente):
    res = 0
    for a in range(1, len(semesters) - 1):
        for s in range(a+1, len(semesters)):
            for c in range(type1_max_trucks):
                res += prix_vente[0][a] * V[c][a][s]
            for c in range(type2_max_trucks):
                res += prix_vente[1][a] * V[c][a][s]
    return res