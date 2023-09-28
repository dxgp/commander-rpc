import grpc
import random
import sys
from concurrent import futures
from messages_pb2_grpc import (
    SoldierNotificationServicer,
    add_SoldierNotificationServicer_to_server,
    ControllerNotificationStub,
)
from messages_pb2 import Empty, survival_response, position_details, missile_details

from constants import Direction, BoardEdges, get_impact_area, CONTROLLER_PORT,SOLDIER_IP
import threading
import time
import _thread
server = 0

class Soldier:
    def __init__(self, soldier_number) -> None:
        self.x = random.randint(0, BoardEdges.RIGHT_X)
        self.y = random.randint(0, BoardEdges.BOTTOM_Y)
        # self.x = 5
        # self.y = 5
        # self.speed = 2
        self.speed = random.randint(1, 5)
        self.is_alive = True
        self.number = soldier_number
        self.is_commander = False
        print(
            f"Soldier initialied with arguments: (x:{self.x})|(y:{self.y})|(speed:{self.speed})|(sno: {self.number})"
        )

    def __str__(self) -> str:
        return f"NUMBER: {self.number} IS_ALIVE: {self.is_alive} | POS:({self.x}, {self.y}) | SPEED: {self.speed}"


class SoldierNotificationService(SoldierNotificationServicer):
    def __init__(self) -> None:
        soldier_number = int(sys.argv[1]) - 60000  # okay, need to pass a port number as the argument
        # soldier_number = 60000 - 60000
        self.soldier = Soldier(soldier_number)
        controller_channel = grpc.insecure_channel(f"{SOLDIER_IP}:{CONTROLLER_PORT}")
        self.controller_stub = ControllerNotificationStub(controller_channel)

    # RPCs
    def notify_soldier(self, request, context):
        print(f"Soldier {self.soldier.number} received missile notification from commander! Calculating survival!")
        missile_x = request.x
        missile_y = request.y
        time_to_impact = request.t

        missile_type = request.missile_type
        survive = self.can_survive(missile_type, missile_x, missile_y, time_to_impact)
        if not survive:
            print(f"**** SOLDIER {self.soldier.number} IS NO MORE!!")
        self.soldier.is_alive = survive
        return Empty()

    def soldier_status(self, request, context):
        print("Soldier status polled...")
        survival = survival_response(is_alive=self.soldier.is_alive)
        return survival

    def soldier_position(self, request, context):
        return position_details(x=self.soldier.x, y=self.soldier.y)

    def make_commander(self, request, context):
        print(f"{self.soldier.number} IS NOW THE NEW COMMANDER BABY!")
        self.soldier.is_commander = True
        return Empty()

    def notify_commander(self, request, context):
        request = missile_details(missile_type=request.missile_type, x=request.x, y=request.y, t=request.t)
        self.controller_stub.notify_controller(request)
        print("** Called Controller.notify_controller **")
        return Empty()

    def kill(self,request,context):
        print("Killing soldier process...")
        t = threading.Thread(target = self.kill_function)
        t.setDaemon(False)
        t.start()
        return Empty()
    
    def kill_function(self):
        time.sleep(0.1)
        server.stop(0)
    # Util methods
    def serve(self):
        global server
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
        add_SoldierNotificationServicer_to_server(self, server)
        server.add_insecure_port(f"{SOLDIER_IP}:{sys.argv[1]}")
        # server.add_insecure_port(f"localhost:{60000}")
        server.start()
        print(f"SOLDIER {self.soldier.number} STARTED...")
        server.wait_for_termination()

    def can_survive(self, missile_type, missile_x, missile_y, time_to_impact):
        impact_area = get_impact_area(missile_type, missile_x, missile_y)
        # If soldier is in the impact zone
        if self.can_get_hit(impact_area):
            top_distance, bottom_distance, left_distance, right_distance = self.get_distances_from_impact_edges(
                impact_area
            )

            distances = [
                (top_distance, Direction.TOP),
                (bottom_distance, Direction.BOTTOM),
                (left_distance, Direction.LEFT),
                (right_distance, Direction.RIGHT),
            ]

            # Sort distances
            distances = sorted(distances, key=lambda x: x[0])
            available_directions = self.get_available_directions_for_movement(impact_area)

            print(f"INITIAL DATA-> {self.soldier}")
            # Update soldier coordinates
            self.move_soldier(distances, available_directions, time_to_impact)

            print(f"AFTER MOVE-> {self.soldier}")

            # Return whether the soldier is still in impact area
            return not self.can_get_hit(impact_area)
        else:
            print(f"SOLDIER NOT HIT-> {self.soldier}")
            return True

    def get_distances_from_impact_edges(self, impact_area):
        # Trivial case, when missile type is M1 i.e radius = 0
        if impact_area.left_x == impact_area.right_x:
            return 0, 0, 0, 0

        top_distance = abs(impact_area.top_y - self.soldier.y)
        right_distance = abs(impact_area.right_x - self.soldier.x)
        bottom_distance = abs(self.soldier.y - impact_area.bottom_y)
        left_distance = abs(self.soldier.x - impact_area.left_x)
        print("top_distance:", top_distance)
        print("right_distance:", right_distance)
        print("bottom_distance:", bottom_distance)
        print("left_distance:", left_distance)
        return top_distance, bottom_distance, left_distance, right_distance

    def can_get_hit(self, impact_area):
        return (impact_area.left_x <= self.soldier.x <= impact_area.right_x) and (
            impact_area.top_y <= self.soldier.y <= impact_area.bottom_y
        )

    def get_available_directions_for_movement(self, impact_area):
        res = []
        top, bottom, left, right = False, False, False, False
        if impact_area.top_y > BoardEdges.TOP_Y:
            res.append(Direction.TOP)
            top = True

        if impact_area.bottom_y < BoardEdges.BOTTOM_Y:
            res.append(Direction.BOTTOM)
            bottom = True

        if impact_area.left_x > BoardEdges.LEFT_X:
            res.append(Direction.LEFT)
            left = True

        if impact_area.right_x < BoardEdges.RIGHT_X:
            res.append(Direction.RIGHT)
            right = True

        if top and right:
            res.append(Direction.TOP_RIGHT)

        if top and left:
            res.append(Direction.TOP_LEFT)

        if bottom and right:
            res.append(Direction.BOTTOM_RIGHT)

        if bottom and left:
            res.append(Direction.BOTTOM_LEFT)

        return res

    # Move soldier in the direction of the least distance from impact area edge
    def move_soldier(self, distances, available_directions, time_to_impact):
        available_moves = []
        for d in distances:
            if d[1] in available_directions:
                available_moves.append(d)

        # print(f"AVAILABLE MOVES: {available_moves}")
        print(f"\n_______________________ MOVEMENT LOG SOLDIER {self.soldier.number} _______________________")
        print(f"SELECTING MOVE: {available_moves[0]}")
        direction = available_moves[0][1]
        d = available_moves[0][0]

        # Return if soldier cannot move out of the impact area
        max_possible_steps = self.soldier.speed * time_to_impact
        if max_possible_steps <= d:
            return

        steps_remaining = max_possible_steps - d - 1
        print(f"**** Steps rem: {steps_remaining}")
        if steps_remaining <= 0:
            noise = 0
        else:
            noise = random.randint(0, steps_remaining)

        move_right = min(self.soldier.x + d + 1 + noise, BoardEdges.RIGHT_X)
        move_top = max(self.soldier.y - d - 1 - noise, BoardEdges.TOP_Y)
        move_bottom = min(self.soldier.y + d + 1 + noise, BoardEdges.BOTTOM_Y)
        move_left = max(self.soldier.x - d - 1 - noise, BoardEdges.LEFT_X)

        print(f"MOVE TOP: {move_top}, MOVE BOTTOM: {move_bottom}, MOVE RIGHT: {move_right}, MOVE LEFT: {move_left}")

        if direction == Direction.RIGHT:
            print(f"*****IN RIGHT, d = {d}, speed = {self.soldier.speed}")
            dirs = [Direction.RIGHT]
            if Direction.TOP_RIGHT in available_directions:
                dirs.append(Direction.TOP_RIGHT)

            if Direction.BOTTOM_RIGHT in available_directions:
                dirs.append(Direction.BOTTOM_RIGHT)

            # Select random direction
            r = random.randint(0, len(dirs) - 1)
            selected_direction = dirs[r]

            if selected_direction == Direction.RIGHT:
                # Move right
                self.soldier.x = move_right
                print("(RIGHT) CONDITION TRIGGERED")
            elif selected_direction == Direction.TOP_RIGHT:
                # Move top and right
                self.soldier.y = move_top
                self.soldier.x = move_right
                print("(TOP RIGHT) CONDITION TRIGGERED")
            elif selected_direction == Direction.BOTTOM_RIGHT:
                # Move bottom and right
                self.soldier.y = move_bottom
                self.soldier.x = move_right
                print("(BOTTOM RIGHT) CONDITION TRIGGERED")

        elif direction == Direction.LEFT:
            print(f"*****IN LEFT, d = {d}, speed = {self.soldier.speed}")
            dirs = [Direction.LEFT]

            if Direction.TOP_LEFT in available_directions:
                dirs.append(Direction.TOP_LEFT)

            if Direction.BOTTOM_LEFT in available_directions:
                dirs.append(Direction.BOTTOM_LEFT)

            # Select random direction
            r = random.randint(0, len(dirs) - 1)
            selected_direction = dirs[r]

            if selected_direction == Direction.LEFT:
                # Move left
                self.soldier.x = move_left
                print("(LEFT) CONDITION TRIGGERED")
            elif selected_direction == Direction.TOP_LEFT:
                # Move top and left
                self.soldier.y = move_top
                self.soldier.x = move_left
                print("(TOP LEFT) CONDITION TRIGGERED")
            elif selected_direction == Direction.BOTTOM_LEFT:
                # Move bottom and left
                self.soldier.y = move_bottom
                self.soldier.x = move_left
                print("(BOTTOM LEFT) CONDITION TRIGGERED")

        elif direction == Direction.TOP:
            print(f"*****IN TOP, d = {d}, speed = {self.soldier.speed}")
            dirs = [Direction.TOP]

            if Direction.TOP_LEFT in available_directions:
                dirs.append(Direction.TOP_LEFT)

            if Direction.TOP_RIGHT in available_directions:
                dirs.append(Direction.TOP_RIGHT)

            # Select random direction
            r = random.randint(0, len(dirs) - 1)
            selected_direction = dirs[r]

            if selected_direction == Direction.TOP:
                # Move top
                self.soldier.y = move_top
                print("(TOP) CONDITION TRIGGERED")
            elif selected_direction == Direction.TOP_LEFT:
                # Move top and left
                self.soldier.y = move_top
                self.soldier.x = move_left
                print("(TOP LEFT) CONDITION TRIGGERED")
            elif selected_direction == Direction.TOP_RIGHT:
                # Move top and right
                self.soldier.y = move_top
                self.soldier.x = move_right
                print("(TOP RIGHT) CONDITION TRIGGERED")
        else:
            print(f"*****IN BOTTOM, d = {d}, speed = {self.soldier.speed}")
            dirs = [Direction.BOTTOM]

            if Direction.BOTTOM_LEFT in available_directions:
                dirs.append(Direction.BOTTOM_LEFT)

            if Direction.BOTTOM_RIGHT in available_directions:
                dirs.append(Direction.BOTTOM_RIGHT)

            # Select random direction
            r = random.randint(0, len(dirs) - 1)
            selected_direction = dirs[r]

            if selected_direction == Direction.BOTTOM:
                # Move bottom
                self.soldier.y = move_bottom
                print("(BOTTOM) CONDITION TRIGGERED")
            elif selected_direction == Direction.BOTTOM_LEFT:
                # Move bottom and left
                self.soldier.y = move_bottom
                self.soldier.x = move_left
                print("(BOTTOM LEFT) CONDITION TRIGGERED")
            elif selected_direction == Direction.BOTTOM_RIGHT:
                # Move bottom and right
                self.soldier.y = move_bottom
                self.soldier.x = move_right
                print("(BOTTOM RIGHT) CONDITION TRIGGERED")

        print(f"***NEW POS***: ({self.soldier.x }, {self.soldier.y})")
        print(f"______________________________________________\n")


if __name__ == "__main__":
    service = SoldierNotificationService()
    service.serve()
