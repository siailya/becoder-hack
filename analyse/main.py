import datetime
import json

url = "analyse_data_angular.json"


def parse_data(data, return_tuple=False):
    dic_total = {}
    dic_broken = {}
    dic_not_broken = {}

    for i in data:
        author = i['author']
        date = datetime.datetime.fromtimestamp(i['date']).strftime("%Y%m")
        if date not in dic_broken:
            dic_broken[date] = {}
            dic_not_broken[date] = {}
            dic_total[date] = {}

        if author not in dic_broken[date]:
            dic_broken[date][author] = {}
            dic_not_broken[date][author] = {}
            dic_total[date][author] = {}

        if i['file'] not in dic_total[date][author]:
            dic_total[date][author][i['file']] = 0
        dic_total[date][author][i['file']] += 1

        if i['is_broken']:
            if i['file'] not in dic_broken[date][author]:
                dic_broken[date][author][i['file']] = 0

            dic_broken[date][author][i['file']] += 1
        else:
            if i['file'] not in dic_not_broken[date][author]:
                dic_not_broken[date][author][i['file']] = 0

            dic_not_broken[date][author][i['file']] += 1

    if return_tuple:
        return dic_total, dic_broken, dic_not_broken

    return dic_broken


def sort_author_files_time_group(dic, author, file):
    dic_author_file = {}

    for date in dic:
        dic_author_file[date] = 0
        for a in dic[date]:
            if a == author:
                for f in dic[date][author]:
                    if f == file:
                        dic_author_file[date] += dic[date][author][f]

    return dic_author_file


def sort_author_files_total(data, author, file):
    res = 0
    for f in data:
        if f['author'] == author and f['file'] == file:
            res += 1

    return res


def sort_author_files_not_broken(data, author, file):
    res = 0
    for f in data:
        if f['author'] == author and f['file'] == file and not f['is_broken']:
            res += 1

    return res


def get_files_broken(data):
    res = {}

    for file in data:
        if file['is_broken']:
            if file['file'] not in res:
                res[file['file']] = 0
            res[file['file']] += 1

    return res


def get_authors_broken(data):
    res = {}

    for file in data:
        if file['is_broken']:
            if file['author'] not in res:
                res[file['author']] = 0
            res[file['author']] += 1

    return res


def get_authors_files_broken(data):
    res = {}

    for file in data:
        if file['is_broken']:
            af = file['author'] + "_" + file['file']
            if af not in res:
                res[af] = 0
            res[af] += 1

    return res


def get_author_file_broke_dates(author, file):
    with open(url, 'r') as filein:
        data = json.load(filein)

    res = []

    for f in data:
        if f['author'] == author and f['file'] == file and f['is_broken']:
            res.append(f['date'])

    return res


if __name__ == '__main__':
    with open(url, 'r') as read_file:
        main_data = json.load(read_file)

    total_dic, broken_dict, not_broken_dict = parse_data(main_data, return_tuple=True)

    broken_file = sort_author_files_time_group(broken_dict, "Alex Rickabaugh",
                                               "packages/compiler-cli/test/ngtsc/ngtsc_spec.ts")
    work_file = sort_author_files_time_group(not_broken_dict, "Alex Rickabaugh",
                                             "packages/compiler-cli/test/ngtsc/ngtsc_spec.ts")
    total_file = sort_author_files_time_group(total_dic, "Alex Rickabaugh",
                                              "packages/compiler-cli/test/ngtsc/ngtsc_spec.ts")
    print(total_file)
    import matplotlib.pyplot as plt

    fig = plt.figure()
    ax = fig.add_axes([0, 0, 1, 1])
    langs = total_file.keys()
    students = total_file.values()
    ax.bar(langs, students)
    plt.show()

    # # print(parse_date(url))
    #
    # broken_files = get_files_broken()
    # # sort by value
    # broken_files = {k: v for k, v in sorted(broken_files.items(), key=lambda item: item[1], reverse=True)}
    # # print(broken_files)
    # broken_authors = get_authors_broken()
    # # sort by value
    # broken_authors = {k: v for k, v in sorted(broken_authors.items(), key=lambda item: item[1], reverse=True)}
    # # print(broken_authors)
    #
    # broken_authors_files = get_authors_files_broken()
    # # sort by value
    # broken_authors_files = {k: v for k, v in
    #                         sorted(broken_authors_files.items(), key=lambda item: item[1], reverse=True)}
    #
    # for i in list(broken_authors_files.keys())[0:10]:
    #     print(broken_authors_files[i], i)
