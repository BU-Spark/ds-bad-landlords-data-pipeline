
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
    - criteria
    - 



