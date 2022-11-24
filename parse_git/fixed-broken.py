import json
from datetime import datetime

from git import Repo

from utils import is_fix_commit

try:
    Repo.clone_from("https://github.com/knockout/knockout", "input/knockout")
except:
    pass

analyse_repo = Repo("input/knockout")
analyse_data = []
commits_count = len(list(analyse_repo.iter_commits("master")))
pending_files = set()
start_time = datetime.now()

for index, commit in enumerate(list(analyse_repo.iter_commits("master"))):
    if commit.message.startswith("Merge"):
        continue

    if index % 100 == 0:
        print(f"Analyse {index} of {commits_count}\n"
              f"Elapsed time: {datetime.now() - start_time}\n"
              f"For one commit: {(datetime.now() - start_time) / (index + 1)}\n"
              f"Estimated time: {(datetime.now() - start_time) / (index + 1) * (commits_count - index)}\n")

    for file in commit.stats.files:
        if file in pending_files:
            pending_files.remove(file)

            for a in analyse_data[::-1]:
                if a["file"] == file:
                    a["broken_by"] = commit.author.name
                    a["broken_msg"] = commit.message
                    a["broken_date"] = commit.committed_datetime.isoformat()
                    break

    if is_fix_commit(commit):
        for file in commit.stats.files:
            pending_files.add(file)

            analyse_data.append({
                "file": file,
                "fix_commit": commit.hexsha,
                "fixed_by": commit.author.name,
                "fixed_msg": commit.message,
                "fixed_date": commit.committed_datetime.isoformat(),
                "broken_by": None,
                "broken_msg": None,
                "broken_date": None,
            })

json.dump(analyse_data, open("output/analyse_data.json", "w"), indent=4)
print(
    f"Ready! Elapsed time: {datetime.now() - start_time}\n"
    f"For one commit: {(datetime.now() - start_time) / commits_count}\n"
)