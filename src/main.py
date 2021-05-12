from pulp import GLPK
from pulp import LpMinimize, LpProblem, lpSum, LpVariable
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
max_trucks_type1 = 20  # nombre max de camions de type 1
max_trucks_type2 = 10  # nombre max de camions de type 2
max_times_in_city = 3  # nombre de fois max qu'un camion peut passer dans une ville par jour
business_days = 1270  # nombre de jours
distances = introduceProblem.introduce_distances()
requests = introduceProblem.introduce_city_requests()  # requests[s][v]
cities_number = 6
transport_types = introduceProblem.introduce_truck_types()
semesters = introduceProblem.introduce_semesters()
semesters_number = len(semesters)
selling_cost = introduceProblem.introduce_selling_cost(depreciation_rate, buying_price_1,
                                                       buying_price_2)  # cost[type][age]

#### PAS A NOUS #####
model = LpProblem(name="Demo", sense=LpMinimize)

x = [[[[LpVariable('x_{},{},{},{}'.format(c, f, v, j), cat='Binary', lowBound=0) for j in range(business_days)]
       for v in range(cities_number)]
      for f in range(max_times_in_city)]
     for c in range(max_trucks)
     ]  # x_cf^vj

y = [[[[LpVariable('y_{},{},{},{}'.format(c, f, v, j), cat='Binary', lowBound=0) for j in range(business_days)]
       for v in range(cities_number)]
      for f in range(max_times_in_city)]
     for c in range(max_trucks)
     ]  # y_cf^vj

p = [[LpVariable('p_{},{}'.format(c, j), cat='Binary', lowBound=0) for j in range(business_days)] for c in
     range(max_trucks)]
# p_cj

#q = [[LpVariable('q_{},{}'.format(c, j), cat='Binary', lowBound=0) for j in range(business_days - 1)] for c in
#     range(max_trucks)]
# q_cj=p_cj*p_cj+1

pos = [[LpVariable('pos_{},{}'.format(str(c), str(j)), cat='Binary', lowBound=0) for j in range(business_days)] for c in
       range(max_trucks)]
# pos_cs

V = [[[LpVariable('V_{},{},{}'.format(c, s, a), cat='Binary', lowBound=0)
       for a in range(semesters_number)]
      for s in range(semesters_number)]
     for c in range(max_trucks)]
# V_cas
A = [[LpVariable('A_{}{}'.format(str(c), str(s))) for s in semesters] for c in range(max_trucks)]
# A_cs

m = [[[[LpVariable('m_{},{},{},{}'.format(c, f, v, j), cat='Binary', lowBound=0) for j in range(business_days)]
       for v in range(cities_number)]
      for f in range(max_times_in_city)]
     for c in range(max_trucks)
     ]
# m_cf^vj

z = [[[[LpVariable('z_{},{},{},{}'.format(c, f, v, j), cat='Binary', lowBound=0) for j in range(business_days)]
       for v in range(cities_number)]
      for f in range(max_times_in_city)]
     for c in range(max_trucks)
     ]
# z_cf^vj
print('Nobody Expects Spanish Inquisition')

