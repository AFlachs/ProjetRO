def distances_camion(x, y, distances, c, j):
    """
    Distance parcourue par un camion c le jour j
    """
    first_part = sum(2 * x[c][f][v][j] * distances[v][len(distances)-1]
                     for f in range(len(x[0]))
                     for v in range(len(x[0][0]))
                     )
    second_part = sum(y[c][f][v][j] * (distances[v][0] + distances[0][len(distances)-1] - distances[v][len(distances)-1])
                      for f in range(len(x[0]))
                      for v in range(len(x[0][0]))
                      )
    return first_part + second_part


def salary(x, y, distances, V_moy):
    alpha = 13  # Paie par l'heure
    return alpha * (
            sum(distances_camion(x, y, distances, c, j) / V_moy for c in range(len(x)) for j in range(len(x[0][0][0])))
            + sum(x[c][f][v][j]
                  for c in range(len(x))
                  for f in range(len(x[0]))
                  for v in range(len(x[0][0]))
                  for j in range(len(x[0][0][0]))
                  )
    )


def maintainance(n, semesters):
    return sum(1000 * n[s] for s in semesters)


def fuel(x, y, distances):
    l = 0.35    # consommation d'essence par kilomètre
    c_e = 1.5   # Prix du litre
    return sum(l * c_e * distances_camion(x, y, distances, c, j) * x[c][f][v][j]
               for c in range(len(x))
               for f in range(len(x[0]))
               for v in range(len(x[0][0]))
               for j in range(len(x[0][0][0])))
