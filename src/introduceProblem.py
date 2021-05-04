import numpy as np

cities_list = [ "Anvers", "Charleroi", "Gand", "Bruxelles", "Hasselt", "Liege"]


def introduce_params():
    distances = introduce_distances()
    requests = introduce_city_requests()
    cities = introduce_cities()
    v_moy = 70                         # km/h
    work_time = 8                      # heures
    delivery_waiting = 1               # heures
    max_capacity_1 = 16.5              # Tonnes
    max_capacity_2 = 5.5               # Tonnes


def introduce_cities():
    return np.linspace(1, len(cities_list), len(cities_list))


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
    # TODO : créer un tableau ayant une dimension "temps" (il en faut 10, 1 par semestre) et une dimension
    # villes, puis le remplir correctement
    return
