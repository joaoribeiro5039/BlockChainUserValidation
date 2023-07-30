# Worker Documentation

This documentation outlines the functionality and configuration of the `worker.py` script, which runs in a Docker container as a worker service. The script implements a simple blockchain system using Redis as the data store. It consists of creating and managing blocks, and it periodically updates the blockchain data based on the specified refresh rate.

## Prerequisites

- Docker: Make sure you have Docker installed on your machine.

## Configuration

The `worker.py` script can be configured using environment variables provided in the Docker Compose file (`docker-compose.yml`). The following environment variables can be set:

1. **REDIS_HOST**: The hostname or IP address of the Redis server. If not provided, the default value will be "localhost".

2. **REFRESH_RATE**: The refresh rate (in seconds) at which the blockchain data is updated. If not provided, the default value will be 1.0 seconds.

## Docker Compose Configuration

To run the `worker.py` script as a Docker service, you can use the provided `docker-compose.yml` file. This file defines the service configuration, build options, environment variables, and scaling settings.

```yaml
version: "3"

services:
  worker:
    build:
      context: ./worker
      dockerfile: Dockerfile
    restart: always
    environment:
      - REDIS_HOST=redis
      - REFRESH_RATE=1.0
    depends_on:
      - redis
    deploy:
      replicas: 2
```

The Docker Compose configuration sets up the following:

1. `worker` Service: This service runs the `worker.py` script in a Docker container.

2. `build`: Specifies the build context for the Dockerfile.

3. `restart: always`: Ensures that the worker service restarts automatically if it crashes or stops.

4. `environment`: Sets the environment variables for the worker service, such as `REDIS_HOST` and `REFRESH_RATE`.

5. `depends_on`: Declares a dependency on the `redis` service, ensuring that the Redis server is started before the worker service.

6. `deploy: replicas`: Specifies the number of replicas (instances) of the worker service. In this case, two replicas will be created.

## Usage

1. Ensure that you have Docker installed and the Docker daemon is running.

2. Place the `worker.py` script in the `./worker` directory along with the `Dockerfile` (for building the image).

3. Create a Redis service or container accessible through the `REDIS_HOST` environment variable. You can use the default Redis settings or customize them as needed.

4. Create the Docker Compose file (`docker-compose.yml`) with the provided configuration.

5. Navigate to the directory containing the `docker-compose.yml` file in your terminal or command prompt.

6. Run the following command to start the worker service:

```bash
docker-compose up -d
```

7. The `worker.py` script will run in the Docker container as a worker service, creating and managing the blockchain using Redis as the data store. The blockchain data will be periodically updated based on the specified `REFRESH_RATE`.

## Notes

- Ensure that you have the necessary permissions and firewall settings to run Docker containers on your machine.

- The provided script and Docker configuration serve as an illustrative example of a simple blockchain implementation using Redis. In a real-world scenario, you may need to consider additional security measures, scalability, and other factors for a robust and production-ready blockchain system.