import hashlib
import time
import threading
import redis
from fastapi import FastAPI
from pydantic import BaseModel
import json
from datetime import datetime, timedelta
import random
import os

global REDIS_Host
REDIS_Host = os.getenv("REDIS_HOST")
if REDIS_Host is None:
    REDIS_Host = "localhost"


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


class Blockchain:
    def __init__(self):
        self.chain = [self.create_genesis_block()]
        self.difficulty = 0  # Adjust this to control the mining difficulty

    def create_genesis_block(self):
        return Block(0, datetime.now(), {"Person_ID": "", "Authorization_ID": "", "Zone_ID": ""}, "0", 0, "0")

    def get_latest_block(self):
        return self.chain[-1]

    def add_block(self, new_block):
        new_block.previous_hash = self.get_latest_block().hash
        new_block.hash = new_block.calculate_hash()  # PoS doesn't use mining, so we just set the hash directly
        self.chain.append(new_block)

    def is_chain_valid(self):
        for i in range(1, len(self.chain)):
            current_block = self.chain[i]
            previous_block = self.chain[i - 1]

            if current_block.hash != current_block.calculate_hash():
                return False

            if current_block.previous_hash != previous_block.hash:
                return False

        return True


class Validator:
    def validate_User(self, blockchain, person_id, authorization_id, zone_id_orig,zone_id_dest):
        data = {"Person_ID": person_id, "Authorization_ID": authorization_id, "Zone_ID_Orig": zone_id_orig, "Zone_ID_Dest": zone_id_dest}
        new_block = Block(len(blockchain.chain), datetime.now(), data, "")
        blockchain.add_block(new_block)
        print(f"Forged a new block #{new_block.index} - Hash: {new_block.hash}")
    def validate_Zones(self, blockchain, Zone_ID, Wait_Time):
        data = {"Zone_ID": Zone_ID, "Wait_Time": Wait_Time}
        new_block = Block(len(blockchain.chain), datetime.now(), data, "")
        blockchain.add_block(new_block)
        print(f"Forged a new block #{new_block.index} - Hash: {new_block.hash}")


class BlockEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Block):
            return obj.__dict__
        if isinstance(obj, datetime):
            return obj.isoformat()
        return json.JSONEncoder.default(self, obj)


app = FastAPI()

# Initialize Redis client
redis_client = redis.StrictRedis(host=REDIS_Host, port=6379, decode_responses=True)

@app.post("/forge")
async def forge_new_block(person_id, authorization_id, zone_id_orig,zone_id_dest):
    current_time = str(datetime.now())
    datetime_current_time = datetime.strptime(current_time, "%Y-%m-%d %H:%M:%S.%f")
    time_difference = datetime_current_time - datetime_current_time
    # Create a timedelta object representing 1 second
    one_second = timedelta(seconds=1)
    while time_difference < one_second:
        last_update = redis_client.get("update")
        datetime_last_update = datetime.strptime(last_update, "%Y-%m-%d %H:%M:%S.%f")
        time_difference = datetime_last_update - datetime_current_time
    
    blockchain_data = redis_client.get("blockchain")
    if blockchain_data:
        blockchain_chain = json.loads(blockchain_data)
        blockchain = Blockchain()
        blockchain.chain = [Block(**block_data) for block_data in blockchain_chain]
    else:
        blockchain = Blockchain()

    current_validator = Validator()
    current_validator.validate_User(blockchain, person_id, authorization_id, zone_id_orig,zone_id_dest)

    # Save the updated blockchain to Redis
    redis_client.set("blockchain", json.dumps(blockchain.chain, cls=BlockEncoder))

    return {"message": "Block forged with Person: " + person_id +
                        " With Authorization: " + authorization_id +
                        " Entering Zone: " + zone_id_dest +
                        " From Zone: " + zone_id_orig}

@app.get("/blocks")
async def get_blocks():
    blockchain_data = redis_client.get("blockchain")
    if blockchain_data:
        blockchain_chain = json.loads(blockchain_data)
        blockchain = Blockchain()
        blockchain.chain = [Block(**block_data) for block_data in blockchain_chain]
        return {"blocks": blockchain.chain}
    else:
        return {"blocks": []}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
