import grpc
from messages_pb2 import missile_details
from messages_pb2_grpc import DefenseNotificationStub
import random

channel = grpc.insecure_channel("172.17.85.111:50000")
stub = DefenseNotificationStub(channel)
x = random.randint(0, 9)
y = random.randint(0, 9)
request = missile_details(missile_type="m1", x=x, y=y, t=1)
print("MISSILE LAUNCHED...")
stub.launch_missile(request)
