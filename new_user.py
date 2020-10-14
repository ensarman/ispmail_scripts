#!/usr/bin/env python3

import argparse
import MySQLdb
from sys import exit as sys_exit
from password import pw_gen, crypt_pass


parser = argparse.ArgumentParser()
parser.add_argument("-p", "--password", help="e-mail password, type 'gen' if want a generated password", default=None)
parser.add_argument("-q", "--quota", help="e-mail quota", default=None)
parser.add_argument("-db", "--dbname", help="mysql database", default='mailserver')
parser.add_argument("-dbh", "--dbhost", help="mysql host", default="localhost")
parser.add_argument("-dbu", "--dbuser", help="mysql username", default='mailadmin')
required_parser = parser.add_argument_group('required arguments')
required_parser.add_argument("-u", "--user", help="username", required=True)
required_parser.add_argument("-dbp", "--dbpassword", help="mysql password", required=True)

options = parser.parse_args()

user = options.user.split("@")[0]
domain = options.user.split("@")[1]

db = MySQLdb.connect(host=options.dbhost, user=options.dbuser,
                     passwd=options.dbpassword, db=options.dbname)
cursor = db.cursor()

if options.quota is None:
    quota = 1073741824  # 1 GB
else:
    # multiplicamos quota por el la cantidad de bytes en un GB
    quota = int(options.quota) * 1073741824
    print(f"new quota is: {quota} bytes")

if options.password is None:
    raw_password = pw_gen()
    print(f'new random password: {raw_password}')
    hashed_password = crypt_pass(raw_password)
elif len(options.password) < 10:
    sys_exit("Password length is less than 10 characters")
else:
    print(f"the new password is: {options.password}")
    hashed_password = crypt_pass(options.password)

query = f"""
INSERT INTO `virtual_users` (`id`, `domain_id`, `email`, `password`, `quota`)
    VALUES (NULL, (SELECT id FROM virtual_domains
    WHERE name='{domain}'), '{user}@{domain}','{hashed_password}', {quota});
"""
cursor.execute(query)
db.commit()
db.close()
