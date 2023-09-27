import grpc
import random
import sys
from concurrent import futures
from messages_pb2_grpc import SoldierNotificationServicer, add_SoldierNotificationServicer_to_server
from messages_pb2 import Empty, survival_response, position_details

from constants import Direction, BoardEdges, get_impact_area


class Soldier:
    def __init__(self, soldier_number) -> None:
        self.x = random.randint(0, 9)
        self.y = random.randint(0, 9)
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
        self.soldier = Soldier(soldier_number)

    # RPCs
    def notify_soldier(self, request, context):
        print(f"Soldier {self.soldier.number} received missile notification from commander! Calculating survival!")
        missile_x = request.x
        missile_y = request.y
        time_remaining = request.t

        missile_type = request.missile_type
        survive = self.can_survive(missile_type, missile_x, missile_y, time_remaining)
        self.soldier.is_alive = survive
        return Empty()

    def soldier_status(self, request, context):
        print("Soldier status polled...")
        survival = survival_response(is_alive=self.soldier.is_alive)
        return survival

    def soldier_position(self, request, context):
        return position_details(x=self.soldier.x, y=self.soldier.y)

    def make_commander(self, request, context):
        self.soldier.is_commander = True
        return Empty()

    # Util methods
    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
        add_SoldierNotificationServicer_to_server(self, server)
        server.add_insecure_port(f"localhost:{sys.argv[1]}")

        server.start()
        print(f"SOLDIER {self.soldier.number} STARTED...")
        server.wait_for_termination()

    def can_survive(self, missile_type, missile_x, missile_y, t):
        impact_area = get_impact_area(missile_type, missile_x, missile_y)
        print("IMPACT AREA:")
        print(impact_area)
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
            self.move_soldier(distances, available_directions)

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

        return top_distance, bottom_distance, left_distance, right_distance

    def can_get_hit(self, impact_area):
        return (impact_area.left_x <= self.soldier.x <= impact_area.right_x) and (
            impact_area.top_y <= self.soldier.y <= impact_area.bottom_y
        )

    def get_available_directions_for_movement(self, impact_area):
        res = []
        if impact_area.top_y < BoardEdges.TOP_Y:
            res.append(Direction.TOP)

        if impact_area.bottom_y > BoardEdges.BOTTOM_Y:
            res.append(Direction.BOTTOM)

        if impact_area.left_x > BoardEdges.LEFT_X:
            res.append(Direction.LEFT)

        if impact_area.right_x < BoardEdges.RIGHT_X:
            res.append(Direction.RIGHT)

        return res

    # Move soldier in the direction of the least distance from impact area edge
    def move_soldier(self, distances, available_directions):
        available_moves = []
        for d in distances:
            if d[1] in available_directions:
                available_moves.append(d)

        print(f"AVAILABLE MOVES: {available_moves}")
        index = random.randint(0, len(available_moves) - 1)
        print(f"SELECTING MOVE: {available_moves[index]}")
        direction = available_moves[index][1]
        if direction == Direction.RIGHT:
            self.soldier.x = min(self.soldier.x + self.soldier.speed, self.soldier.x + d[0] + 1, BoardEdges.RIGHT_X)
        elif direction == Direction.LEFT:
            self.soldier.x = max(self.soldier.x - self.soldier.speed, self.soldier.x - d[0] - 1, BoardEdges.LEFT_X)
        elif direction == Direction.TOP:
            self.soldier.y = max(self.soldier.y - self.soldier.speed, self.soldier.y - d[0] - 1, BoardEdges.TOP_Y)
        else:
            self.soldier.y = min(self.soldier.y + self.soldier.speed, self.soldier.y + d[0] + 1, BoardEdges.BOTTOM_Y)


if __name__ == "__main__":
    service = SoldierNotificationService()
    service.serve()
