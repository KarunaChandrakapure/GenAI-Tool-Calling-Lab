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
        port=int((os.getenv("MYSQL_PORT")))
    )
      
   
    cursor = connection.cursor()
    try:
        query_clean = query.strip().lower()
        if not query_clean.startswith("select"):
            return {
                "success":False,
                "error":"Only SELECT queries are allowed"
            }
        cursor.execute(query)
        results = cursor.fetchall()
        return {
            'success':True,
            'data':results
        }
    except mysql.connector.Error as e:
        return {
            'success':False,
            'error':str(e)
        }    

    finally:
        cursor.close()
        connection.close() 

def get_schema():
    return {
        "table": "alerts",
        "columns": {
            "id": "integer - unique alert ID",
            "date": "date - date of alert",
            "time": "time - time of alert",
            "camera_name": "string - camera identifier",
            "alert_type": "string - type of alert"
        }
    }
  


   
