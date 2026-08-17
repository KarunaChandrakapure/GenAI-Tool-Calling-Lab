import os
import mysql.connector
from dotenv import load_dotenv
load_dotenv()
def execute_sql(query):
    
    connection = mysql.connector.connect(
        
        host=os.getenv("MYSQL_HOST"),
        user=os.getenv("MYSQL_USER"),
        password=os.getenv("MYSQL_PASSWORD"),
        database=os.getenv("MYSQL_DATABASE"),
        port=(os.getenv("MYSQL_PORT"))
    )

    cursor = connection.cursor()
    cursor.execute("SELECT *FROM alerts")
    results = cursor.fetchall()


    cursor.close()
    connection.close()    
    return results


result = execute_sql("SELECT * FROM alerts")   
#print(result) 