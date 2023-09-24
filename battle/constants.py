from enum import Enum


class MissileType(Enum):
    M1 = 1
    M2 = 2
    M3 = 3
    M4 = 4


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
    TOP_Y = 10
    BOTTOM_Y = 0
    LEFT_X = 0
    RIGHT_X = 10


class ImpactArea:
    def __init__(self, left_x, right_x, top_y, bottom_y) -> None:
        self.left_x = left_x
        self.right_x = right_x
        self.top_y = top_y
        self.bottom_y = bottom_y
