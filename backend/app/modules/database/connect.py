import mysql.connector

def mysql_connect():
    # establish a connection to the database
    mysql_conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="Ease2Prosperity",
        database="asklylachat"
    )
    return mysql_conn