for c in range(max_trucks):
    for j in range(business_days):
        s = j % (business_days // len(semesters))  # Semestre actuel
        for f in range(max_times_in_city):
            for v in range(cities_number):
                model += (y[c][f][v][j] >= x[c][f][v][j] + x[c][f][0][j] - 1,
                          'Prod bin (a) {},{},{},{}'.format(str(c), str(f), str(v), str(j)))
                model += (y[c][f][v][j] <= 0.5 * (x[c][f][v][j] + x[c][f][0][j]),
                          'Prod bin (b) {},{},{},{}'.format(str(c), str(f), str(v),
                                                            str(j)))  # 0 est l'indice d'anvers

                model += pos[c][s] >= x[c][f][v][j]

                model += (z[c][f][v][j] >= p[c][j] + x[c][f][v][j] - 1,
                          'Prod bin x, p (a) {},{},{},{}'.format(str(c), str(f), str(v), str(j)))
                model += (z[c][f][v][j] <= 0.5 * (p[c][j] + x[c][f][v][j]),
                          'Prod bin x, p (b) {},{},{},{}'.format(str(c), str(f), str(v), str(j)))
                model += (m[c][f][v][j] >= p[c][j] + y[c][f][v][j] - 1,
                          'Prod bin y, p (a) {},{},{},{}'.format(str(c), str(f), str(v), str(j)))
                model += (m[c][f][v][j] <= 0.5 * (p[c][j] + y[c][f][v][j]),
                          'Prod bin y, p  (b) {},{},{},{}'.format(str(c), str(f), str(v), str(j)))

        #if j > 0:
        #    if j < business_days - 2:
        #        model += (1 >= lpSum(x[c][f][v][jp] for jp in range(j, j + 3) for f in range(max_times_in_city)
        #                             for v in range(cities_number)) / (3 * max_times_in_city * cities_number)
        #                  + p[c][j] + p[c][j - 1] - 2 * q[c][j - 1])
        #    else:
        #        model += p[c][j] >= p[c][j - 1]
        #        model += p[c][j] <= p[c][j - 1]
        #if j < business_days - 1:
        #    model += q[c][j] >= p[c][j] + p[c][j + 1] - 1
        #    model += q[c][j] <= 0.5 * (p[c][j] + p[c][j + 1])

        # Temps de travail inférieur à worktime
        model += (costs.distances_camion(x, y, distances, c, j) - 1 + tau * lpSum(x[c][f][v][j]
                                                                                  for f in range(max_times_in_city)
                                                                                  for v in
                                                                                  range(cities_number)) <= work_time,
                  'WorkTime {},{}'.format(str(c), str(j)))


    print("Camion : " + str(c))

for j in range(business_days):
    for f in range(max_times_in_city):
        for c1 in range(max_trucks_type1):
            model += (lpSum(x[c1][f][v][j]
                            for v in range(cities_number)) <= 1)  # Une ville par passage pour type 1
        for c2 in range(max_trucks_type1, max_trucks_type2):
            model += (lpSum(x[c2][f][v][j]
                            for v in  # Max une ville pour type 2 sans compter Anvers
                            range(1, cities_number)) <= 1)  # on fait la boucle sur toutes les villes sauf Anvers

for s in semesters:
    for v in range(cities_number):
        # quantity(v, s, x, p, y) >= requests[s][v] #TODO
        a = 1

    # Contraintes vente :
    for c in range(max_trucks):
        model += A[c][s] <= 0.5 * (pos[c][s] + 1 - pos[c][s - 1])
        model += A[c][s] >= pos[c][s] - pos[c][s - 1]
        for a in range(len(V[0])):
            if s - a - 1 >= 0:
                for i in range(s - a, s):
                    model += V[c][a][s] <= pos[c][i]
                model += V[c][a][s] <= 1 - pos[c][s]
                model += V[c][a][s] <= 1 - pos[c][s - a - 1]
                model += V[c][a][s] >= lpSum(pos[c][i] for i in range(s - a, s)) - pos[c][s] - a + 1
    for c1 in range(1,max_trucks_type1):
        model += pos[c1][s] <= pos[c1 - 1][s]
    for c2 in range(max_trucks_type1+1, max_trucks_type2):
        model += pos[c2][s] <= pos[c2 - 1][s]

print("Initialisation terminée")

model += costs.salary(x, y, distances, v_moy) + costs.maintainance(
    sum(pos[c][s] for c in range(max_trucks) for s in semesters)) + costs.fuel(x, y, distances,
                                                                               ), 'Objective Function '

input("Press enter")
print("Solving")

status = model.solve(solver=GLPK(msg=True, keepFiles=True, timeLimit=450))
