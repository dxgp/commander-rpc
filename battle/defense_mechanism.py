import grpc
from concurrent import futures
from messages_pb2_grpc import (
    DefenseNotificationServicer,
    CommanderNotificationStub,
    add_DefenseNotificationServicer_to_server,
)
from messages_pb2 import Empty, missile_details


class DefenseNotificationService(DefenseNotificationServicer):
    def launch_missile(self, request, context):
        print("In launch missile******")
        # Call Commander notification service
        # Create commander stub object
        commander_channel = grpc.insecure_channel("localhost:50001")
        commander_stub = CommanderNotificationStub(commander_channel)
        # Send missile details to commander
        comm_request = missile_details(missile_type=request.missile_type, x=request.x, y=request.y, t=request.t)
        commander_stub.missile_notification(comm_request)
        return Empty()


def serve():
    print("****Server started")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_DefenseNotificationServicer_to_server(DefenseNotificationService(), server)
    server.add_insecure_port("localhost:50000")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
