# API Server

This is a simple api to return results of the processing. Several routes will be added as data processing module matures.

## Routes

- GET /status

  - returns info on the last run. Data points include
    - time it took
    - number of bad landlords in each criteria
    - data points used to get bad landlords in each criteria
    - filters used

- POST /forcerun:

  - reruns data processing immediately without waiting for next scheduled time.

- GET /badlandlords:

  - Return bad landlords in json format
  - params:
    - criteria : i, ii, iii, all
  - return format:
    - criteria i : {name, cases}
    - criteria ii : {name, address, violations, properties}. violations and properties are comma separated OR arrays of strings. A violation is represented by violation case number whilst a property is represented by full address.
    
  - Implementation:

    - criteria I: get unique landlords from badlandlords_criteria_i table.

    ```
      SELECT party_name, party_id, case_number
      FROM badlandlords_criteria_i
      WHERE row_num = 1;

    ```

- GET /badlandlords/search:

  - Return bad landlords that meet the search query. in json format
  - params:
    - name
    - address

- GET /cases/landlord_id:

  - Return all cases that a bad landlord is involved in. in json format
  - params:
    - landlord_id

- GET /properties/landlord_id:
  - Return all properties that a bad landlord owns. in json format
  - params:
    - landlord_id
