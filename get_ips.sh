#!/bin/sh
###################################################################
# $Id: get_ips.sh,v 1.2 2017/11/27 02:58:24 root Exp root $
# Purpose: Parses firewall denials in /var/log/messages and writes
#          output a text file which is read by update_db.py .
#          This program runs out of the HoneyPot's crontab
###################################################################
# tmp file 
TMPFL="/tmp/hostile_ips.txt"

# read log file for Firewalld
LOGFL="/var/log/messages"

# the next one line of shell commands parses all the denials and
# results in 4 space-delimited fields: Month Day Time sourceIP
#  1. grep FINAL_REJECT from /var/log/messages
#  2. capture the 1st, 2nd, 3rd, and 10th fields
#  3. get rid of "SRC=" in the 10th field
#  4. sort the output by IP (4th field)
#  5. eliminate duplcate IP's 
grep "FINAL_REJECT" $LOGFL | awk '{ print $1 " " $2 " " $3 " " $10 }' | sed 's/SRC=//' | sort -k 4 | uniq --skip-fields=3  > $TMPFL

# exit gracefully with a return code of 0
exit 0

