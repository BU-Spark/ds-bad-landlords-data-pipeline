## What's left to do

### Update mass court filters with expert interpretaion of the ordinance in Criteria II
The exact meaning of *active enforcement proceedings* and the corresponding matching cases in mass court database are yet to be confirmed by an expert. So far, we select cases based on layman's guess of which cases meet criteria II.

### Combine results from all three criteria
In addition to getting bad landlords from the three criterias, it might be helpful to combine the results into a singular list. The list can mark landlords that appear in multiple criteria.

Currently, the only feasible method to find if a landlord appears in multiple caterias is to fuzzy-match by name. There isn't any other idntifying feature that appears in all three criteria to allow perfect matching. 

The only identifying info, besides name, we have of landlords is their address, which is only available in criteria II. Data sources of the two other categories have name as the only identifying info.

### Implement searching
Part of the deliverables is searching by landlord name or address. This needs to be implemented on route GET /search.


### Deploy
Project is currently deployed on NERC for demo purposes. Find a permanent deployment home. 

### Miscellaneous implementation todos 
- Complete criteria III
    - simply return the official list of problem properties on route GET /badlandlords?criteria=iii
- [Sam dataset](https://data.boston.gov/dataset/live-street-address-management-sam-addresses)'s api is offline at the moment. When it is online, modify criteria II to fetch sam data via api instead of the locally stored, 6 months+ old xlsx file. 
- Fill summary table with info about data points and filters used for processing.
- In criteria II, ensure all properties of a landlord are fetched instead of just one.

