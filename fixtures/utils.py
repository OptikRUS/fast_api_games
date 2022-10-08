import json


def save_data(filename, data):
    with open(filename) as file:
        all_data = json.load(file)
    with open(filename, 'w') as file:
        item = json.loads(data.json())
        all_data.append(item)
        json.dump(all_data, file)
