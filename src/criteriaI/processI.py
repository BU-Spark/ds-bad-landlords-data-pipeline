import mysql.connector
from database.database import getSQLiteConnection, insertIntoSQLiteTable
import os
from dotenv import load_dotenv
import pandas as pd
import json

load_dotenv()
# database credentials
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

def fetchBadLandlordsFromCourtCaseDatabase():
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
    fetchAllCasesInvolvingBadLandlord(result)
    cursor.close()
    connection.close()
    
def fetchAllCasesInvolvingBadLandlord(badlandlord_rows):
    """
    fetch all active cases involving a badlandlord
    whether they are defendant or not. 
    result is simply appended to the badlandlords_criteria_i table
    """
    connection = getConnection()
    if connection is None:
        return
    
    print("Criteria I: Fetching all cases involving badlandlords from mass court data...")    
    cursor = connection.cursor()
    for row in badlandlord_rows:
        party_id = row[1]
        query = f"SELECT pi.party_name, pa.party_id, cm.case_number \
                FROM cdocs_party_assignment_index pa \
                JOIN cdocs_case_meta_index cm ON pa.case_id = cm.post_id \
                JOIN cdocs_party_index pi ON pa.party_id = pi.post_id \
                WHERE pa.party_id = {party_id} \
                AND cm.case_status = 'Active' \
                AND cm.case_type IN ('Housing Court Civil', 'Housing Court Summary Process');"
        cursor.execute(query)
        result = cursor.fetchall()
        insertIntoSQLiteTable("badlandlords_criteria_i" ,result)
    cursor.close()

def getFormattedUniqueBadLandlords():
    conn = getSQLiteConnection()
    query = '''
        SELECT party_name, party_id, case_number
        FROM badlandlords_criteria_i
    '''
    df = pd.read_sql_query(query, conn)
    conn.close()

    # group by party_name and party_id, then aggregate case_numbers into a list
    grouped_df = df.groupby(['party_name', 'party_id'])['case_number'].agg(list).reset_index()
    grouped_df.rename(columns={'case_number': 'case numbers'}, inplace=True)
    
    # convert to jon
    result = grouped_df.to_dict(orient='records')
    return json.dumps(result, indent=4)