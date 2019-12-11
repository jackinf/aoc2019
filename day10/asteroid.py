import math
from typing import Tuple, List


class Asteroid:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.seen_asteroids = []
        self.blocked_asteroids = []
        self.other_asteroids: List[Tuple[Asteroid, str, float]] = []

    def has_seen(self, x: int, y: int) -> bool:
        for seen_asteroid in self.seen_asteroids:
            if seen_asteroid.x == x and seen_asteroid.y == y:
                return True
        return False

    def is_blocked(self, x: int, y: int) -> bool:
        for blocked_asteroid in self.blocked_asteroids:
            if blocked_asteroid.x == x and blocked_asteroid.y == y:
                return True
        return False

    def add_other_asteroid(self, other):
        angle = f'{round(math.atan2(other.x - self.x, other.y - self.y), 4)}'
        dist = round(math.sqrt((other.x - self.x)**2 + (other.y - self.y)**2), 4)
        # for _, other_angle, other_distance in self.other_asteroids:
        #     if other_angle == angle and other_distance < dist:
        #         return  # found an asteroid with smaller distance
        if dist == 0:
            return
        self.other_asteroids.append((other, angle, dist))

    def clean_up_blocked(self):
        temp = {}
        for asteroid, angle, dist in self.other_asteroids:
            if angle in temp:
                if math.fabs(temp[angle][0]) > math.fabs(dist):
                    temp[angle] = (dist, asteroid)
            else:
                temp[angle] = (dist, asteroid)

        self.other_asteroids.clear()
        for angle, dist_asteroid in temp.items():
            dist, asteroid = dist_asteroid
            self.other_asteroids.append((asteroid, angle, dist))

    def get_coord(self):
        return self.x, self.y

    def get_how_much_asteroids_i_see(self):
        return f'({self.x}, {self.y}): I see {len(self.seen_asteroids)} asteroids.'

    def get_how_much_other_asteroids_i_see(self):
        return f'({self.x}, {self.y}): I see {len(self.other_asteroids)} asteroids.'

    def is_same(self, asteroid) -> bool:
        return self.x == asteroid.x and self.y == asteroid.y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return self.__str__()
