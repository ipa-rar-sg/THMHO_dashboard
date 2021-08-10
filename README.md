## Heatmap Lidar

Grafana + Postgres

### Initial Setup

1. Create the following docker volumes.
  ```bash
  docker volume create pgstorage
  docker volume create grafstorage
  ```
2. Create the network.
  ```bash
  docker network create heatmap_net
  ```

### Initial migration

### Functionality

### TODO
- [] Modularity through env variables (Maybe file)
- [] Functionality sh scripts
  + [] Grafana + DB connection through script (not through UI)
  + [] Scripts for API interaction
- [] Actual python code for flask
- [] Heatmap itself
