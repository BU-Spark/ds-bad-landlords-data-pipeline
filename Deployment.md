## Setup in .env file
Criteria I requires credentials to connect mass court database. Place the credentials in a .env (similar to example.env) file under criteriaI directory.

## How to deploy

- build image
  ```
  build -t image_name .
  ```
- run container
  ```
  docker run -p 80:80 -d --name container_name image_name
  ```

The Flask server is served at port 80 so exposing the container's port 80 to localhost 80 makes the server available outside the container. 


## How to change processing cadence
Change cron time in 'cron-scheduler' file to change how often data is re-processed. 

# Debugging
View logs in file root/logfile.log