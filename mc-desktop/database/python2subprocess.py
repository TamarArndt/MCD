from pyspatialite import dbapi2 as db
import sys, os, logging


# TODO if database path is given by user, this needs to receive given path
currentpath = os.path.dirname(__file__)
database = os.path.join(currentpath, './../assets/data.db')


query_str = sys.argv[1]

con = db.connect(database)
result = con.execute(query_str)

# for json-list type output
first=True
for row in result:
    if first:
        first=False
        out_str = '['+row[0]
    else:
        out_str = out_str+','+row[0]
out_str = out_str+']'
print(out_str)