## Heatmap Lidar

![General services architecture](docs/img/LidarHeatmapArch.png)

### Initial Setup

1. Create the docker volumes and network by executing the init.sh script
  ```bash
  ./src/init.sh
  ```
2. Inside the docker directory (Set the --build flag only for the first time, or if there are changes made to the flask app image)
  ```bash
  docker-compose up --build
  ```

### Functionality

- Grafana: http://localhost:3000
- API: http://localhost:5000
- Postgres: localhost:5432

To create the factory database:
- http://localhost:5000/create

To insert the test message into the facory db:
- http://localhost:5000/insert

### TODO
- [] Modularity through env variables (Maybe file)
- [] Functionality sh scripts
  + [] Scripts for API interaction
- [] Actual python code for flask
- [] Heatmap itself
