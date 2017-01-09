# gitlogExporter
version 0.0.1 stage

# Example usage
gitlogExporter/log2csv.py -r myrepo/ -b master -s "2016-01-01"


# Example for Data Export to Postgres

create table IF NOT EXISTS repo(sha varchar(43) NOT NULL PRIMARY KEY,  authored_date TIMESTAMP, author varchar(128),  author_email varchar(128), committed_date TIMESTAMP, committer varchar(128),committer_email varchar(128),  lines int,  insertions int,  deletions int,  filecount int);


copy repo
from 's3://ou-code-stat/monorepo/'
credentials 'aws_access_key_id=xxx;aws_secret_access_key=yy' delimiter ',' csv quote as '"' timeformat 'YYYY-MM-DD HH:MI:SS';
