import os
import subprocess
import sys
import git
from git import Repo, InvalidGitRepositoryError
import time
class InvalidBranchError(Exception):
    pass

def getRepo(args):
    try:
        repo = git.Repo(args.gitroot)
    except Exception as e:
        raise InvalidGitRepositoryError("%s is not a git repository" % (str(e)))

    try:
        if args.branch not in repo.branches:
            raise InvalidBranchError("Branch does not exist: %s" % (args.branch))
    except:
        sys.exit("no such branch")
    return repo

from collections import defaultdict

def sumByExt(m):
    d = defaultdict(dict)
    for k in m.keys():
        stat = m[k]
        fname, ext = os.path.splitext(k)
        x = stat
        y = d[ext]
        v = { k: x.get(k, 0) + y.get(k, 0) for k in set(x) | set(y) }
        d[ext] = v
    return d

def genTuples(repo, branch, limit, since):
    for i in repo.iter_commits(branch):
      if i.authored_date < since:
        break

      if limit <= 0:
        break

      limit = limit - 1

      extStat = sumByExt(i.stats.files)
      yield {"sha": str(i.hexsha),
             "authored_date": time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(i.authored_date)),
             "authored_name": i.author.name,
             "lines": i.stats.total["lines"],
             "insertions": i.stats.total["insertions"],
             "deletions": i.stats.total["deletions"],
             "extStat": extStat
             }
