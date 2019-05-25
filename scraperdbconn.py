import mysql.connector
from mysql.connector import errorcode


def getQueries():
    try:

        cnx = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="scraperDB")

        if cnx:
            cursor = cnx.cursor()

        query = """Select arg from SearchQueries"""
        cursor.execute(query)
        op = cursor.fetchall()

        available = list()
        for x in op:
            available.append(x[0])

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    except Exception as e:
        print("error while getQueries")
        raise e

    finally:
        # closing database connection.
        if(cnx.is_connected()):
            cursor.close()
            cnx.close()
        return available


def insertScrappedData(data):
    try:

        cnx = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="scraperDB")

        if cnx:
            cursor = cnx.cursor()

        query = """INSERT INTO ScrapedData (qusRef, questionHeading, questionLink, votes, answered) VALUES (%s, %s, %s, %s, %s)"""
        result = cursor.executemany(query, data)
        cnx.commit()
        print (cursor.rowcount, "Record inserted successfully into ScrapedData table")

    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
            print("Something is wrong with your user name or password")
        elif err.errno == errorcode.ER_BAD_DB_ERROR:
            print("Database does not exist")
        else:
            print(err)
    except mysql.connector.Error as error:
        cnx.rollback()
        print("Failed to insert into MySQL table {}".format(error))
    except Exception as e:
        print("error while getQueries")
        raise e

    finally:
        # closing database connection.
        if(cnx.is_connected()):
            cursor.close()
            cnx.close()


def addQuery(userTag):
    try:

        cnx = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="scraperDB")

        if cnx:
            cursor = cnx.cursor()

        query = """INSERT INTO SearchQueries (arg) VALUES (%s)"""
        result = cursor.execute(query, (str(userTag),))
        cnx.commit()
        print (cursor.rowcount, "Record added successfully")

    except mysql.connector.Error as error:
        cnx.rollback()
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        # closing database connection.
        if(cnx.is_connected()):
            cursor.close()
            cnx.close()


def getDatafromDB():
    try:

        cnx = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="scraperDB")
        if cnx:
            cursor = cnx.cursor()
        available = getQueries()
        for i, x in enumerate(available, 1):
            print(f"{i}. {x}")
        c = int(input("Choice: ").strip())
        query = f"""SELECT * from ScrapedData where qusRef = {c}"""
        cursor.execute(query)
        print(f"[*] Printing data related to {available[c-1]}")
        op = cursor.fetchall()
        for i, x in enumerate(op):
            print(f"{i}. Question: {x[2]}")
            print(f"    link: {x[3]}")
            print(f"    Votes: {x[4]}")
            print(f"    Answers: {x[5]}")
            print()

    except mysql.connector.Error as error:
        cnx.rollback()
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        # closing database connection.
        if(cnx.is_connected()):
            cursor.close()
            cnx.close()


def deleteScrapped():
    try:

        cnx = mysql.connector.connect(
            host="localhost",
            user="root",
            passwd="",
            database="scraperDB")
        if cnx:
            cursor = cnx.cursor()
        available = getQueries()
        for i, x in enumerate(available, 1):
            print(f"{i}. {x}")
        c = int(input("Choice: ").strip())
        query = f"""Delete from ScrapedData where qusRef = {c}"""
        cursor.execute(query)
        cnx.commit()
        print(cursor.rowcount, "record(s) deleted")

    except mysql.connector.Error as error:
        cnx.rollback()
        print("Failed to insert into MySQL table {}".format(error))

    finally:
        # closing database connection.
        if(cnx.is_connected()):
            cursor.close()
            cnx.close()
