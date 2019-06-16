import mysql.connector
from mysql.connector import errorcode

import Artists as art

DB_NAME = 'Art'
# cnx = mysql.connector.connect(user='akuma', password='5s5e2r2g', database= DB_NAME)
cnx = mysql.connector.connect(user='akuma', password='123456')
cursor = cnx.cursor(buffered=True)

try:
    cursor.execute("USE {}".format(DB_NAME))
except mysql.connector.Error as err:
    print("Database {} does not exists.".format(DB_NAME))
    if err.errno == errorcode.ER_BAD_DB_ERROR:
        art.create_database(cursor)
        print("Database {} created successfully.".format(DB_NAME))
        cnx.database = DB_NAME
    else:
        print(err)
        exit(1)

art.create_table(cursor)
art.create_foreign_key(cursor)
art.initializing_db(cursor)


cnx.commit()

cursor.close()
cnx.close()
