import pandas as pd
import os

def processData():
    # load sam csv file

    # get the absolute path of the current file
    current_file = os.path.abspath(__file__)
    directory = os.path.dirname(current_file)
    csv_path = os.path.join(directory, "sam.xlsx")
    
    # load the CSV file
    data = pd.read_excel(csv_path)
    
    # print the first 5 rows of the dataframe
    print(data.head())

