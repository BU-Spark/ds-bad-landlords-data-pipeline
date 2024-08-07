# About

Read about project goals and data sources in [this concise presentaion](https://docs.google.com/presentation/d/1KNGK72Dig-N882HKt90cVlukRAtAu-UxNVEodczT12w/edit?usp=sharing).

See project architecture [diagram here](https://www.figma.com/board/DLYAxLJqEGdjqHhQ4bwXLX/BadLandlords-Automated-Data-Pipeline?node-id=0-1&t=FKSWBu0LLGtjnAUu-1).

Overall, this repo contains code to;

1. Fetch building violation, property ownership and court case data from various sources.
2. Process the data to identify 'scofflaw' landlords according to the proposed ordinance.
3. Rerun the above data fetching and processing steps at a regular cadence (once every day).
4. Expose the list of 'scofflaw' landlords over a REST api.

# Live deployment

- https://badlandlords.sail.codes/summary : returns summary of the last process
- https://badlandlords.sail.codes/badlandlords?criteria=i : returns list of bad landlords identified from court cases
- https://badlandlords.sail.codes/badlandlords?criteria=ii : returns badland lords identified from building violations

# How to run

- Build image
  ```
  docker build -t image_name .
  ```
- Run container
  ```
  docker run -p 80:80 -d --name container_name image_name
  ```
  The above will build a docker image and start a container. On start, the container runs a bash script which schedules a cron job and starts a Flask server. The cron job runs a python module that fetches and processes data and is scheduled to run once every day.

The results of the data processing is stored in SQLite tables which are read and returned by the server when a client sends an API request to it.

# Other docs in this project

There are other docs in project that go over specific topics.

- [DataProcessing](DataProcessing.md): Goes over the methods used to identify bad landlords.
- [Deployment](Deployment.md): Goes over how this project is deployed and how to change configurations.
- [ApiServer](src/api-server/ApiServer.md) : Goes over the available API routes and what they return.
- [Todos](Todos.md) : Goes over major todos of the project.

# Contact person

Reach out to mannysa@bu.edu for clarification, if needed.
