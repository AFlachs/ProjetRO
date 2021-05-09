from pulp import GLPK
from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable
import introduceProblem
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
max_times_in_city = 3  # nombre de fois max qu'un camion peut passer dans une ville par jour
business_days = 1270  # nombre de jours
distances = introduceProblem.introduce_distances()
requests = introduceProblem.introduce_city_requests()
cities = introduceProblem.introduce_cities()
transport_types = introduceProblem.introduce_truck_types()
semesters = introduceProblem.introduce_semesters()
selling_cost = introduceProblem.introduce_selling_cost(depreciation_rate, buying_price_1,
                                                       buying_price_2)  # cost[type][age]

# TODO : introduce variables
x = list(list(list(list)))  # x^cf_vj -> camion passe ou pas, x[c][f][v][j]
y = list(list(list(list)))  # y^cf_vj -> produit x_v * x_a
p = list(list)  # p_cj -> type principal transporté

#### PAS A NOUS #####
model = LpProblem(name="Demo", sense=LpMaximize)

for c in range(max_trucks):
    for j in range(business_days):
        for f in range(max_times_in_city):
            for v in cities:
                x[c][f][v][j] = LpVariable('x', cat='Binary')
                y[c][f][v][j] = LpVariable('y', cat='Binary')

                model += (y[c][f][v][j] <= x[c][f][v][j], 'Produit de binaires')
                model += (y[c][f][v][j] <= x[c][f][len(x) - 1][j], 'Produit de binaires')  # indice d'anvers
                model += (y[c][f][v][j] >= x[v] + x[len(x) - 1] - 1, 'Produit de binaires')
        p[c][j] = LpVariable('p', cat='Binary')

        # Temps de travail inférieur à worktime
        model += (costs.distances_camion(x, y, distances, c, j) - 1 + tau * lpSum(x[c][f][v][j]
                                                                                  for f in range(max_times_in_city)
                                                                                  for v in cities) <= work_time,
                  'Travail journalier')

model += costs.salary(x, y, distances, v_moy) + costs.maintainance(x, semesters) + costs.fuel(x, distances,
                                                                                              y), 'Objective Function '

status = model.solve(solver=GLPK(msg=True, keepFiles=True))
