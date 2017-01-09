#!/usr/bin/env python
from __future__ import print_function
import argparse

import time
import csv
from logExporter import *
import datetime as DT

def eprint(*args, **kwargs):
    print(*args, file=sys.stderr, **kwargs)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Export git log into csv.')
    parser.add_argument('-b', '--branch', action='store', dest="branch", help='specify the branch', required=True)
    parser.add_argument('-r', '--root', action='store', dest="gitroot",  help='specify the gitroot', required=True)
    parser.add_argument('-l', '--limit', action='store', dest="limit", type=int, help='specify the maxium items want to take')
    parser.add_argument('-s', '--since', action='store', dest="since", help='specify a date YYYY-MM-DD , e.g. 2014-1-1')

    args = parser.parse_args()
    repo = getRepo(args)

    if args.limit is None:
        limit = 999999;
    else:
        limit = int(args.limit)

    if args.since is None:
        since = time.mktime(time.strptime("2016-01-01", "%Y-%m-%d"));
    else:
        since = time.mktime(time.strptime(args.since, "%Y-%m-%d"));

    csvWriter = csv.writer(sys.stdout, quoting=csv.QUOTE_NONNUMERIC)
    for x in genTuples(repo, args.branch, limit, since):
        ## normal
        #dt = DT.datetime.utcfromtimestamp(x.authored_date)
        #iso_format = dt.isoformat() + 'Z'

        author_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(x.authored_date))
        # dt_c = DT.datetime.utcfromtimestamp(x.committed_date)
        # iso_format_c = dt.isoformat() + 'Z'

        commit_time = time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(x.committed_date))

        row = (x.sha, author_time, x.author_name, x.author_email, commit_time, x.committer_name, x.committer_email, x.lines, x.insertions, x.deletions, x.file_count)
        try:
            csvWriter.writerow (row)
        except Exception as e:
            eprint(">>>>>>>>>>>>>>")
            eprint(row)
            eprint(e)
            eprint("<<<<<<<<<<<<<<")
