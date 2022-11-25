import datetime
import json

import matplotlib.pyplot as plt


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

    # Remove empty dates at start and end
    while list(dic_author_file.values())[0] == 0:
        del dic_author_file[list(dic_author_file.keys())[0]]

    while list(dic_author_file.values())[-1] == 0:
        del dic_author_file[list(dic_author_file.keys())[-1]]

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
            af = file['author'] + "\n" + file['file']
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


def plot_data(total, broken, work, title, broken_count):
    fig, ax = plt.subplots()

    ax.plot(total.keys(), total.values(), alpha=0.4, color='g', label="Total")
    ax.plot(broken.keys(), broken.values(), alpha=0.4, color='r', label="Broken")
    ax.plot(work.keys(), work.values(), alpha=0.4, color='b', label="Not broken")

    ax.legend()
    ax.set_xlabel("Date")
    ax.set_ylabel("File changes count")
    ax.set_title(title)
    ax.set_xticks(list(total.keys()), labels=list(total.keys()), rotation=70, fontsize=4.5)

    plt.savefig(f'out_plots/{title.lower().replace(" ", "")}{broken_count}.png', dpi=250)


def process_person_file(author_in, file_in, in_data, broken_count=0):
    total_dict, broken_dict, not_broken_dict = parse_data(in_data, return_tuple=True)

    broken_file = sort_author_files_time_group(broken_dict, author_in, file_in)
    work_file = sort_author_files_time_group(not_broken_dict, author_in, file_in)
    total_file = sort_author_files_time_group(total_dict, author_in, file_in)

    plot_data(total_file, broken_file, work_file, f"{author_in} - {file_in.split('/')[-1]}", broken_count)


def get_most_edit_person_for_file(data, file):
    authors = {}

    for f in data:
        if f['file'] == file:
            if f['author'] not in authors:
                authors[f['author']] = 0
            authors[f['author']] += 1

    return max(authors, key=authors.get)


if __name__ == '__main__':
    url = "analyse_data_angular.json"

    with open(url, 'r') as read_file:
        main_data = json.load(read_file)

    broken_authors = get_authors_files_broken(main_data)
    broken_authors = {k: v for k, v in sorted(broken_authors.items(), key=lambda item: item[1], reverse=True)}

    for a in list(broken_authors.keys())[:10]:
        author, file = a.split("\n")
        print(f"Processing {author} - {file}: {broken_authors[a]}")

        process_person_file(author, file, main_data, broken_authors[a])
