import argparse
import os
import subprocess
import sys
import git
from git import Repo, InvalidGitRepositoryError
import base64
import time
import csv
class InvalidBranchError(Exception):
    pass

def main(args):
    try:
        repo = git.Repo(args.gitroot)
    except Exception as e:
        raise InvalidGitRepositoryError("%s is not a git repository" % (str(e)))

    try:
        if args.branch not in repo.branches:
            raise InvalidBranchError("Branch does not exist: %s" % (args.branch))
        text = repo.git.rev_list(args.branch).splitlines()
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
      yield (str(i.hexsha),
             time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(i.authored_date)),
             i.author.name, i.stats.total["lines"],
             i.stats.total["insertions"],
             i.stats.total["deletions"],
             extStat
             )

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Tag current branch with ticket ID')
    parser.add_argument('-b', '--branch', action='store', dest="branch", help='specify the branch')
    parser.add_argument('-r', '--root', action='store', dest="gitroot", help='specify the gitroot')
    parser.add_argument('-l', '--limit', action='store', dest="limit", type=int, help='specify the maxium items want to take')
    parser.add_argument('-s', '--since', action='store', dest="since", help='specify a date YYYY-MM-DD , e.g. 2014-1-1')

    args = parser.parse_args()
    repo = main(args)

    if args.limit is None:
        limit = 999999;
    else:
        limit = int(args.limit)

    if args.since is None:
        since = time.mktime(time.strptime("2016-01-1", "%Y-%m-%d"));
    else:
        since = time.mktime(time.strptime(args.since, "%Y-%m-%d"));

    csvWriter = csv.writer(sys.stdout, quoting=csv.QUOTE_NONNUMERIC)
    for x in genTuples(repo, args.branch, limit, since):
        x1 = x[0:-1] #drop last element
        csvWriter.writerow (x1)
