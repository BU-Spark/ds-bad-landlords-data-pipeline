import time
import json
from database.database import createAllTables, updateSummaryTable
import datetime
from criteriaII.processII import processData
from criteriaI.getData import fetchData, getBadLandlords


def identifyBadLandlords():
    start_time = time.time()

    print("Processing data...")
    # Process the data here
    # processData()
    # fetchBadLandlords()
    getBadLandlords()
    print("Data processing complete...")
    end_time = time.time()
    time_taken = end_time - start_time
    start_time_str = datetime.datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
    time_taken_minutes = time_taken / 60

    summary = tuple([start_time_str, time_taken_minutes, "Bad landlords identified successfully",
                     json.dumps({"criteria1": ["data_point1", "data_point2"], "criteria2": ["data_point1", "data_point2"]}),
                     json.dumps(["filter1", "filter2"])])
    updateSummaryTable(summary)
    pass

createAllTables()
identifyBadLandlords()