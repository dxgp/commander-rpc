import grpc
from concurrent import futures
from messages_pb2_grpc import (
    DefenseNotificationServicer,
    ControllerNotificationStub,
    add_DefenseNotificationServicer_to_server,
)
from messages_pb2 import Empty, missile_details
from constants import DEFENSE_SYSTEM_PORT,CONTROLLER_PORT
import threading,time,_thread

server = 0

class DefenseNotificationService(DefenseNotificationServicer):
    def launch_missile(self, request, context):
        print("In launch missile******")
        # Call Commander notification service
        # Create commander stub object
        controller_channel = grpc.insecure_channel(f"localhost:{CONTROLLER_PORT}")
        controller_stub = ControllerNotificationStub(controller_channel)
        # Send missile details to commander
        comm_request = missile_details(missile_type=request.missile_type, x=request.x, y=request.y, t=request.t)
        controller_stub.missile_notification(comm_request)
        return Empty()
    def kill(self,request,context):
        print("Killing defense process...")
        t = threading.Thread(target = self.kill_function)
        t.setDaemon(False)
        t.start()
        return Empty()
    
    def kill_function(self):
        time.sleep(0.1)
        server.stop(0)


def serve():
    global server
    print("****Server started")
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_DefenseNotificationServicer_to_server(DefenseNotificationService(), server)
    server.add_insecure_port(f"localhost:{DEFENSE_SYSTEM_PORT}")
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
