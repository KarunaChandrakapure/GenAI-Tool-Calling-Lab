import mysql.connector

def execute_sql(query):
    connection = mysql.connector.connect(
        host="localhost",
        user="root",
        password="123456789",
        database="alert_systems"
    )

    cursor = connection.cursor()
    cursor.execute("SELECT *FROM alerts")
    results = cursor.fetchall()


    cursor.close()
    connection.close()    
    return results


result = execute_sql("SELECT * FROM alerts")   
print(result) 