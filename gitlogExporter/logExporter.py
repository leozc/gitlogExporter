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
        fname, ext = os.path.splitext(os.path.basename(k))
        if len(ext)==0:
            ext = fname
        x = stat
        y = d[ext]
        v = { k: x.get(k, 0) + y.get(k, 0) for k in set(x) | set(y) }

        if not "file_count" in v:
            v["file_count"]=1
        else:
            v["file_count"] = v["file_count"] + 1


        d[ext] = v
    return d

class CommitObject:
    def __init__(self, sha, authored_date, author_name, author_email, committed_date, committer_name, committer_email, lines, insertions, deletions, file_count, extStat, raw_files):
        self.sha = sha
        self.authored_date =authored_date
        self.author_name =author_name
        self.author_email =author_email
        self.committed_date =committed_date
        self.committer_name =committer_name
        self.committer_email =committer_email
        self.lines =lines
        self.insertions =insertions
        self.deletions =deletions
        self.file_count =file_count
        self.extStat =extStat
        self.raw_files =raw_files

def genTuples(repo, branch, limit, since):
    for i in repo.iter_commits(branch):
      if i.authored_date < since:
        break

      if limit <= 0:
        break

      limit = limit - 1

      extStat = sumByExt(i.stats.files)
      file_count = len(i.stats.files)

      yield CommitObject(str(i.hexsha),
                i.authored_date,
                i.author.name.encode('utf-8'),
                i.author.email.encode('utf-8'),
                i.committed_date,
                i.committer.name.encode('utf-8'),
                i.committer.email.encode('utf-8'),
                i.stats.total["lines"],
                i.stats.total["insertions"],
                i.stats.total["deletions"],
                file_count,
                extStat,
                i.stats.files
            )
