# Blockchain Project Documentation

This documentation provides an overview of the Blockchain project, which consists of three services running in Docker containers: Redis, API, and Worker. The project aims to simulate a simple blockchain system using Redis as the data store and provide an API for interacting with the blockchain.

![Image Alt Text](https://example.com/path/to/image.png)


## Services

### 1. Redis

**Description:** The Redis service runs the Redis server in a Docker container. Redis is used to store the blockchain data and provide persistence for the blockchain.

**Container Name:** redis

**Image:** redis:latest

**Exposed Port:** 6379 (mapped to host port 6379)

**Volume:** redis_data (used to persist Redis data)

**Restart Policy:** always (Redis container will automatically restart if it crashes)

### 2. API

**Description:** The API service runs the FastAPI application in a Docker container. The API serves as an interface to interact with the blockchain stored in Redis. It provides endpoints to create blocks, simulate user movement between zones, and retrieve blockchain information.

**Container Name:** api

**Build:** The API container is built using the Dockerfile located in the "./api" directory.

**Exposed Port:** 8000 (mapped to host port 8000)

**Environment Variables:**
- `REDIS_HOST`: Set to "redis" to indicate the Redis container as the host for the Redis server used by the API.

**Restart Policy:** always (API container will automatically restart if it crashes)

**Dependencies:**
- The API service depends on the Redis service to be running before it starts.

### 3. Worker

**Description:** The Worker service runs the Python script `worker.py` in multiple Docker containers (specified by the `replicas` field). The Worker simulates the movement of users between zones in the blockchain and updates the blockchain stored in Redis accordingly.

**Container Name:** worker

**Build:** The Worker container is built using the Dockerfile located in the "./worker" directory.

**Environment Variables:**
- `REDIS_HOST`: Set to "redis" to indicate the Redis container as the host for the Redis server used by the Worker.
- `REFRESH_RATE`: Set to 1.0 (seconds) to define the time interval between blockchain updates.

**Restart Policy:** always (Worker containers will automatically restart if they crash)

**Dependencies:**
- The Worker service depends on the Redis service to be running before it starts.

**Deploy:**
- The `replicas` field is set to 2, which means there will be two Worker containers running in parallel.

## Usage

1. Ensure that you have Docker installed and the Docker daemon is running.

2. Create a directory structure with the following layout:
```
project_directory/
  |- api/
  |    |- app.py
  |    |- Dockerfile
  |- worker/
  |    |- worker.py
  |    |- Dockerfile
  |- docker-compose.yml
```

3. Place the `app.py` script in the "api" directory and the `worker.py` script in the "worker" directory.

4. Create the `docker-compose.yml` file with the provided configuration.

5. Navigate to the "project_directory" in your terminal or command prompt.

6. Run the following command to start the Redis, API, and Worker services:

```bash
docker-compose up -d
```

7. The Redis server, API, and Worker services will be running in separate Docker containers.

## Notes

- The provided Docker Compose configuration sets up a simple simulation of a blockchain system using FastAPI, Redis, and Python. In a real-world scenario, you may need to consider additional security measures, load balancing, scaling, and other factors for a production-ready blockchain solution.

- The Worker service simulates user movement and updates the blockchain periodically based on the `REFRESH_RATE` environment variable. The `REFRESH_RATE` value can be adjusted in the `docker-compose.yml` file to change the frequency of blockchain updates.

- The provided API endpoints allow users to interact with the blockchain and simulate user movement. However, additional authentication and validation mechanisms should be implemented in a real-world application to ensure data integrity and security.

- It is recommended to deploy the project in a secure and isolated environment, and configure any necessary firewall settings to restrict access to the services as needed.

- The blockchain system in this project is for illustrative purposes only and may not be suitable for production use. For a robust and production-ready blockchain solution, consider using well-established blockchain frameworks and protocols.

- For a more comprehensive API documentation, you can refer to the "Blockchain API Documentation" section provided earlier. This section explains the available API endpoints and their functionality.