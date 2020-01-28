#!/usr/bin/python3

import argparse
import subprocess
from MySQLdb import _mysql


parser = argparse.ArgumentParser()
parser.add_argument("-u", help="username")
parser.add_argument("-p", help="password")
parser.add_argument("-d", help="domain")
parser.add_argument("-db", help="mysql database")
parser.add_argument("-dbh", help="mysql host")
parser.add_argument("-dbu", help="mysql username")
parser.add_argument("-dbp", help="mysql password")

options = parser.parse_args()

if options.dbh == None :
    dbhost = 'localhost'
else:
    dbhost = options.dbh

if options.dbu == None :
    dbuser = 'mailadmin'
else:
    dbuser = options.dbu

if options.dbp == None :
    raise argparse.ArgumentError("no password given")
else:
    dbpass = options.dbp

if options.dbp == None :
    database = "mailserver"
else:
    database = options.db

raw_password = options.p
user = options.u
domain = options.d

hashed_password = subprocess.run(
    ['doveadm', 'pw', '-s', 'BLF-CRYPT', '-p', raw_password],
    capture_output=True,
    encoding='utf8').stdout

db = _mysql.connect(host=dbhost, user=dbuser, passwd=dbpass, db=database)

db.query(f"""
INSERT INTO virtual_users (domain_id, email, password) 
VALUES (SELECT id FROM virtual_domains WHERE name='{domain}'), '{user}@{domain}','{hashed_password}';""")

print(hashed_password)
