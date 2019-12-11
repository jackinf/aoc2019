import math
from typing import Tuple, List


class Asteroid:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.other_asteroids: List[Tuple[Asteroid, float, float]] = []

    def add_other_asteroid(self, other):
        angle = math.atan2(other.x - self.x, other.y - self.y)
        distance = math.sqrt((other.x - self.x)**2 + (other.y - self.y)**2)
        if distance == 0:  # then this is exactly the same asteroid
            return
        self.other_asteroids.append((other, angle, distance))

    def clean_up_blocked(self):
        # TODO: optimize the code: group by angle, take with minimum distance
        temp = {}
        for asteroid, angle, distance in self.other_asteroids:
            if angle in temp:
                if math.fabs(temp[angle][0]) > math.fabs(distance):
                    temp[angle] = (distance, asteroid)
            else:
                temp[angle] = (distance, asteroid)

        self.other_asteroids.clear()
        for angle, dist_asteroid in temp.items():
            distance, asteroid = dist_asteroid
            self.other_asteroids.append((asteroid, angle, distance))

    def get_coord(self):
        return self.x, self.y

    def get_how_much_other_asteroids_i_see(self):
        return f'({self.x}, {self.y}): I see {len(self.other_asteroids)} asteroids.'

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return self.__str__()
