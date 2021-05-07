from pulp import GLPK
from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable
import introduceProblem
import costs


v_moy = 70              # km/h
work_time = 8           # heures
delivery_waiting = 1    # heures
max_capacity_1 = 16.5   # Tonnes
max_capacity_2 = 5.5    # Tonnes
depreciation_rate = 0.2 #pas d'unité
buying_price_1 = 40000  #euros
buying_price_2 = 50000  #euros
max_trucks = 30         # nombre de camions
max_times_in_city = 3   # nombre de fois max qu'un camion peut passer dans une ville par jour
business_days = 1270    # nombre de jours
distances = introduceProblem.introduce_distances()
requests = introduceProblem.introduce_city_requests()
cities = introduceProblem.introduce_cities()
transport_types = introduceProblem.introduce_truck_types()
semesters = introduceProblem.introduce_semesters()
selling_cost = introduceProblem.introduce_selling_cost(depreciation_rate, buying_price_1, buying_price_2)


# TODO : introduce variables
x = list(list(list(list)))   # x_vj^cf -> camion passe ou pas, x[c][f][v][j]
y = list(list(list(list)))   # y_vj^cf -> produit x_v * x_a
p = list(list)               # p_cj -> type transporté
n = list()                   # n_s -> nombre de camions au semestre s


#### PAS A NOUS #####
model = LpProblem(name="Demo", sense=LpMaximize)

x = [LpVariable('x_vj^cf', lowBound=0, cat='Binary')
        for c in range(max_trucks)
        for f in range(max_times_in_city)
        for v in range(len(cities))
        for j in range(business_days)]
y = [LpVariable('y', lowBound=0, cat='Binary')
        for c in range(max_trucks)
        for f in range(max_times_in_city)
        for v in range(len(cities))
        for j in range(business_days)]
p = [LpVariable('p', lowBound=1, upBound=2, cat='Integer')
        for c in range(max_trucks)
        for j in range(business_days)]

n=LpVariable('n', lowBound=0, upBound=max_trucks)


model += (2*x1 + x2 + x3 <= 20, 'Constraint 1')
model += (3*x1 + x2 + 2*x3 <= 30, 'Constraint 2')


for c in range(len(y)):
    for f in range(len(y[0])):
        for v in range(len(y[0][0])):
            for j in range(len(y[0][0][0])):
                model += (y[c][f][v][j] <= x[c][f][v][j], 'Produit de binaires')
                model += (y[c][f][v][j] <= x[c][f][len(x)-1][j], 'Produit de binaires')  # indice d'anvers
                model += (y[c][f][v][j] >= x[v] + x[len(x)-1] - 1, 'Produit de binaires')


model += costs.salary(x, distances) + costs.maintainance(x) + costs.fuel(x), 'Objective Function'

status = model.solve(solver=GLPK(msg=True, keepFiles=True))
