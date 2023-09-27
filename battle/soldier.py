import grpc
import random
import sys
from concurrent import futures
from messages_pb2_grpc import SoldierNotificationServicer, add_SoldierNotificationServicer_to_server
from messages_pb2 import missile_details, Empty, survival_response,position_details

from constants import missile_radius, Direction, BoardEdges, ImpactArea


class Soldier:
    def __init__(self, soldier_number) -> None:
        self.x = random.randint(0, 9)
        self.y = random.randint(0, 9)
        self.speed = random.randint(1, 5)
        self.is_alive = True
        self.number = soldier_number
        print(f"Soldier initialied with arguments: (x:{self.x})|(y:{self.y})|(speed:{self.speed})|(sno: {self.number})")

    def __str__(self) -> str:
        return f"NUMBER: {self.number} IS_ALIVE: {self.is_alive} | POS:({self.x}, {self.y}) | SPEED: {self.speed}"


class SoldierNotificationService(SoldierNotificationServicer):
    def __init__(self) -> None:
        soldier_number = int(sys.argv[1]) - 60000 #okay, need to pass a port number as the argument
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
        return position_details(x = self.soldier.x,y = self.soldier.y)

    # Util methods
    def serve(self):
        server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
        add_SoldierNotificationServicer_to_server(self, server)
        server.add_insecure_port(f"localhost:{sys.argv[1]}")

        server.start()
        print(f"SOLDIER {self.soldier.number} STARTED...")
        server.wait_for_termination()

    def can_survive(self, missile_type, missile_x, missile_y, t):
        impact_area = self.get_impact_area(missile_type, missile_x, missile_y)
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

    def get_impact_area(self, missile_type, missile_x, missile_y):
        # Calculate boundaries of missile impact area
        missile_left_x = missile_x - missile_radius[missile_type]
        missile_right_x = missile_x + missile_radius[missile_type]

        missile_top_y = missile_y + missile_radius[missile_type]
        missile_bottom_y = missile_y - missile_radius[missile_type]
        if(missile_left_x<BoardEdges.LEFT_X): missile_left_x = BoardEdges.LEFT_X
        if(missile_right_x>BoardEdges.RIGHT_X): missile_right_x = BoardEdges.RIGHT_X
        if(missile_bottom_y<BoardEdges.BOTTOM_Y): missile_bottom_y = BoardEdges.BOTTOM_Y
        if(missile_bottom_y>BoardEdges.TOP_Y): missile_top_y = BoardEdges.TOP_Y
        impact_area = ImpactArea(
            left_x=missile_left_x, right_x=missile_right_x, top_y=missile_top_y, bottom_y=missile_bottom_y
        )

        return impact_area

    def get_distances_from_impact_edges(self, impact_area):
        # Trivial case, when missile type is M1 i.e radius = 0
        if impact_area.left_x == impact_area.right_x:
            return 0, 0, 0, 0

        top_distance = impact_area.top_y - self.soldier.y
        right_distance = impact_area.right_x - self.soldier.x
        bottom_distance = self.soldier.y - impact_area.bottom_y
        left_distance = self.soldier.x - impact_area.left_x

        return top_distance, bottom_distance, left_distance, right_distance

    def can_get_hit(self, impact_area):
        return (impact_area.left_x <= self.soldier.x <= impact_area.right_x) and (
            impact_area.top_y >= self.soldier.y >= impact_area.bottom_y
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
        for d in distances:
            direction = d[1]
            if direction in available_directions:
                if direction == Direction.RIGHT:
                    self.soldier.x = min(self.soldier.x + self.soldier.speed, BoardEdges.RIGHT_X)
                elif direction == Direction.LEFT:
                    self.soldier.x = max(self.soldier.x - self.soldier.speed, BoardEdges.LEFT_X)
                elif direction == Direction.TOP:
                    self.soldier.y = min(self.soldier.y + self.soldier.speed, BoardEdges.TOP_Y)
                else:
                    self.soldier.y = max(self.soldier.y - self.soldier.speed, BoardEdges.BOTTOM_Y)

                return


if __name__ == "__main__":
    service = SoldierNotificationService()
    service.serve()
