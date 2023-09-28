import grpc
import numpy as np
import termtables as tt
import random
from concurrent import futures
from messages_pb2_grpc import (
    ControllerNotificationServicer,
    SoldierNotificationStub,
    add_ControllerNotificationServicer_to_server,
    DefenseNotificationStub,
)
from messages_pb2 import missile_details, Empty
from constants import SOLDIER_COUNT, SOLDIER_BASE_PORT, CONTROLLER_PORT, get_impact_area,BoardEdges,T,DEFENSE_SYSTEM_PORT,CONTROLLER_IP,SOLDIER_IP,DEFENSE_NOTIFICATION_IP
import numpy as np
import termtables as tt
import random
import logging
import sys
from io import StringIO
import _thread,threading,time

server = 0
# Parent Class to store the current situation
class BattleField:
    def __init__(self) -> None:
        self.current_commander = np.random.randint(0, SOLDIER_COUNT)
        logging.debug(f"The initial commander has been decided as soldier {self.current_commander}")
        self.all_soldiers = dict([(i, True) for i in range(SOLDIER_COUNT)])
        self.init_new_grid()
        self.t = 0

    def print_battlefield(self):
        tt.print(self.battle_grid)
        buffer = StringIO()
        old_stdout = sys.stdout
        sys.stdout = buffer
        tt.print(self.battle_grid)
        logging.debug(f"Current grid arrangement:\n{buffer.getvalue()}")
        sys.stdout = old_stdout

    def init_new_grid(self):
        self.battle_grid = np.empty((BoardEdges.RIGHT_X+1,BoardEdges.BOTTOM_Y+1), dtype=object)
        for i in range(self.battle_grid.shape[0]):
            for j in range(self.battle_grid.shape[1]):
                self.battle_grid[i][j] = " "


