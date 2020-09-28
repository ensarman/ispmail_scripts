#!python3

import argparse
import MySQLdb
from sys import exit as sys_exit
from password import pw_gen, crypt_pass


parser = argparse.ArgumentParser()

parser.add_argument("-p", "--password", help="e-mail password, type 'gen' if want a generated password", default=None)
parser.add_argument("-q", "--quota", help="e-mail quota", default=None)
parser.add_argument("-db", "--dbname", help="mysql database", default='mailserver')
parser.add_argument("-dbh",  "--dbhost", help="mysql host", default="localhost")
parser.add_argument("-dbu", "--dbuser", help="mysql username", default='mailadmin')
required_parser = parser.add_argument_group('required arguments')
required_parser.add_argument("-u", "--user", help="username", required=True)
required_parser.add_argument("-dbp", "--dbpassword", help="mysql password", required=True)

options = parser.parse_args()

user = options.user.split("@")[0]
domain = options.user.split("@")[1]

db = MySQLdb.connect(host=options.dbhost, user=options.dbuser, passwd=options.dbpassword, db=options.dbname)
cursor = db.cursor()

print(f"editing user: {options.user}")

cursor.execute(f' SELECT id, email, password, quota from virtual_users WHERE email = "{options.user}"')
row = cursor.fetchone()

if options.quota == None:
    quota = row[3]  # es entero
else:
    quota = int(options.quota) * 1073741824  #multiplicamos quota por el la cantidad de bytes en un GB
    print(f"quota changed by: {quota}")

## cambiar password
if options.password == 'gen':
    raw_password = pw_gen()
    print("generated_password")
    print(f'password changed by: {raw_password}')
    hashed_password = crypt_pass(raw_password)
elif options.password == None:
    hashed_password = row[2]
    print(f'password not changed')
elif len(options.password) < 10:
    sys_exit("Password length is less than 10 characters")
else:
    print(f'password changed by: {options.password}')
    hashed_password = crypt_pass(options.password)



query = f'''
    UPDATE `virtual_users` SET `password`="{hashed_password}", `quota`="{quota}" WHERE `email`="{options.user}";
    '''

cursor.execute(query)
db.commit()

db.close()
