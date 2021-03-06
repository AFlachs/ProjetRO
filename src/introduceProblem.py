import numpy as np
import math

cities_list = ["Anvers", "Charleroi", "Gand", "Bruxelles", "Hasselt", "Liege"]


def introduce_distances():
    distances = np.array(
        [   # Anvers    Charleroi   Gand    Bruxelles   Hasselt     Liege
            [0,        100,        40,     45,         50,         105],
            [0,        0,          100,    60,         80,         100],
            [0,        0,          0,      40,         60,         140],
            [0,        0,          0,      0,          50,         100],
            [0,        0,          0,      0,          0,          60 ],
            [0,        0,          0,      0,          0,          0  ],
        ]
    )
    distances += distances.transpose()
    return distances


def introduce_city_requests():
    # Tableau ayant une dimension "temps" (il en faut 10, 1 par semestre) et une dimension
    # villes, puis le remplir correctement
    city_requests = np.array(
        [   # Anvers    Charleroi   Gand    Bruxelles   Hasselt     Liege
            [0,         0,          0,      0,          0,          0],
            [0,         0,          0,      0,          0,          0],
            [9000,      12000,      2000,   6200,       350,        30000],
            [9000,      12000,      2000,   6200,       1650,       30000],
            [18000,     24000,      4000,   12400,      2000,       60000],
            [18000,     24000,      4000,   12400,      2000,       60000],
            [27000,     36000,      6000,   18600,      2350,       90000],
            [27000,     36000,      6000,   18600,      2350,       90000],
            [36000,     48000,      8000,   24800,      2700,       120000],
            [36000,     48000,      8000,   24800,      2700,       120000],
            [45000,     60000,      10000,  31000,      3050,       150000],
        ]
    )
    return city_requests


def introduce_semesters():
    semesters = np.array(
        [0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    )
    return semesters


def introduce_truck_types():
    truck_types = np.array(
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
         1, 1, 1, 1, 1, 1, 1, 1, 1, 1,
         2, 2, 2, 2, 2, 2, 2, 2, 2, 2]
    )
    return truck_types


def introduce_selling_cost(d_r, b_p_1, b_p_2):
    selling_cost = np.array(
        [
            # camion de type 1
            [math.pow(b_p_1/(1+d_r), i/2) for i in range(10)] + [ math.pow(b_p_1/(1+d_r), 5) ],
            # camion de type 2
            [math.pow(b_p_2/(1+d_r), i/2) for i in range(10)] + [ math.pow(b_p_2/(1+d_r), 5) ]
        ]
    )
    return selling_cost