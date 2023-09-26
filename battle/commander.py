import grpc
from concurrent import futures
from messages_pb2_grpc import (
    CommanderNotificationServicer,
    SoldierNotificationStub,
    add_CommanderNotificationServicer_to_server,
)
from messages_pb2 import missile_details, Empty
from constants import SOLDIER_COUNT


class CommanderNotificationService(CommanderNotificationServicer):
    def missile_notification(self, request, context):
        print(
            f"Commander received missile notification!Arguments missile_type: {request.missile_type}, x: {request.x}, y: {request.y}, t: {request.t}"
        )
        notify_all_soldiers(request.missile_type, request.x, request.y, request.t)
        return Empty()


def notify_all_soldiers(missile_type, missile_x, missile_y, missile_t):
    for i in range(SOLDIER_COUNT):
        channel = grpc.insecure_channel(f"localhost:{50002+i}")
        stub = SoldierNotificationStub(channel)
        request = missile_details(missile_type=missile_type, x=missile_x, y=missile_y, t=missile_t)
        empty_val = stub.notify_soldier(request)
        print(f"Soldier {i+1} notified of incoming missile!")


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_CommanderNotificationServicer_to_server(CommanderNotificationService(), server)
    server.add_insecure_port("localhost:50001")
    server.start()
    print("COMMANDER STARTED....")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