class ControllerNotificationService(ControllerNotificationServicer):
    def __init__(self) -> None:
        self.battlefield = BattleField()

        # Create and store soldier stubs
        self.soldier_stubs = {}
        for soldier in self.battlefield.all_soldiers.keys():
            channel = grpc.insecure_channel(f"{SOLDIER_IP}:{SOLDIER_BASE_PORT+soldier}")
            stub = SoldierNotificationStub(channel)
            self.soldier_stubs[soldier] = stub

        # need to do an initial poll of the soldier positions here
        alive_soldiers = self.get_alive_soldiers()

        for soldier in alive_soldiers:
            self.update_soldier_position(soldier)

        self.battlefield.print_battlefield()

    def kill_function(self):
        time.sleep(0.1)
        server.stop(0)
    # RPCs
    def missile_notification(self, request, context):
        if(self.battlefield.t>=T):
            alive_percentage = len(self.get_alive_soldiers())/SOLDIER_COUNT *100
            logging.debug(f"Time over. Currently {alive_percentage}% soldiers are alive.")
            if(alive_percentage>=50):
                logging.debug("The game has been won by the soldiers.")
            else:
                logging.debug("The game has been won by the enemies.")
            # TODO: Write the code to kill all processes here...
            # the current idea is to add a kill RPC to each service
            for soldier_no,stub in self.soldier_stubs.items():
                logging.debug(f"[[Killing soldier {soldier_no}]]")
                stub.kill(Empty())
            ds_channel = grpc.insecure_channel(f"{DEFENSE_NOTIFICATION_IP}:{DEFENSE_SYSTEM_PORT}")
            ds_stub = DefenseNotificationStub(ds_channel)
            ds_stub.kill(Empty())
            print("Now killing the controller")
            t = threading.Thread(target = self.kill_function)
            t.setDaemon(False)
            t.start()
            return Empty()
            #_thread.interrupt_main()
        else:
            print(
                f"Controller received missile notification!Arguments missile_type: {request.missile_type}, x: {request.x}, y: {request.y}, t: {request.t}"
            )

            #checking to see the game's ending condition
            logging.debug(f"[Time = {self.battlefield.t}]Currently there are {len(self.get_alive_soldiers())/SOLDIER_COUNT *100}% soldiers alive.")
            self.battlefield.t = self.battlefield.t + request.t

            logging.debug("Controller received missile notification.")
            stub = self.soldier_stubs.get(self.battlefield.current_commander)
            request = missile_details(missile_type=request.missile_type, x=request.x, y=request.y, t=request.t)
            stub.notify_commander(request)
            print("**Commander notified by controller**")
            logging.debug("Controller notified the current commander.")
            # update_commander_if_needed()
            return Empty()

    def notify_controller(self, request, context):
        print("notify_controller called. It will now notify all soldiers on behalf of the commander")
        logging.debug("Controller has been asked to broadcast the missile details to all soldiers.")
        self.notify_all_soldiers(request.missile_type, request.x, request.y, request.t)
        # now, we'll have to poll the status of each soldier and update the battlefield accordingly
        self.print_impact_area(request.missile_type, request.x, request.y)
        self.update_board_positions()
        return Empty()

    # Notify alive soldiers about incoming missile
    def notify_all_soldiers(self, missile_type, missile_x, missile_y, missile_t):
        alive_soldiers = self.get_alive_soldiers()
        for soldier in alive_soldiers:
            stub = self.soldier_stubs.get(soldier)
            request = missile_details(missile_type=missile_type, x=missile_x, y=missile_y, t=missile_t)
            empty_val = stub.notify_soldier(request)
            print(f"Soldier {soldier} notified of incoming missile!")
        logging.debug("Controller finished broadcasting to all soldiers.")
        print(self.get_alive_soldiers())

    def print_impact_area(self, missile_type, x, y):
        impact_area = get_impact_area(missile_type=missile_type, missile_x=x, missile_y=y)
        print(f"range({impact_area.left_x}, {impact_area.right_x+1})")
        print(f"range({impact_area.bottom_y},{impact_area.top_y+1})")
        for i in range(impact_area.left_x, impact_area.right_x + 1):
            for j in range(impact_area.top_y, impact_area.bottom_y + 1):
                if self.battlefield.battle_grid[j][i] == " ":
                    self.battlefield.battle_grid[j][i] = "*"
                    print(f"x:{i},y:{j})")

        self.battlefield.print_battlefield()

    # Commander re-election also happens here
    def update_board_positions(self):
        self.battlefield.init_new_grid()
        self.update_soldier_status()
        alive_soldiers = self.get_alive_soldiers()
        if self.battlefield.current_commander not in alive_soldiers:
            new_commander_index = random.randint(0, len(alive_soldiers) - 1)
            print(
                f"The commander [Soldier {self.battlefield.current_commander}] is dead. The new commander will now be {alive_soldiers[new_commander_index]}"
            )
            logging.debug(
                f"The commander [Soldier {self.battlefield.current_commander}] is dead. The new commander will now be {alive_soldiers[new_commander_index]}"
            )
            self.battlefield.current_commander = alive_soldiers[new_commander_index]
            # now,we'll call the make commander RPC in the soldier to notify it that it has been elected as the new commander
            stub = self.soldier_stubs.get(self.battlefield.current_commander)
            stub.make_commander(Empty())
            logging.debug(
                f"The newly elected commander [{self.battlefield.current_commander}] has been notified of his new position."
            )
        print("NEW COMMANDER ELECTION COMPLETE.")
        # print("update_board called.")
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
        if self.battlefield.battle_grid[pos_reply.y][pos_reply.x] == " ":
            self.battlefield.battle_grid[pos_reply.y][pos_reply.x] = str(soldier)
        else:
            self.battlefield.battle_grid[pos_reply.y][pos_reply.x] += f" {soldier}"
        # print(f"Soldier {soldier}'s position polled at {pos_reply.x},{pos_reply.y}")

    # Polls soldiers for liveness and updates their status in the battlefield
    def update_soldier_status(self):
        logging.debug("Now polling all soldiers after the impact.")

        for soldier in self.battlefield.all_soldiers.keys():
            stub = self.soldier_stubs.get(soldier)
            request = Empty()
            survival_reply = stub.soldier_status(request)
            self.battlefield.all_soldiers[soldier] = survival_reply.is_alive
        logging.debug(f"Remaining alive soldiers: {len(self.get_alive_soldiers())}")

    # Return only alive soldiers from all_soldiers
    def get_alive_soldiers(self):
        alive_soldiers = []
        for soldier, status in self.battlefield.all_soldiers.items():
            if status == True:
                alive_soldiers.append(soldier)
        return alive_soldiers


def serve():
    global server
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=20))
    add_ControllerNotificationServicer_to_server(ControllerNotificationService(), server)
    server.add_insecure_port(f"{CONTROLLER_IP}:{CONTROLLER_PORT}")
    server.start()
    print("Controller STARTED....")
    server.wait_for_termination()


if __name__ == "__main__":
    logging.basicConfig(filename="output.log", filemode="a", format="%(asctime)s - %(message)s", level=logging.DEBUG)
    serve()
