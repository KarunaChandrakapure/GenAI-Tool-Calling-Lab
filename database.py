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
    try:
        cursor.execute(query)
        results = cursor.fetchall()
        return {
            'success':True,
            'data':results
        }
    except mysql.connector.Error as e:
        return 
        {
            'success':False,
            'data':str(e)
        }    

    finally:
        cursor.close()
        connection.close() 


      
  


   
