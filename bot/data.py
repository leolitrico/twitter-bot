import datetime
import pathlib

FORMAT = "%Y-%m-%d"
FILENAME = str(pathlib.Path(__file__).parent.absolute()) + "/data.csv"

def load_data():
    output = [] 
    with open(FILENAME, 'r') as file:
        list = file.read().splitlines()
        for i, elem in enumerate(list):
            elem = elem.split(',')
            output[i] = elem[0], datetime.datetime.strptime(elem[1], FORMAT)
    return output

def store_data(data):
    with open(FILENAME, 'w') as file:
        for pair in data:
            name, date = pair
            file.write(name + ',' + date.strftime(FORMAT) + '\n')

def contains(data, name):
    for pair in data:
        if pair[0] == name:
            return True
    return False

def remove_before(data, date):
    output = []
    for pair in data:
        if pair[1] < date:
            output.append(data.pop(pair))
    return output