import pandas as pd
import os
import requests
from datetime import datetime, timedelta

def determineBadlandlordsFromViolationsDatasets():
    violations_df = fetchViolationsData()
    #drop some columns in the violations dataset. keep address, code, status_dttm, sam_id
    """
    address is combo of violation_stno": "27",
        "violation_sthigh": null,
        "violation_street": "Gilman",
        "violation_suffix": "ST",
        "violation_city": "Roslindale",
        "violation_state": "MA",
        "violation_zip": "02131",

    GET badlandlords criteria ii: return
        name, address, violations (comma separated case numbers)
    
        properties:
        

    """
    sam_df = fetchSamData()
    violations_df = addParcelIdsToViolationsDataset(violations_df, sam_df)
    fetchPropertyData(violations_df)

def fetchSamData():
    # Sam dataset is not available via api currently so 
    # we will use a prefetched (2023) sam.xlsx file 

    current_file = os.path.abspath(__file__)
    directory = os.path.dirname(current_file)
    csv_path = os.path.join(directory, "sam.xlsx")
    data = pd.read_excel(csv_path)
    print("Number of rows in sam dataset:", len(data))
    return data



def fetchViolationsData():
    # violation filters
    one_year_ago = datetime.now() - timedelta(days=365)
    status_dttm = one_year_ago.strftime('%Y-%m-%d %H:%M:%S') # only violations from the last 12 months, as per the ordinance
    codes = "('780', '527', '105')" # violation codes that are mentioned in the ordinance
    print("Fetching violations data with filters: status_dttm >= ", status_dttm, "AND code IN", codes)
    url = f"https://data.boston.gov/api/3/action/datastore_search_sql?sql=SELECT * from \"800a2663-1d6a-46e7-9356-bedb70f5332c\" WHERE status_dttm >= '{status_dttm}' AND code IN {codes}"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()["result"]["records"]
        print("Successfully fetched violations data.",len(data), "violations meet the filters.")
        print("Columns in violations dataset:", pd.DataFrame(data).columns)
        return pd.DataFrame(data)
    else:
        print("Error fetching data from violations URL")

def addParcelIdsToViolationsDataset(violations_df, sam_df):
    """
    add new column "parcel' to violations_df where values are filled with column PARCEL of sam_df where
    SAM_ADDRESS_ID (in sam_df) = sam_id (in violations_df)
    """
    # convert columns to be merged to same type
    violations_df['sam_id'] = violations_df['sam_id'].astype(str)
    sam_df['SAM_ADDRESS_ID'] = sam_df['SAM_ADDRESS_ID'].astype(str)

    merged_df = violations_df.merge(sam_df[['SAM_ADDRESS_ID', 'PARCEL']], left_on='sam_id', right_on='SAM_ADDRESS_ID', how='left')
    violations_df['parcel'] = merged_df['PARCEL']

    print(violations_df)
    return violations_df

def fetchPropertyData(violations_df):
    """
    instead of fetching the full property dataset, we will fetch only the properties that have violations. 
    typically, only a small subset of properties will have violations that meet the prescibed violation filters, so this is a more efficient approach.
    """
    # property filters
    # we fetch only rental properties ie not owner occupied
    violation_parcels = tuple(violations_df['parcel'].unique()) # we only need the landlords of the properties with violations
    # # violation_parcels_str = '"' + violation_parcels + '"'  # add quotes around the tuple
    url = f"https://data.boston.gov/api/3/action/datastore_search_sql?sql=SELECT * from \"a9eb19ad-da79-4f7b-9e3b-6b13e66f8285\" WHERE \"OWN_OCC\" = 'N' AND \"PID\" IN {violation_parcels}"
    print("Fetching property data with filters: OWN_OCC = 'N' AND PID IN", violation_parcels)
    # url = "https://data.boston.gov/api/3/action/datastore_search_sql?sql=SELECT * from \"a9eb19ad-da79-4f7b-9e3b-6b13e66f8285\" WHERE OWN_OCC = 'N' AND PID IN ('1806169000', '1501455000', '2201603000', '2204406000', '2203238000', '2205338000')"
    # url = "https://data.boston.gov/api/3/action/datastore_search_sql?sql=SELECT * from \"a9eb19ad-da79-4f7b-9e3b-6b13e66f8285\" WHERE \"OWN_OCC\" = 'N' AND \"PID\" IN ('2203238000', '2205338000')"
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()["result"]["records"]
        print("Successfully fetched property data.", len(data), "properties meet the filters.")
        property_df = pd.DataFrame(data)

        # get only relevant columns: PID, OWNER, MAIL_ADDRESSEE, MAIL_STREET_ADDRESS, MAIL_CITY, MAIL_STATE, MAIL_ZIP_CODE
        # combine MAIL_STREET_ADDRESS, MAIL_CITY, MAIL_STATE, MAIL_ZIP_CODE to form new column address
        property_df['address'] = property_df['MAIL_ADDRESSEE'] + ", " + property_df['MAIL_STREET_ADDRESS'] + ", " + property_df['MAIL_CITY'] + ", " + property_df['MAIL_STATE'] + " " + property_df['MAIL_ZIP_CODE']

        # add landlord names to violations dataset
        violations_df['landlord'] = violations_df['parcel'].map(property_df.set_index('PID')['OWNER'])
        violations_df['address'] = violations_df['parcel'].map(property_df.set_index('PID')['address'])

        violations_df['violations'] = violations_df.groupby('landlord')['case_no'].transform(lambda x: ', '.join(x))
        # add property addresses to violations dataset
        print(violations_df)

        badlandlords_df = violations_df[['landlord', 'address', 'violations']].drop_duplicates().dropna()
        badlandlords_df.rename(columns={'landlord': 'name'}, inplace=True)
       
        # fetch all properties of landlords with violations
        for landlord in badlandlords_df['name']:
            badlandlords_df['properties'] = fetchLandlordProperties(landlord)
       
     
        print(violations_df)
        print(badlandlords_df)
    else:
        print("Error fetching data from property dataset URL")

    # fetch all properties of landlords with violations

def fetchLandlordProperties(landlordName):
    url = f"https://data.boston.gov/api/3/action/datastore_search_sql?sql=SELECT * from \"a9eb19ad-da79-4f7b-9e3b-6b13e66f8285\" WHERE \"OWNER\" LIKE {landlordName}"
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()["result"]["records"]
        property_df = pd.DataFrame(data)
        return property_df['MAIL_ADDRESSEE'] + ", " + property_df['MAIL_STREET_ADDRESS'] + ", " + property_df['MAIL_CITY'] + ", " + property_df['MAIL_STATE'] + " " + property_df['MAIL_ZIP_CODE']
  

def processData():

    # get relevant violations data
 
  

    # continue with the rest of the code
    pass