import mysql.connector
from database.database import getSQLiteConnection, insertIntoSQLiteTable
import os
from dotenv import load_dotenv


load_dotenv()
# Database credentials
host = os.getenv("DATABASE_HOST")
user = os.getenv("DATABASE_USER")
password = os.getenv("DATABASE_PASSWORD")
database = "wp_courtdocs"


def getConnection():
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        print("Connection to masscourt database successful!")
        return connection
    except mysql.connector.Error as error:
        print("Error while connecting to masscourt database:", error)
        return None

def fetchData():
    connection = getConnection()
    if connection is None:
        return
    
    print("Criteria I: Fetching bad landlords from mass court data...")    
    cursor = connection.cursor()
    query = "SELECT pi.party_name, pa.party_id, cm.case_number \
            FROM cdocs_party_assignment_index pa \
            JOIN cdocs_case_meta_index cm ON pa.case_id = cm.post_id \
            JOIN cdocs_party_index pi ON pa.party_id = pi.post_id \
            WHERE pa.party_type = 'Defendant' \
            AND cm.case_status = 'Active' \
            AND cm.case_type IN ('Housing Court Civil', 'Housing Court Summary Process') \
            LIMIT 15;"
    print("Executing query...", query)
    cursor.execute(query)
    result = cursor.fetchall()

    insertIntoSQLiteTable("badlandlords_criteria_i" ,result)
    cursor.close()
    connection.close()


def getBadLandlords():
    fetchData()
    conn = getSQLiteConnection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT party_name, party_id, case_number
        FROM badlandlords_criteria_i
        GROUP BY party_id;
    ''')
    result = cursor.fetchall()
    for row in result:
       print(row[0], row[1], row[2])
    conn.close()
    return result