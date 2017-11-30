#!/usr/bin/python3.6
import sqlite3
import os

# define the database location
mydb = '/var/tmp/ip.db'

# read entries in db
db = sqlite3.connect(mydb)
c = db.execute('select ip from Hostile')
for row in c:
    ip = c.fetchone()	# returns a tuple
    # create the ipset command that will be executed (once per IP)
    # note the --quiet option sends stdout to /dev/null
    blockip = "ipset -quiet add blacklist " + ip[0]
    # execute the command from a shell
    ret = os.system(blockip)
    print(ret)
