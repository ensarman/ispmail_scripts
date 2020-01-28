#!/usr/bin/python3

import argparse
import subprocess
from MySQLdb import _mysql
import string
import random

def pw_gen(size = 15, chars=string.ascii_letters + string.digits):
        return ''.join(random.choice(chars) for _ in range(size))



parser = argparse.ArgumentParser()
parser.add_argument("-u", help="username")
parser.add_argument("-p", help="password")
parser.add_argument("-d", help="domain")
parser.add_argument("-q", help="quota")
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
    dbpass = ""
else:
    dbpass = options.dbp

if options.db == None :
    database = "mailserver"
else:
    database = options.db

if options.q == None:
    quota = 0
else:
    quota = options.q

if options.p == None:
    raw_password = pw_gen()
else:
    raw_password = options.p
user = options.u
domain = options.d
quota = options.q

print(raw_password)

hashed_password = subprocess.run(
    ['doveadm', 'pw', '-s', 'BLF-CRYPT', '-p', raw_password],
    capture_output=True,
    encoding='utf8').stdout.rstrip()

print(hashed_password)

db = _mysql.connect(host=dbhost, user=dbuser, passwd=dbpass, db=database)


query = f"""
INSERT INTO `virtual_users` (`id`, `domain_id`, `email`, `password`, `quota`) VALUES (NULL, (SELECT id FROM virtual_domains WHERE name='{domain}'), '{user}@{domain}','{hashed_password}', {quota});
"""
db.query(query)

db.close()

