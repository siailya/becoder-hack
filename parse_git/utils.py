from git import Commit


def is_fix_commit(c: Commit):
    return "fix" in c.message.lower()