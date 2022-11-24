import json
from datetime import datetime

from git import Repo

from utils import is_fix_commit

NAME = "angular"
COMMITS_LIMIT = 5000

try:
    Repo.clone_from("https://github.com/angular/angular", f"input/{NAME}")
    print("Cloned")
except:
    print("Already cloned")

analyse_repo = Repo(f"input/{NAME}")
analyse_data = []
commits_count = len(list(analyse_repo.iter_commits("main"))[:COMMITS_LIMIT])
changed_files = set()
start_time = datetime.now()


print(f"Start analyse {NAME}\nTotal commits:", commits_count)
for index, commit in enumerate(list(analyse_repo.iter_commits("main"))[:COMMITS_LIMIT][::-1]):
    if commit.message.startswith("Merge"):
        continue

    if index % 100 == 0:
        print(f"Analyse {index} of {commits_count}\n"
              f"Elapsed time: {datetime.now() - start_time}\n"
              f"For one commit: {(datetime.now() - start_time) / (index + 1)}\n"
              f"Estimated time: {(datetime.now() - start_time) / (index + 1) * (commits_count - index)}\n")
        json.dump(analyse_data, open(f"output/analyse_data_{NAME}.json", "w"), indent=4)

    for file in commit.stats.files:
        if is_fix_commit(commit):
            for a in analyse_data[::-1]:
                if a["file"] == file:
                    a["is_broken"] = True
                    break

        analyse_data.append({
            "file": file,
            "author": commit.author.name,
            "msg": commit.message,
            "date": commit.committed_datetime.isoformat(),
            "is_broken": False,
        })

json.dump(analyse_data, open(f"output/analyse_data_{NAME}.json", "w"), indent=4)

print(
    f"Ready! Elapsed time: {datetime.now() - start_time}\n"
    f"For one commit: {(datetime.now() - start_time) / commits_count}\n"
)
