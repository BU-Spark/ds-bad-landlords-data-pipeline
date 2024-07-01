import time
import json
from database.database import createResultTables, updateSummaryTable
import datetime
from criteriaII.processII import indentifyBadlandlordsFromViolationsDatasets
from criteriaI.processI import identifyBadLandlordsFromCourtCaseDatabase

def identifyBadLandlords():
    start_time = time.time()
    print("Processing data...")
    identifyBadLandlordsFromCourtCaseDatabase()
    indentifyBadlandlordsFromViolationsDatasets()
    print("Data processing complete...")
    end_time = time.time()
    time_taken = end_time - start_time
    start_time_str = datetime.datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
    time_taken_minutes = round(time_taken / 60, 1)

    # TODO fill summary table with info about data points and filters used for processing
    summary = tuple([start_time_str, time_taken_minutes, "Bad landlords identified successfully",
                     json.dumps({"criteria1": ["data_point1", "data_point2"], "criteria2": ["data_point1", "data_point2"]}),
                     json.dumps(["filter1", "filter2"])])
    updateSummaryTable(summary)
    pass

createResultTables()
identifyBadLandlords()
# conn = getSQLiteConnection()
# cursor = conn.cursor()
# criteria = "ii"
# cursor.execute(f'SELECT * FROM badlandlords_criteria_{criteria}')
# rows = cursor.fetchall()
# result = [dict(zip([column[0] for column in cursor.description], row)) for row in rows]
# print(json.dumps(result))
# conn.close()