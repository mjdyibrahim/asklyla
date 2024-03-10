from modules.database.connect import mysql_connect

def test_db_connection():
    # Establish a connection to the database
    conn = mysql_connect()

    print("Executing test_db_connection()")

    # Create a cursor object
    cursor = conn.cursor()
    
    # Execute a basic SQL query to fetch the current database version
    cursor.execute("SELECT VERSION()")
    
    # Fetch the query result
    result = cursor.fetchone()

    # Print MySQL Databae version
    print("MySQL Database version:", result)
    
    # Close the cursor and connection
    cursor.close()
    conn.close()
    
    # Return the database version as a response
    return f"MySQL Database version: {result}"

if __name__ == '__main__':
    test_db_connection()