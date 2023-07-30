import redis
import json
from datetime import datetime, timedelta

redis_client = redis.StrictRedis(host="localhost", port=6379, decode_responses=True)
last_update = json.loads(redis_client.get("update"))




while True:
    current_update = json.loads(redis_client.get("update"))

    datetime_last_update = datetime.strptime(current_update["last_update"], "%Y-%m-%d %H:%M:%S.%f")
    datetime_current_update = datetime.strptime(current_update["datetime"], "%Y-%m-%d %H:%M:%S.%f")
    time_difference = datetime_current_update - datetime_last_update
    
    if current_update != last_update:
        print(str(datetime.now()) + "------>" + str((time_difference).total_seconds()))
        last_update = json.loads(redis_client.get("update"))