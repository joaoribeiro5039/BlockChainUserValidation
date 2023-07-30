# Blockchain API Documentation

This documentation provides an overview of the Blockchain API built with FastAPI, which serves as an interface to interact with a blockchain system stored in Redis. The API enables users to create and manage blocks, simulate user movement between zones, and retrieve information about the blockchain.

## Prerequisites

- Docker: Make sure you have Docker installed on your machine.

## Endpoints

### 1. POST /move

**Description:** This endpoint allows users to move a user from one zone to another in the blockchain.

**Parameters:**
- `person_id` (str): The ID of the user to be moved.
- `zone_id_orig` (int): The ID of the original zone from which the user is moved.
- `zone_id_dest` (int): The ID of the destination zone to which the user is moved.

**Response:**
- If the move is successful, the response will be "Transition Allowed!".
- If the user is not defined in the blockchain, the response will be "User Not defined in the Blockchain".
- If the user is not properly initialized on the blockchain, the response will be "User Not Properly Initialized on the Blockchain".
- If the original zone is not initialized on the blockchain, the response will be "Original Zone Not Initialized on the Blockchain".
- If the destination zone is not initialized on the blockchain, the response will be "Destination Zone Not Initialized on the Blockchain".
- If the user does not have authorization for the destination level, the response will be "User has no Authorization for the Destination Level".
- If the user is not in the original zone, the response will be "User not in the Original Zone".
- If another block was added before processing the request, the response will be "Another Block was added, please Repeat your Request!".

### 2. GET /info

**Description:** This endpoint retrieves information about the blockchain.

**Response:**
- The response will be a JSON object containing three lists:
  1. `Current_User_List`: A list of user data in the blockchain.
  2. `Current_Zone_List`: A list of zone data in the blockchain.
  3. `Current_UserLocation_State`: A list of user location data in the blockchain.

## Docker Configuration

To run the Blockchain API and the workers in Docker containers, you can use the provided Docker Compose configuration. Ensure that the `worker.py` and `app.py` scripts are placed in the respective worker and api directories.

```yaml
version: "3.8"

services:
  worker:
    build:
      context: ./worker
      dockerfile: Dockerfile
    restart: always
    environment:
      - REDIS_HOST=redis
    depends_on:
      - redis
    deploy:
      replicas: 2

  api:
    build:
      context: ./api
      dockerfile: Dockerfile
    restart: always
    environment:
      - REDIS_HOST=redis
    ports:
      - "8000:8000"
    depends_on:
      - redis

  redis:
    image: redis:latest
    ports:
      - "6379:6379"
    volumes:
      - redis_data:/data
    restart: always

volumes:
  redis_data:
```

The Docker Compose configuration sets up the following services:

1. `worker`: Runs the `worker.py` script in a worker Docker container. The number of replicas can be specified in the `replicas` field.

2. `api`: Runs the `app.py` script, which is the FastAPI application, in an API Docker container. The API is accessible on port 8000.

3. `redis`: Uses the Redis official image to run the Redis server in a container. The Redis data is stored in a volume for persistence.

## Usage

1. Ensure that you have Docker installed and the Docker daemon is running.

2. Place the `worker.py` and `app.py` scripts in the respective worker and api directories.

3. Create the Docker Compose file (`docker-compose.yml`) with the provided configuration.

4. Navigate to the directory containing the `docker-compose.yml` file in your terminal or command prompt.

5. Run the following command to start the worker and API services:

```bash
docker-compose up -d
```

6. The Blockchain API and workers will run in separate Docker containers, allowing you to interact with the blockchain through the API.

## Notes

- Ensure that you have the necessary permissions and firewall settings to run Docker containers on your machine.

- The provided scripts and Docker configuration serve as an illustrative example of a simple blockchain system and API. In a real-world scenario, you may need to consider additional security measures, scalability, and other factors for a robust and production-ready blockchain solution.

- It is recommended to run the Redis server in a separate container for better isolation and data persistence. In a production environment, you may also consider using Redis Sentinel or clustering for high availability and fault tolerance.