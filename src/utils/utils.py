import json
import requests


# function to save HTML text to a file
def saveHTML(name, res):
    with open(name + '.html', 'w') as file:
        file.write(res.text)


# function to save json text to a file
def saveJSON(name, data):
    with open(name + '.json', 'w') as file:
        json.dump(data, file, indent=4)


# function to print the history of a request
def printHistory(res):
    for i in res.history:
        print(i.status_code, i.url)
    print(res.url)


def saveJSON(name, data):
    with open(name + '.json', 'w') as file:
        json.dump(data, file, indent=4)
