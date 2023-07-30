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
import uvicorn

global REDIS_Host
REDIS_Host = os.getenv("REDIS_HOST")
if REDIS_Host is None:
    REDIS_Host = "localhost"

class Block:
    def __init__(self, index, timestamp, data, previous_hash, hash=None):
        self.index = index
        self.timestamp = timestamp
        self.data = data
        self.previous_hash = previous_hash
        self.hash = self.calculate_hash() if hash is None else hash

    def calculate_hash(self):
        data_str = f"{self.index}{self.timestamp}{self.previous_hash}"
        return hashlib.sha256(data_str.encode('utf-8')).hexdigest()

    def is_valid(self, difficulty):
        target = "0" * difficulty
        return self.hash[:difficulty] == target
    
    class BlockEncoder(json.JSONEncoder):
        def default(self, obj):
            if isinstance(obj, Block):
                return obj.__dict__
            return json.JSONEncoder.default(self, obj)


def Create_Genesis_Block():
    data = {"Genesis": True}
    return Block(0, str(datetime.now()), data, "0")

def Create_User_Block(index, user_ID, authorizationlevel_id, prev_hash):
    data = {"User_ID": user_ID, "AuthorizationLevel_ID": authorizationlevel_id}
    return Block(index, str(datetime.now()), data, prev_hash)

def Create_Zone_Block(index, Zone_ID, RequiredLevel_ID, prev_hash):
    data = {"Zone_ID": Zone_ID,"RequiredLevel_ID": RequiredLevel_ID}
    return Block(index, str(datetime.now()), data, prev_hash)

def Create_Move_Block(index, user_ID, from_id, to_id, prev_hash):
    data = {"User_ID": user_ID, "From_ID": from_id, "To_ID": to_id}
    return Block(index, str(datetime.now()), data, prev_hash)






app = FastAPI()

@app.post("/move")
async def forge_new_block(person_id, zone_id_orig , zone_id_dest):
    
    zone_id_orig = int(zone_id_orig)
    zone_id_dest = int(zone_id_dest)
    redis_client = redis.StrictRedis(host=REDIS_Host, port=6379, decode_responses=True)
    
    update_flag = True
    last_update = json.loads(redis_client.get("update"))
    while update_flag:
        current_update = json.loads(redis_client.get("update"))
        if current_update != last_update:
            update_flag = False
            

    Current_User_List = json.loads(redis_client.get("Current_User_List"))
    Current_Zone_List = json.loads(redis_client.get("Current_Zone_List"))
    Current_UserLocation_State = json.loads(redis_client.get("Current_UserLocation_State"))
    Current_User = None
    for user in Current_User_List:
        if user["User_ID"] == person_id:
            Current_User = user
            break
    if Current_User is None:
        return "User Not defined in the BlockChain"
    Current_User_Location = None
    for user_location in Current_UserLocation_State:
        if user_location["User_ID"] == person_id:
            Current_User_Location = user_location
            break
    if Current_User_Location is None:
        return "User Not Properly Inicialized on the BlockChain"
    
    Original_Zone = None
    Destination_Zone = None
    for zone in Current_Zone_List:
        print(zone)
        if zone["Zone_ID"] == zone_id_orig:
            Original_Zone = zone
        elif zone["Zone_ID"] == zone_id_dest:
            Destination_Zone = zone
    if Original_Zone is None:
        return "Original Zone Not Inicialized on the BlockChain"
    if Destination_Zone is None:
        return "Destination Zone Not Inicialized on the BlockChain"


    if Destination_Zone["RequiredLevel_ID"] in json.loads(Current_User["AuthorizationLevel_ID"]) and Current_User_Location["Zone_ID"] == Original_Zone["Zone_ID"]:

        Current_update = json.loads(redis_client.get("update"))
        if last_update["BlockChain_LastHash"] == Current_update["BlockChain_LastHash"] and last_update["BlockChain_Size"] == Current_update["BlockChain_Size"]:
            Blockchain_Data ={
                "last_update":Current_update["datetime"],
                "datetime":Current_update["datetime"],
                "BlockChain_Size":Current_update["BlockChain_Size"]+1,
                "BlockChain_LastHash":Current_update["BlockChain_LastHash"]
            }
            current_block = Create_Move_Block(Current_update["BlockChain_Size"]+1, person_id, zone_id_orig, zone_id_dest, Current_update["BlockChain_LastHash"])
            Blockchain_Data["datetime"] = Current_update["datetime"]
            Blockchain_Data["BlockChain_LastHash"] = current_block.hash
            redis_client.set(current_block.hash, json.dumps(current_block, cls=Block.BlockEncoder))
            redis_client.set("update",json.dumps(Blockchain_Data))
            return "Transition Allowed!"
        else:
            print("Another Block was added, please Repeat your Request!")
    else:
        if Destination_Zone["RequiredLevel_ID"] not in json.loads(Current_User["AuthorizationLevel_ID"]):
            return "User has no Autorization for the destination Level"
        elif Current_User_Location["Zone_ID"] == Original_Zone["Zone_ID"]:
            return "User has no Autorization for the destination Level"
        else:
            return "User not in the Original Zone"


@app.get("/info")
async def get_blocks():
    
    redis_client = redis.StrictRedis(host=REDIS_Host, port=6379, decode_responses=True)
    Data = []
    Current_User_List = json.loads(redis_client.get("Current_User_List"))
    Data.append(Current_User_List)
    Current_Zone_List = json.loads(redis_client.get("Current_Zone_List"))
    Data.append(Current_Zone_List)
    Current_UserLocation_State = json.loads(redis_client.get("Current_UserLocation_State"))
    Data.append(Current_UserLocation_State)

    return Data
       
# Start the OPC UA server and the task to send OPC values to Redis
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)