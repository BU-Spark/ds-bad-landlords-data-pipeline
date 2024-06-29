import sqlite3

DATABASE_NAME = 'badlandlords.db'

def getSQLiteConnection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def createAllTables():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # Delete previusly identified badlandlords. 
    # Other processing data is left untouched
    cursor.execute('''
        DROP TABLE IF EXISTS badlandlords_criteria_i
    ''')

    cursor.execute('''
        CREATE TABLE IF NOT EXISTS processing_summary_table (
            id INTEGER PRIMARY KEY,
            last_run TEXT,
            time_taken TEXT,
            summary TEXT,
            data_points TEXT,
            filters TEXT
        )
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS badlandlords_criteria_i (
            party_name varchar(255),
            party_id bigint(20),
            case_number varchar(50)
        );
    ''')
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS badlandlords_criteria_ii (
            name varchar(255),
            violation_code varchar(50),
            address TEXT,
            properties TEXT
        );
    ''')
    conn.commit()
    conn.close()

def updateSummaryTable(summary):
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO processing_summary_table (last_run, time_taken, summary, data_points, filters)
        VALUES (?, ?, ?, ?, ?)
    ''', (summary))
    conn.commit()
    conn.close()

def insertIntoSQLiteTable(table_name, data):
    try:
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        placeholders = ', '.join(['?' for _ in range(len(data[0]))])
        query = f'INSERT INTO {table_name} VALUES ({placeholders})'
        cursor.executemany(query, data)
        conn.commit()
        print(f"Data inserted into {table_name} table successfully!")
    except sqlite3.Error as error:
        print(f"Error while inserting data into {table_name} table:", error)
    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()
