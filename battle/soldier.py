import grpc
from concurrent import futures
from messages_pb2_grpc import SoldierNotificationServicer, add_SoldierNotificationServicer_to_server
from messages_pb2 import missile_details, Empty, survival_response
import sys
import random


is_alive = True
soldier_speed = random.randint(0,5)
soldier_number = 0

def can_survive(mtype, x, y, t):
    return True
class SoldierNotificationService(SoldierNotificationServicer):
    def notify_soldier(self, request, context):
        print(f"Soldier {soldier_number} received missile notification from commander! Calculating survival!")
        missile_x = request.x
        missile_y = request.y
        time_remaining = request.t
        missile_type = request.missile_type
        survive = can_survive(missile_type, missile_x, missile_y, time_remaining)
        is_alive = survive
        return Empty()
    def soldier_status(self, request, context):
        print("Soldier status polled...")
        survival = survival_response(is_alive = is_alive)
        return survival
        
def serve():
    global soldier_number
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    add_SoldierNotificationServicer_to_server(SoldierNotificationService(), server)
    server.add_insecure_port(f"localhost:{sys.argv[1]}")
    soldier_number = (int(sys.argv[1]) - 50002 + 1)
    server.start()
    server.wait_for_termination()

if __name__=='__main__':
    serve()