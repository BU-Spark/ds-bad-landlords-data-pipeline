import sqlite3

DATABASE_NAME = 'sample.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def createAllTables():
    conn = sqlite3.connect(DATABASE_NAME)
    cursor = conn.cursor()

    # processing_summary_table
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
