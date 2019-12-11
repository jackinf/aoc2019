class Asteroid:
    def __init__(self, x: int, y: int):
        self.x = x
        self.y = y
        self.seen_asteroids = []
        self.blocked_asteroids = []

    def has_seen(self, x: int, y: int) -> bool:
        for seen_asteroid in self.seen_asteroids:
            if seen_asteroid[0] == x and seen_asteroid[1] == y:
                return True
        return False

    def is_blocked(self, x: int, y: int) -> bool:
        for blocked_asteroid in self.blocked_asteroids:
            if blocked_asteroid.x == x and blocked_asteroid.y == y:
                return True
        return False

    def get_coord(self):
        return self.x, self.y

    def get_how_much_asteroids_i_see(self):
        return f'({self.x}, {self.y}): I see {len(self.seen_asteroids)} asteroids.'

    def is_same(self, asteroid) -> bool:
        return self.x == asteroid.x and self.y == asteroid.y

    def __str__(self):
        return f'({self.x}, {self.y})'

    def __repr__(self):
        return self.__str__()
