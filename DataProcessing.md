# Overview
**Note**: Without meticulously going over the data sources in [this concise presentaion](https://docs.google.com/presentation/d/1KNGK72Dig-N882HKt90cVlukRAtAu-UxNVEodczT12w/edit?usp=sharing), this doc won't make sense. 


We identify badlandlords in each criteria separately. The results are written into three separate SQLite tables. Then, we try to combine that list to find possible matches ie landlords who are classified as 'bad' across multiple criteria. 

Again, please make sure to carefully review the above presentation in order to understand the following.

## Criteria I
The masscourt SQL database is already preprocessed and close to what we need. We just need to find cases that fit criteria I. All defendant landlords associated with the resulting cases are 'bad' landlords.

Relevant filters: 
- case_status == "Active"
- case_type == "Housing Court Civil" | "Housing Court Summary Process"
- party_type == "Defendant"

Note: The above filters may not be enough to narrow down to only cases that meet Criteria I. The current outstanding challenge is to identify cases where;
- the defendant is a landlord
- the case is about landlord's rental property
- the case is in *active enforcement proceedings*


### SQL Query
Goal: using the above filters, find all parties and their case. Steps;
- Find all cases that meet the filters in cdocs_case_meta_index table


- Find all defendant parties for the resulting cases from above in cdocs_party_assignment_index

- Write results to new table
```
Table : badlandlords_criteria_i
Schema:
    - party_name : varchar(255)
    - party_id : bigint(20) UN
    - case_number : varchar(50)
```
- Combinining the steps above; 

```
-- : Create the new table
CREATE TABLE badlandlords_criteria_i (
    party_name varchar(255),
    party_id bigint(20) UNSIGNED,
    case_number varchar(50)
);

-- Insert the relevant data into the new table
INSERT INTO badlandlords_criteria_i (party_name, party_id, case_number)
SELECT pi.party_name, pa.party_id, cm.case_number
FROM cdocs_party_assignment_index pa
JOIN cdocs_case_meta_index cm ON pa.case_id = cm.post_id
JOIN cdocs_party_index pi ON pa.party_id = pi.post_id
WHERE pa.party_type = 'Defendant'
  AND cm.case_status = 'Active'
  AND cm.case_type IN ('Housing Court Civil', 'Housing Court Summary Process');

```


## Criteria II
To find badlandlords, we use all three tables. Each row in violations table has a SamId. We get the Parcel number associate with that SamId in the sam table. Then we use that parcel number to find the associated landlord in the property table.

We then filter down to qualifying landlords and tally their total number of violations. Those with 6+ violations are 'bad' landlords.

The datasets are available via APIs.

Options:
 - Get full csv at https://data.boston.gov/dataset/705244a6-70a6-4ff8-ab8e-56441aff18e7/resource/800a2663-1d6a-46e7-9356-bedb70f5332c/download/tmp52ftfd_1.csv
 - Get filtered results using CKAN DATA API at https://data.boston.gov/api/3/action/datastore_search
 
- Eg query with SQL filter 

```
https://data.boston.gov/api/3/action/datastore_search_sql?sql=SELECT * from "800a2663-1d6a-46e7-9356-bedb70f5332c" WHERE "violation_stno" = '302'
```

steps
- fetch qualifying violations 
Relevant filters:
    - status_dttm >=  (now() - 12months) : ie with a date in the last 12 months: 
    - code = XXX
```
https://data.boston.gov/api/3/action/datastore_search_sql?sql=SELECT * from "800a2663-1d6a-46e7-9356-bedb70f5332c" WHERE status_dttm >= '2023-01-01 00:00:00' AND  "code" = '105.1'

```


- fetch qualifying landlords
    - owner occupied = N
    - 
```
https://data.boston.gov/api/3/action/datastore_search_sql?sql=SELECT * from "a9eb19ad-da79-4f7b-9e3b-6b13e66f8285" WHERE "OWN_OCC" = 'N'
```

- load into dataframe, df. 

- Get building parcel in sam table. Get from https://bostonopendata-boston.opendata.arcgis.com/api/download/v1/items/b6bffcace320448d96bb84eabb8a075f/csv?layers=0 . Sam dataset doesn't seem to be available anymore. It also hasn't been getting regular updates. Last update was 6 months ago, as of June, 2024. We could use previously-fetched sam table in postGres db. 


```

```

- Add and fill new column "parcel". 
 For each row in df, get and add parcel value by using the row's samid to fetch a parcel number in sam table.  


- Add and fill new column "lanlord". 
 For each row in df, get and add landlord value by using the row's parcel to fetch an owner in number in landlord table.  


- Create landlord tally.


- Create lanlord ids for efficient tallying
Using fuzzy matching, create an index of all landlords. For each row, check all other rows if match exceeds 0.9. If so, it's the same landlord. Add id. 


## Criteria III
This part is trivial. The short list here is hardcoded in a json. When the list starts to grow, a scraping script will be added to get the updated list regularly. 

