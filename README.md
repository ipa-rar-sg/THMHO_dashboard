## Heatmap Lidar

![General services architecture](docs/img/LidarHeatmapArch.png)

### Requirements

1. docker-compose version 1.29.2 or above

### How To

Go into the src directory and run the init.sh script (might require sudo
depending on your docker and docker-compose configuration). It will prompt
the user for the following data: 

1. Table name (Should NOT contain spaces nor special characters)
2. Heatmap width (Integer)
3. Heatmap height (Integer)

### Functionality

- Dashboard (dash): http://localhost:8050
- Flask API: http://localhost:5000
- Postgres DB: localhost:5432

To insert a registry into the factory table, send a post request to the following endpoint:

- http://localhost:5000/insert

With a json body, with the following fields and values:
- width: (int)
- height: (int)
- date: (string of timestamp)
- data: (list of ints, size width * height)

For automatic population of database make sure to be running in parallel your respective script that makes the mentioned request (E.g. Through rospy)
