from pulp import GLPK
from pulp import LpMaximize, LpProblem, LpStatus, lpSum, LpVariable
import introduceProblem
import costs

distances = introduceProblem.introduce_distances()
requests = introduceProblem.introduce_city_requests()
cities = introduceProblem.introduce_cities()
transport_types = introduceProblem.introduce_truck_types()
semesters = introduceProblem.introduce_semesters()
selling_cost = introduceProblem.introduce_selling_cost()
v_moy = 70              # km/h
work_time = 8           # heures
delivery_waiting = 1    # heures
max_capacity_1 = 16.5   # Tonnes
max_capacity_2 = 5.5    # Tonnes


x = list(list(list(list)))   # x_vj^cf -> camion passe ou pas
p = list(list)               # p_cj -> type transporté
n = list()                   # n_s -> nombre de camions au semestre s


#### PAS A NOUS #####
model = LpProblem(name="Demo", sense=LpMaximize)

x1 = LpVariable('x_1', lowBound=0)
x2 = LpVariable('x_2', lowBound=0, cat='Continuous')
x3 = LpVariable('x_3', lowBound=0)


model += (2*x1 + x2 + x3 <= 20, 'Constraint 1')
model += (3*x1 + x2 + 2*x3 <= 30, 'Constraint 2')


model += costs.salary(x) + costs.maintainance(x) + costs.fuel(x), 'Objective Function'

status = model.solve(solver=GLPK(msg=True, keepFiles=True))
