import grpc
from concurrent import futures
from messages_pb2_grpc import CommanderNotificationServicer, SoldierNotificationStub, add_CommanderNotificationServicer_to_server
from messages_pb2 import missile_details, Empty

class CommanderNotificationService(CommanderNotificationServicer):
    def missile_notification(self, request, context):
        print(f"Commander received missile notification!Arguments missile_type: {request.missile_type}, x: {request.x}, y: {request.y}, t: {request.t}")
        # channel = grpc.insecure_channel("localhost:50002")
        # stub = SoldierNotificationStub(channel)
        # request = missile_details(missile_type = request.missile_type, x = request.x, y = request.y, t = request.t)
        # stub.notify_soldier(request)\
        notify_all_soldiers(request.missile_type, request.x, request.y, request.t)
        return Empty()
    
def notify_all_soldiers(missile_type, missile_x, missile_y, missile_t):
    for i in range(0, 2):
        channel = grpc.insecure_channel(f"localhost:{50002+i}")
        stub = SoldierNotificationStub(channel)
        request = missile_details(missile_type = missile_type, x = missile_x, y = missile_y, t = missile_t)
        stub.notify_soldier(request)
        print(f"Soldier {i} notified of incoming missile!")
def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_CommanderNotificationServicer_to_server(CommanderNotificationService(), server)
    server.add_insecure_port("localhost:50001")
    server.start()
    server.wait_for_termination()

if __name__=='__main__':
    serve()
    