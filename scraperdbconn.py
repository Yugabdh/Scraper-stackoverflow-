import mysql.connector
from mysql.connector import errorcode


try:
    cnx = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="",
        database="scraperDB")
    if cnx:
        cursor = cnx.cursor()

        def getQueries():
            try:
                query = ("Select arg from SearchQueries")
                cursor.execute(query)
                op = cursor.fetchall()
                available = list()
                for x in op:
                    available.append(x[0])
                for i, x in enumerate(available, 1):
                    print(f"{ i }. { x }")
                return available
            except Exception as e:
                print("error while getQueries")
                raise e

except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("Something is wrong with your user name or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("Database does not exist")
    else:
        print(err)

