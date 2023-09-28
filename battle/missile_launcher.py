import grpc
from messages_pb2 import missile_details
from messages_pb2_grpc import DefenseNotificationStub
import random
from constants import MissileType,BoardEdges

channel = grpc.insecure_channel("localhost:50000")
stub = DefenseNotificationStub(channel)

# Missile params
x = random.randint(0, BoardEdges.RIGHT_X)
y = random.randint(0, BoardEdges.BOTTOM_Y)
# x, y = 5, 5
missile_type = MissileType.M3

request = missile_details(missile_type=missile_type, x=x, y=y, t=1)
print("MISSILE LAUNCHED...")
stub.launch_missile(request)
