#!/usr/bin/python3.6
###############################################################
# $Id$
# Purpose: Update db of hostile ip's
###############################################################

import sqlite3

# define the database location
mydb = '/var/tmp/ip.db'

# connect to the database
db = sqlite3.connect(mydb)

# create the db if it doesn't exists
db.execute('CREATE TABLE IF NOT EXISTS Hostile (mon text, day text, time text, ip text, UNIQUE(ip))')

# open /tmp/hostile_ips.txt created by cron job
try:
    f = open('/tmp/hostile_ips.txt', 'r')
except:
    print('WARNING: File /tmp/hostile_ips.txt cannot be opened')
    exit()

hostile = f.readlines()
# remove whitespace characters or \n at end of lines
hostile = [x.strip() for x in hostile] 

for line in hostile:
    mon = line.split()[0]
    day = line.split()[1]
    time = line.split()[2]
    ip = line.split()[3]

    msg = 'INSERT OR IGNORE INTO Hostile (mon, day, time, ip) VALUES (?,?,?,?)'
    db.execute(msg, (mon, day, time, ip))

# difference between committing db changes here and in the loop is massive!
db.commit()

# close the input file
f.close()




