import numpy as np

cities_list = [ "Anvers", "Charleroi", "Gand", "Bruxelles", "Hasselt", "Liege"]


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
    return


def introduce_semesters():
    return None


def introduce_truck_types():
    return None


def introduce_selling_cost():
    return None