import json

solution_file = open('solution.csv', 'w')
solution_file.write("Name;Value\n")
with open('jason_data.json') as json_file:
    data = json.load(json_file)

for p in data["variables"]:
    if p['name'][0] != 'y' and p['name'][0] != 'm' and p['name'][0] != 'z' and p['name'][0] != 'q':
        solution_file.write(p['name'] + ';' + str(p['varValue']) + "\n")
