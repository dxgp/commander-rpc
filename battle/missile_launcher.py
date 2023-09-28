import grpc
from messages_pb2 import missile_details
from messages_pb2_grpc import DefenseNotificationStub
import random
from constants import MissileType, BoardEdges, t, T, DEFENSE_NOTIFICATION_IP
import time


channel = grpc.insecure_channel(f"{DEFENSE_NOTIFICATION_IP}:50000")
stub = DefenseNotificationStub(channel)

# Missile params

starttime = time.time()
local_t = 0
while local_t <= T:
    local_t += t
    x = random.randint(0, BoardEdges.RIGHT_X)
    y = random.randint(0, BoardEdges.BOTTOM_Y)

    missile_types = [MissileType.M1, MissileType.M2, MissileType.M3, MissileType.M4]
    missile_random_index = random.randint(0, len(missile_types) - 1)

    missile_type = missile_types[missile_random_index]
    request = missile_details(missile_type=missile_type, x=x, y=y, t=t)
    print("MISSILE LAUNCHED...")
    stub.launch_missile(request)

    # Remove the Time taken by code to execute
    time.sleep(t - ((time.time() - starttime) % t))
