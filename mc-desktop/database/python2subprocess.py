from pyspatialite import dbapi2 as db
import sys, os, logging


database = sys.argv[2]
query_str = sys.argv[1]

if sys.argv[3] == 'True':

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

else:
    con = db.connect(database)
    c = con.cursor()
    c.execute(query_str)
    con.commit()
    c.close()