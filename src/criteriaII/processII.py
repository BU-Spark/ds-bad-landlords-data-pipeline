import pandas as pd
import os
import requests
from datetime import datetime, timedelta

from database.database import insertIntoSQLiteTable

def indentifyBadlandlordsFromViolationsDatasets():
    violations_df = fetchViolationsData()
    sam_df = fetchSamData()
    violations_df = addParcelIdsToViolationsDataset(violations_df, sam_df)
    property_df = fetchPropertyData(violations_df)
    consolidateBadlandlordsData(property_df, violations_df)

def fetchSamData():
    # Sam dataset is not available via api currently so 
    # we will use a prefetched (2023) .xlsx file 
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
    return violations_df

def fetchPropertyData(violations_df):
    """
    instead of fetching the full property dataset, we will fetch only 
    the properties that have violations. typically, only a small subset
    of properties will have violations that meet the prescibed violation filters,
    so this is a more efficient approach.
    """
    # property filters
    # we fetch only rental properties ie not owner occupied
    violation_parcels = tuple(violations_df['parcel'].unique()) # we only need the landlords of the properties with violations
    url = f"https://data.boston.gov/api/3/action/datastore_search_sql?sql=SELECT * from \"a9eb19ad-da79-4f7b-9e3b-6b13e66f8285\" WHERE \"OWN_OCC\" = 'N' AND \"PID\" IN {violation_parcels}"
    print("Fetching property data with filters: OWN_OCC = 'N' AND PID IN", violation_parcels)
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()["result"]["records"]
        print("Successfully fetched property data.", len(data), "properties meet the filters.")
        return pd.DataFrame(data)
    else:
        print("Error fetching data from property dataset URL")
        return None
    
def addLandlordFullAddresses(property_df):
    property_df['address'] = property_df.apply(lambda x: {
        'addressee': x['MAIL_ADDRESSEE'],
        'street_address': x['MAIL_STREET_ADDRESS'],
        'city': x['MAIL_CITY'],
        'state': x['MAIL_STATE'],
        'zip_code': x['MAIL_ZIP_CODE']
    }, axis=1)
    return property_df

def consolidateBadlandlordsData(property_df, violations_df):
    """
    add landlord names to violations dataset
    add landlord address to violations dataset
    remove rows where landlord is null
    add list of each landlord's property addresses 
    save to sqlite db
    """
    addLandlordFullAddresses(property_df)

    # add landlord names and addresses to violations dataset
    violations_df['name'] = violations_df['parcel'].map(property_df.set_index('PID')['OWNER'])
    violations_df['address'] = violations_df['parcel'].map(property_df.set_index('PID')['address'])
    
    violations_df['violation_code'] = violations_df['code']
    
    # get relevant columns
    badlandlords_df = pd.DataFrame(violations_df[['name', 'violation_code', 'address']].dropna(subset=['name']))

    badlandlords_df['properties'] = badlandlords_df['name'].apply(fetchLandlordProperties)

    # convert json fields to string for sqlite
    badlandlords_df['address'] = badlandlords_df['address'].apply(lambda x: str(x))
    badlandlords_df['properties'] = badlandlords_df['properties'].apply(lambda x: str(x))

    insertIntoSQLiteTable("badlandlords_criteria_ii", badlandlords_df.values)


def fetchLandlordProperties(landlordName):
    url = f"https://data.boston.gov/api/3/action/datastore_search_sql?sql=SELECT * from \"a9eb19ad-da79-4f7b-9e3b-6b13e66f8285\" WHERE \"OWNER\" LIKE '{landlordName}'"
    # TODO ensure all properties of landlord are fetched instead of just one
    print(url)
    response = requests.get(url)
    if response.status_code == 200:
        data = response.json()["result"]["records"]
        l_p_df = pd.DataFrame(data)
        print("Successfully fetched property data for landlord:", landlordName)
        print(l_p_df)
        l_p_df = l_p_df.fillna('')
        addresses = l_p_df.apply(lambda x: {
            'st_num': x['ST_NUM'],
            'st_name': x['ST_NAME'],
            'unit_num': x['UNIT_NUM'],
            'city': x['CITY'],
            'zip_code': x['ZIP_CODE']
        }, axis=1)
        return addresses
    else:
        print("Error fetching properties of landlord:", landlordName)
        return []

"""
https://data.boston.gov/api/3/action/datastore_search_sql?sql=SELECT * from \"a9eb19ad-da79-4f7b-9e3b-6b13e66f8285\" WHERE \"OWNER\" LIKE 'LEXINGTON STREET REALTY TRUST'
"""