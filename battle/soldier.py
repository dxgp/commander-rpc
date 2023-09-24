import grpc
import random
import sys
from concurrent import futures
from messages_pb2_grpc import SoldierNotificationServicer, add_SoldierNotificationServicer_to_server
from messages_pb2 import missile_details, Empty, survival_response

from .constants import missile_radius, Direction, BoardEdges, ImpactArea, MissileType

is_alive = True
soldier_speed = random.randint(0, 5)
soldier_number = 0
soldier_x = random.randint(0, 9)
soldier_y = random.randint(0, 9)


def get_impact_area(missile_type, missile_x, missile_y):
    # Calculate boundaries of missile impact area
    missile_left_x = missile_x - missile_radius[missile_type]
    missile_right_x = missile_x + missile_radius[missile_type]

    missile_top_y = missile_y - missile_radius[missile_type]
    missile_bottom_y = missile_y + missile_radius[missile_type]
    impact_area = ImpactArea(
        left_x=missile_left_x, right_x=missile_right_x, top_y=missile_top_y, bottom_y=missile_bottom_y
    )

    return impact_area


def get_distances_from_impact_edges(impact_area):
    # Trivial case, when missile type is M1 i.e radius = 0
    if impact_area.left_x == impact_area.right_x:
        return 0, 0, 0, 0

    top_distance = impact_area.top_y - soldier_y
    right_distance = impact_area.right_x - soldier_x
    bottom_distance = soldier_y - impact_area.bottom_y
    left_distance = soldier_x - impact_area.left_x

    return top_distance, bottom_distance, left_distance, right_distance


def get_available_directions_for_movement(impact_area):
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
def move_soldier(distances, available_directions):
    for d in distances:
        direction = d[1]
        if direction in available_directions:
            if direction == Direction.RIGHT:
                soldier_x = min(soldier_x + soldier_speed, BoardEdges.RIGHT_X)
            elif direction == Direction.LEFT:
                soldier_x = max(soldier_x - soldier_speed, BoardEdges.LEFT_X)
            elif direction == Direction.TOP:
                soldier_y = min(soldier_y + soldier_speed, BoardEdges.TOP_Y)
            else:
                soldier_y = max(soldier_y - soldier_speed, BoardEdges.BOTTOM_Y)

            return


def can_get_hit(impact_area):
    return (impact_area.left_x <= soldier_x <= impact_area.right_x) and (
        impact_area.top_y <= soldier_y <= impact_area.bottom_y
    )


def can_survive(missile_type, missile_x, missile_y, t):
    impact_area = get_impact_area(missile_type, missile_x, missile_y)
    # If soldier is in the impact zone
    if can_get_hit(impact_area):
        top_distance, bottom_distance, left_distance, right_distance = get_distances_from_impact_edges(impact_area)

        distances = [
            (top_distance, Direction.TOP),
            (bottom_distance, Direction.BOTTOM),
            (left_distance, Direction.LEFT),
            (right_distance, Direction.RIGHT),
        ]

        # Sort distances
        distances = sorted(distances)
        available_directions = get_available_directions_for_movement(impact_area)

        # Update soldier coordinates
        move_soldier(distances, available_directions)

        # Return whether the soldier is still in impact area
        return not can_get_hit(impact_area)


class SoldierNotificationService(SoldierNotificationServicer):
    def notify_soldier(self, request, context):
        print(f"Soldier {soldier_number} received missile notification from commander! Calculating survival!")
        missile_x = request.x
        missile_y = request.y
        time_remaining = request.t
        # TODO Convert missile_type from str to MissileType enum instance
        missile_type = request.missile_type
        survive = can_survive(missile_type, missile_x, missile_y, time_remaining)
        is_alive = survive
        return Empty()

    def soldier_status(self, request, context):
        print("Soldier status polled...")
        survival = survival_response(is_alive=is_alive)
        return survival


def serve():
    global soldier_number
    server = grpc.server(futures.ThreadPoolExecutor(max_workers=2))
    add_SoldierNotificationServicer_to_server(SoldierNotificationService(), server)
    server.add_insecure_port(f"localhost:{sys.argv[1]}")
    soldier_number = int(sys.argv[1]) - 50002 + 1
    server.start()
    server.wait_for_termination()


if __name__ == "__main__":
    serve()
