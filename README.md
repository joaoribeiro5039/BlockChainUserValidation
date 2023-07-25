# FastAPI Blockchain-based User Validation Documentation

This documentation provides details about the FastAPI application for blockchain-based user validation. The application uses a blockchain to store user validation data securely and exposes APIs to interact with the blockchain.

## Prerequisites

- Python 3.7+
- FastAPI
- Pydantic
- Web3.py (Python library for interacting with Ethereum blockchain)
- Redis (a fast in-memory data structure store used as a database)

## Setup

1. Install Python: Ensure you have Python 3.7 or a higher version installed on your system.

2. Install FastAPI: Use pip to install FastAPI.

```bash
pip install fastapi
```

3. Install Pydantic: Pydantic is used for data validation and serialization.

```bash
pip install pydantic
```

4. Install Web3.py: Web3.py is required to interact with the blockchain.

```bash
pip install web3
```

5. Install Redis: Install Redis server or use a cloud service for Redis.

## Application Overview

The FastAPI application provides a blockchain-based user validation system. Users can be validated and added to the blockchain, and the blockchain will store the user validation data securely. Additionally, the application supports forging new blocks for user validation through API requests.

### Data Model

The data model for user validation is represented by the `Block` class. Each block contains user validation information.

```python
class Block:
    def __init__(self, index, timestamp, data, previous_hash, nonce=0, hash=None):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.nonce = 0
        self.hash = self.calculate_hash() if hash is None else hash

    def calculate_hash(self):
        data_str = f"{self.index}{self.timestamp}{self.data}{self.previous_hash}{self.nonce}"
        return hashlib.sha256(data_str.encode('utf-8')).hexdigest()

    def is_valid(self, difficulty):
        target = "0" * difficulty
        return self.hash[:difficulty] == target
```

### Endpoints

The FastAPI application exposes the following endpoints:

1. **Forge New Block** - Forges a new block for user validation and stores it on the blockchain.

   **Endpoint:** `/forge`

   **HTTP Method:** POST

   **Request Body:**

   ```json
   {
       "person_id": "user123",
       "authorization_id": "auth456",
       "zone_id_orig": "zoneA",
       "zone_id_dest": "zoneB"
   }
   ```

   **Response:**

   - `200 OK` with the response body containing a success message.

2. **Get Blocks** - Retrieves all the blocks in the blockchain.

   **Endpoint:** `/blocks`

   **HTTP Method:** GET

   **Response:**

   - `200 OK` with the response body containing the list of blocks in the blockchain.

## Blockchain Interaction

The application uses Redis to store the blockchain data. The `Blockchain` class manages the blockchain and provides functions for adding blocks and validating the chain.

## Usage

1. Ensure Redis server is running or use a cloud Redis service.

2. Run the FastAPI application.

```bash
uvicorn app:app --host 127.0.0.1 --port 8000
```

3. The FastAPI application will now be running on `http://localhost:8000`.

4. Use API clients like `curl`, `httpie`, or any other tool to interact with the API.

## Security Considerations

1. Ensure that the Redis server is secure and properly configured.

2. Implement authentication and authorization mechanisms to protect sensitive endpoints and operations.

3. Use HTTPS to secure communication with the API.

## Conclusion

This documentation provides an overview of the FastAPI application for blockchain-based user validation. By utilizing blockchain technology, the application ensures data integrity and transparency, making it suitable for various use cases that require secure and tamper-resistant validation. Ensure to follow the security considerations to maintain the robustness of the application.