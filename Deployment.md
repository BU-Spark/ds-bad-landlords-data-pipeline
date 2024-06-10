## How to deploy

- build image
  ```
  build -t image_name .
  ```
- run container
    ```
    docker run -d --name container_name image_name
    ```



## How to change processing cadence
Change cron time in 'cron-scheduler' file to change how often data is re-processed. 