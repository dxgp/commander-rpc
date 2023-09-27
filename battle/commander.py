import grpc
from concurrent import futures
from messages_pb2_grpc import (
    CommanderNotificationServicer,
    SoldierNotificationStub,
    add_CommanderNotificationServicer_to_server,
)
from messages_pb2 import missile_details, Empty
from constants import SOLDIER_COUNT,get_impact_area
import numpy as np
import termtables as tt



# Parent Class to store the current situation
class BattleField:
    def __init__(self) -> None:
        self.current_commander = np.random.randint(0, SOLDIER_COUNT)
        self.all_soldiers = dict([(i, True) for i in range(SOLDIER_COUNT)])
        self.init_new_grid()

    def print_battlefield(self):
        tt.print(self.battle_grid)
    def init_new_grid(self):
        self.battle_grid = np.empty((10, 10), dtype=object)
        for i in range(self.battle_grid.shape[0]):
            for j in range(self.battle_grid.shape[1]):
                self.battle_grid[i][j] = " "


class CommanderNotificationService(CommanderNotificationServicer):
    def __init__(self) -> None:
        self.battlefield = BattleField()

        # Create and store soldier stubs
        self.soldier_stubs = {}
        for soldier in self.battlefield.all_soldiers.keys():
            channel = grpc.insecure_channel(f"localhost:{60000+soldier}")
            stub = SoldierNotificationStub(channel)
            self.soldier_stubs[soldier] = stub

        # need to do an initial poll of the soldier positions here
        alive_soldiers = self.get_alive_soldiers()

        for soldier in alive_soldiers:
            self.update_soldier_position(soldier)

        self.battlefield.print_battlefield()

    def missile_notification(self, request, context):
        print(
            f"Commander received missile notification!Arguments missile_type: {request.missile_type}, x: {request.x}, y: {request.y}, t: {request.t}"
        )
        self.notify_all_soldiers(request.missile_type, request.x, request.y, request.t)
        # now, we'll have to poll the status of each soldier and update the battlefield accordingly
        self.print_impact_area(request.missile_type,request.x,request.y)
        self.update_board_positions()
        # update_commander_if_needed()
        return Empty()

    # Notify alive soldiers about incoming missile
    def notify_all_soldiers(self, missile_type, missile_x, missile_y, missile_t):
        alive_soldiers = self.get_alive_soldiers()
        for soldier in alive_soldiers:
            stub = self.soldier_stubs.get(soldier)
            request = missile_details(missile_type=missile_type, x=missile_x, y=missile_y, t=missile_t)
            empty_val = stub.notify_soldier(request)
            print(f"Soldier {soldier} notified of incoming missile!")
        print(self.get_alive_soldiers())

    def print_impact_area(self,missile_type, x,y):
        impact_area = get_impact_area(missile_type=missile_type, missile_x=x, missile_y=y)
        print(f"range({impact_area.left_x}, {impact_area.right_x+1})")
        print(f"range({impact_area.bottom_y},{impact_area.top_y+1})")
        for i in range(impact_area.left_x, impact_area.right_x+1):
            for j in range(impact_area.bottom_y,impact_area.top_y+1):
                if(self.battlefield.battle_grid[j][i]==" "):
                    self.battlefield.battle_grid[j][i] = "*"
                    print(f"x:{i},y:{j})")
        self.battlefield.print_battlefield()
    def update_board_positions(self):
        self.battlefield.init_new_grid()
        self.update_soldier_status()
        alive_soldiers = self.get_alive_soldiers()
        print("update_board called.")
        print(alive_soldiers)
        for soldier in alive_soldiers:
            self.update_soldier_position(soldier)

        self.battlefield.print_battlefield()

    # Polls a soldier for position and updates it in the battlefield
    def update_soldier_position(self, soldier):
        stub = self.soldier_stubs.get(soldier)
        request = Empty()
        pos_reply = stub.soldier_position(request)
        print("update_soldier_position called.")
        if self.battlefield.battle_grid[pos_reply.x][pos_reply.y] == " ":
            self.battlefield.battle_grid[pos_reply.x][pos_reply.y] = str(soldier)
        else:
            self.battlefield.battle_grid[pos_reply.x][pos_reply.y] += f" {soldier}"

        print(f"Soldier {soldier}'s position polled at {pos_reply.x},{pos_reply.y}")

    # Polls soldiers for liveness and updates their status in the battlefield
    def update_soldier_status(self):
        for soldier in self.battlefield.all_soldiers.keys():
            stub = self.soldier_stubs.get(soldier)
            request = Empty()
            survival_reply = stub.soldier_status(request)
            self.battlefield.all_soldiers[soldier] = survival_reply.is_alive

    # Return only alive soldiers from all_soldiers
    def get_alive_soldiers(self):
        alive_soldiers = []
        for soldier, status in self.battlefield.all_soldiers.items():

            if status == True:
                alive_soldiers.append(soldier)
        return alive_soldiers


def serve():
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=10))
    add_CommanderNotificationServicer_to_server(CommanderNotificationService(), server)
    server.add_insecure_port("localhost:50001")
    server.start()
    print("COMMANDER STARTED....")
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
