import json
import datetime

url = "analyse_data_angular.json"


def parse_date(date):
    with open(url, 'r') as file:
        data = json.load(file)
    dic = {}

    for i in data:
        author = i['author']
        date = datetime.datetime.fromtimestamp(i['date']).strftime("%Y%m")
        if date not in dic:
            dic[date] = {}

        if author not in dic[date]:
            dic[date][author] = {}

        if i['is_broken']:
            if i['file'] not in dic[date][author]:
                dic[date][author][i['file']] = 0

            dic[date][author][i['file']] += 1

    return dic
