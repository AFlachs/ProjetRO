from pulp import GLPK
from pulp import LpMinimize, LpProblem, LpStatus, lpSum, LpVariable
import introduceProblem
import numpy as np
import costs

v_moy = 70  # km/h
work_time = 8  # heures
tau = 1  # heures
delivery_waiting = 1  # heures
max_capacity_1 = 16.5  # Tonnes
max_capacity_2 = 5.5  # Tonnes
depreciation_rate = 0.2  # pas d'unité
buying_price_1 = 40000  # euros
buying_price_2 = 50000  # euros
max_trucks = 30  # nombre de camions
max_trucks_type1 = 20  # nombre max de camions de type 1
max_trucks_type2 = 10  # nombre max de camions de type 2
max_times_in_city = 3  # nombre de fois max qu'un camion peut passer dans une ville par jour
business_days = 1270  # nombre de jours
distances = introduceProblem.introduce_distances()
requests = introduceProblem.introduce_city_requests()
cities_number = 6
transport_types = introduceProblem.introduce_truck_types()
semesters = introduceProblem.introduce_semesters()
semesters_number = len(semesters)
selling_cost = introduceProblem.introduce_selling_cost(depreciation_rate, buying_price_1,
                                                       buying_price_2)  # cost[type][age]

# TODO : introduce variables

pos = list(list())  # pos_cs -> camion possédé ou non,

#### PAS A NOUS #####
model = LpProblem(name="Demo", sense=LpMinimize)

x = [[[[LpVariable('x_{c},{f},{v},{j}', cat='Binary') for j in range(business_days)]
       for v in range(cities_number)]
      for f in range(max_times_in_city)]
     for c in range(max_trucks)
     ]  # x_cf^vj

y = [[[[LpVariable('y_{c},{f},{v},{j}', cat='Binary') for j in range(business_days)]
       for v in range(cities_number)]
      for f in range(max_times_in_city)]
     for c in range(max_trucks)
     ]  # x_cf^vj

p = [[LpVariable('p_{c},{j}', cat='Binary') for j in range(business_days)] for c in range(max_trucks)]

V = [[[LpVariable('V_{c},{s},{a}', cat='Binary')
       for a in range(semesters_number)]
      for s in range(semesters_number)]
     for c in range(max_trucks)]

z = [[[[LpVariable('z_{c},{f},{v},{j}', cat='Binary') for j in range(business_days)]
       for v in range(cities_number)]
      for f in range(max_times_in_city)]
     for c in range(max_trucks)
     ]
# print(x)
for c in range(max_trucks):
    for j in range(business_days):
        for f in range(max_times_in_city):
            for v in range(cities_number):
                model += (y[c][f][v][j] <= x[c][f][v][j],
                          'Produit de binaires (a) {},{},{},{}'.format(str(c), str(f), str(v), str(j)))
                model += (y[c][f][v][j] <= x[c][f][cities_number - 1][j],
                          'Produit de binaires (b) {},{},{},{}'.format(str(c), str(f), str(v),
                                                                       str(j)))  # indice d'anvers
                model += (y[c][f][v][j] >= x[c][f][v][j] + x[c][f][cities_number - 1][j] - 1,
                          'Produit de binaires (c) {},{},{},{}'.format(str(c), str(f), str(v), str(j)))

                # model += (x[c][f][v][j] >=)
                model += (z[c][f][v][j] >= p[c][j] + x[c][f][v][j] - 1,
                          'Produit de binaires x et p (a) {},{},{},{}'.format(str(c), str(f), str(v), str(j)))
                model += (z[c][f][v][j] <= 0.5 * (p[c][j] + x[c][f][v][j]),
                          'Produit de binaires x et p (b) {},{},{},{}'.format(str(c), str(f), str(v), str(j)))

        # Temps de travail inférieur à worktime
        model += (costs.distances_camion(x, y, distances, c, j) - 1 + tau * lpSum(x[c][f][v][j]
                                                                                  for f in range(max_times_in_city)
                                                                                  for v in
                                                                                  range(cities_number)) <= work_time,
                  'Travail journalier {},{}'.format(str(c), str(j)))
for j in range(business_days):
    for f in range(max_times_in_city):
        for c1 in range(max_trucks_type1):
            model += (lpSum(x[c1][f][v][j]
                            for v in range(cities_number)) <= 1)
        for c2 in range(max_trucks_type1, max_trucks_type2):
            model += (lpSum(x[c2][f][v][j]
                            for v in range(cities_number-1)) <= 1) #on fait la boucle sur toutes les villes sauf Anvers


model += costs.salary(x, y, distances, v_moy) + costs.maintainance(x, semesters) + costs.fuel(x, distances,
                                                                                              y), 'Objective Function '

status = model.solve(solver=GLPK(msg=True, keepFiles=True), timeLimit=300)
