from enum import Enum


SOLDIER_COUNT = 10
SOLDIER_BASE_PORT = 60000
CONTROLLER_PORT = 50001


class MissileType:
    M1 = "M1"
    M2 = "M2"
    M3 = "M3"
    M4 = "M4"


# Radius is number of cells in vertical or horizontal direction from the centre cell in the impact zone.
# This does not count the centre cell in the radius.
# This is set in this way in order to easily calculate the boundary coordinates of the impact area
# like missile_left_x = missile_x - missile_radius[missile_type]
missile_radius = {MissileType.M1: 0, MissileType.M2: 1, MissileType.M3: 2, MissileType.M4: 3}


# 8 directions
class Direction(Enum):
    TOP = 1
    BOTTOM = 2
    LEFT = 3
    RIGHT = 4
    TOP_LEFT = 5
    TOP_RIGHT = 6
    BOTTOM_LEFT = 7
    BOTTOM_RIGHT = 8

    def get_all_directions(self):
        return [
            Direction.TOP,
            Direction.BOTTOM,
            Direction.LEFT,
            Direction.RIGHT,
            Direction.TOP_LEFT,
            Direction.TOP_RIGHT,
            Direction.BOTTOM_LEFT,
            Direction.BOTTOM_RIGHT,
        ]


class BoardEdges:
    TOP_Y = 0
    BOTTOM_Y = 5
    LEFT_X = 0
    RIGHT_X = 5


class ImpactArea:
    def __init__(self, left_x, right_x, top_y, bottom_y) -> None:
        self.left_x = left_x
        self.right_x = right_x
        self.top_y = top_y
        self.bottom_y = bottom_y

    def __str__(self) -> str:
        return f"left_x: {self.left_x} right_x: {self.right_x} | top_y: {self.top_y} bottom_y: {self.bottom_y}"


def get_impact_area(missile_type, missile_x, missile_y):
    # Calculate boundaries of missile impact area
    missile_left_x = missile_x - missile_radius[missile_type]
    missile_right_x = missile_x + missile_radius[missile_type]

    missile_top_y = missile_y - missile_radius[missile_type]
    missile_bottom_y = missile_y + missile_radius[missile_type]

    if missile_left_x < BoardEdges.LEFT_X:
        missile_left_x = BoardEdges.LEFT_X
    if missile_right_x > BoardEdges.RIGHT_X:
        missile_right_x = BoardEdges.RIGHT_X
    if missile_bottom_y > BoardEdges.BOTTOM_Y:
        missile_bottom_y = BoardEdges.BOTTOM_Y
    if missile_top_y < BoardEdges.TOP_Y:
        missile_top_y = BoardEdges.TOP_Y

    impact_area = ImpactArea(
        left_x=missile_left_x, right_x=missile_right_x, top_y=missile_top_y, bottom_y=missile_bottom_y
    )

    return impact_area
