import datetime
import json

url = "analyse_data_angular.json"


def parse_data():
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


def sort_person_file(dic, author, file):
    dic_author_file = {}
    for i in dic:
        dic_author_file[i] = 0
        for a in dic[i]:
            if a == author:
                for f in dic[i][author]:
                    if f == file:
                        dic_author_file[i] += 1
    return dic_author_file

if __name__ == '__main__':
    main_data = parse_data()
    # print(main_data)
    print(sort_person_file(main_data, "Alex Rickabaugh", "packages/compiler-cli/test/ngtsc/ngtsc_spec.ts"))
