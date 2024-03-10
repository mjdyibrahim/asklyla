from modules.database.connect import mysql_connect

conn = mysql_connect()
cursor = conn.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS users (
                      id INT PRIMARY KEY AUTO_INCREMENT,
                      username VARCHAR(50) NOT NULL,
                      email VARCHAR(50) NOT NULL UNIQUE,
                      password VARCHAR(255) NOT NULL,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')

cursor.close()
conn.close()
