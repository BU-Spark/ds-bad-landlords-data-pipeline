# API Server

This is a simple api to return results of the data processing. Several routes will be added as data processing module matures.

## Routes

- GET /status

  - returns info on the last run. Data points include
    - time taken to process data, in minutes.
    - number of bad landlords in each criteria
    - data points used to get bad landlords in each criteria
    - filters used

- GET /badlandlords:

  - Return bad landlords in json format
  - params:
    - criteria : i, ii, iii, all
  - return format:
    - criteria i : {name, cases}
    - criteria ii : {name, address, violations, properties}. A violation is represented by violation case number whilst a property is represented by full address. Note that we return all landlords with a violation not necessarily those with 6+ violations. 

- GET /search:

  - Return bad landlords that meet the search query. in json format
  - params:
    - name
    - address
