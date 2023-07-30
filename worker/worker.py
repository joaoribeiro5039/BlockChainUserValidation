import hashlib
import redis
from pydantic import BaseModel
import json
from datetime import datetime
import random
import os
import time

global REDIS_Host
REDIS_Host = os.getenv("REDIS_HOST")
if REDIS_Host is None:
    REDIS_Host = "localhost"

global REFRESH_Rate
REFRESH_Rate_env = os.getenv("REFRESH_RATE")
if REFRESH_Rate_env is None:
    REFRESH_Rate = 1.0
else:
    REFRESH_Rate = float(REFRESH_Rate_env)


def clear_redis_data(host, port, password=None, db=0):
    try:
        # Connect to Redis
        r = redis.StrictRedis(host=host, port=port, password=password, db=db)

        # Flush all data from the selected Redis database
        r.flushall()

        print("All data in Redis has been cleared.")
    except redis.exceptions.ConnectionError as e:
        print(f"Error connecting to Redis: {e}")






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


# Initialize Redis client
redis_client = redis.StrictRedis(host=REDIS_Host, port=6379, decode_responses=True)


latest_Data = redis_client.get("update")
if latest_Data is None:
    
    redis_host = REDIS_Host
    redis_port = 6379
    redis_password = None  # Set the password if your Redis server requires authentication
    redis_db = 0  # The database number, usually 0
    
    clear_redis_data(redis_host, redis_port, redis_password, redis_db)
    
    
    genesis_block = Create_Genesis_Block()
    redis_client.set(genesis_block.hash, json.dumps(genesis_block, cls=Block.BlockEncoder))
    Blockchain_Data ={
        "last_update":str(datetime.now()),
        "datetime":str(datetime.now()),
        "BlockChain_Size":1,
        "BlockChain_LastHash":genesis_block.hash
    }

    User_List= []
    for i in range(100):
        obj ={
            "User_ID": str(i),
            "AuthorizationLevel_ID": [random.randint(1, 10) for _ in range(3)]
            }
        User_List.append(obj)

    for user in User_List:
        current_block = Create_User_Block(Blockchain_Data["BlockChain_Size"], user["User_ID"], json.dumps(user["AuthorizationLevel_ID"]),Blockchain_Data["BlockChain_LastHash"])
        Blockchain_Data["BlockChain_Size"] += 1
        Blockchain_Data["datetime"] = str(datetime.now())
        Blockchain_Data["BlockChain_LastHash"] = current_block.hash
        redis_client.set(current_block.hash, json.dumps(current_block, cls=Block.BlockEncoder))
        redis_client.set("update",json.dumps(Blockchain_Data))
        
        #Move User to ZoneID 0
        current_block = Create_Move_Block(Blockchain_Data["BlockChain_Size"], user["User_ID"],0,0,Blockchain_Data["BlockChain_LastHash"])
        Blockchain_Data["BlockChain_Size"] += 1
        Blockchain_Data["datetime"] = str(datetime.now())
        Blockchain_Data["BlockChain_LastHash"] = current_block.hash
        redis_client.set(current_block.hash, json.dumps(current_block, cls=Block.BlockEncoder))
        redis_client.set("update",json.dumps(Blockchain_Data))


    Zones= []
    for i in range(10):
        obj ={
            "Zone_ID": i,
            "Required_Level_ID": random.randint(2, 4)
            }
        Zones.append(obj)

    for zones in Zones:
        current_block = Create_Zone_Block(Blockchain_Data["BlockChain_Size"], zones["Zone_ID"], zones["Required_Level_ID"],Blockchain_Data["BlockChain_LastHash"])
        Blockchain_Data["BlockChain_Size"] += 1
        Blockchain_Data["datetime"] = str(datetime.now())
        Blockchain_Data["BlockChain_LastHash"] = current_block.hash
        redis_client.set(current_block.hash, json.dumps(current_block, cls=Block.BlockEncoder))
        redis_client.set("update",json.dumps(Blockchain_Data))


while True:
    Current_User_List = []
    Current_UserLocation_State = []

    Current_Zone_List = []

    blockchain_data = json.loads(redis_client.get("update"))
    size = blockchain_data["BlockChain_Size"]
    last_hash = blockchain_data["BlockChain_LastHash"]
    Current_hash = last_hash
    counter = 0
    for i in range(size, -1, -1):
        # print(i)
        if i == 0:
            datetime_last_update = datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f")
            datetime_current_update = datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f")
            time_difference = datetime_current_update - datetime_last_update
            update_in_Seconds = (time_difference).total_seconds()
            while update_in_Seconds < REFRESH_Rate:
                new_blockchain_data = json.loads(redis_client.get("update"))
                datetime_current_update = datetime.strptime(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f")
                datetime_last_update = datetime.strptime(new_blockchain_data["datetime"], "%Y-%m-%d %H:%M:%S.%f")
                time_difference = datetime_current_update - datetime_last_update
                update_in_Seconds = (time_difference).total_seconds()
                if update_in_Seconds < REFRESH_Rate:
                    time.sleep((REFRESH_Rate-update_in_Seconds)*random.uniform(0.75, 1.0))

            if new_blockchain_data["BlockChain_LastHash"] == blockchain_data["BlockChain_LastHash"]:
                new_blockchain_data["last_update"] = new_blockchain_data["datetime"]
                new_blockchain_data["datetime"] = str(datetime.now())
                redis_client.set("Current_User_List",json.dumps(Current_User_List))
                redis_client.set("Current_Zone_List",json.dumps(Current_Zone_List))
                redis_client.set("Current_UserLocation_State",json.dumps(Current_UserLocation_State))
                redis_client.set("update",json.dumps(new_blockchain_data))
                    

            break

        else:

            Current_Block = json.loads(redis_client.get(Current_hash))
            
            if str(Current_Block["data"]).__contains__("AuthorizationLevel_ID"):
                data = Current_Block["data"]
                block_data = {
                        "User_ID": data["User_ID"],
                        "AuthorizationLevel_ID": data["AuthorizationLevel_ID"]
                    }
                if len(Current_User_List)>0:
                    if block_data not in Current_User_List:
                        Current_User_List.append(block_data)
                else:
                    Current_User_List.append(block_data)


            elif str(Current_Block["data"]).__contains__("Zone_ID"):
                
                data = Current_Block["data"]
                
                block_data = {
                        "Zone_ID": data["Zone_ID"],
                        "RequiredLevel_ID": data["RequiredLevel_ID"]
                    }
                
                if len(Current_Zone_List)>0:
                    if block_data not in Current_Zone_List:
                        Current_Zone_List.append(block_data)
                else:
                    Current_Zone_List.append(block_data)

            elif str(Current_Block["data"]).__contains__("To_ID"):
                
                data = Current_Block["data"]

                block_data = {
                        "User_ID": data["User_ID"],
                        "Zone_ID": data["To_ID"]
                    }
                
                if len(Current_UserLocation_State)>0:
                    user_ids = [user_data["User_ID"] for user_data in Current_UserLocation_State]
                    if block_data["User_ID"] not in user_ids:
                        Current_UserLocation_State.append(block_data)
                else:
                    Current_UserLocation_State.append(block_data)




        counter += 1
        Current_hash = Current_Block["previous_hash"]
                                                 

