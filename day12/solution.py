import math
from copy import copy
from typing import List

class Position:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z


class Velocity:
    def __init__(self, x: int, y: int, z: int):
        self.x = x
        self.y = y
        self.z = z


class Planet:
    def __init__(self, name: str, pos: Position, vel: Velocity):
        self.name = name
        self.pos = pos
        self.vel = vel

    def apply_gravity(self, planet_positions: List[Position]):
        for position in planet_positions:
            if position.x > self.pos.x:
                self.vel.x += 1
            elif position.x < self.pos.x:
                self.vel.x -= 1

            if position.y > self.pos.y:
                self.vel.y += 1
            elif position.y < self.pos.y:
                self.vel.y -= 1

            if position.z > self.pos.z:
                self.vel.z += 1
            elif position.z < self.pos.z:
                self.vel.z -= 1

    def apply_velocity(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        self.pos.z += self.vel.z

    def get_potential_energy(self):
        return math.fabs(self.pos.x) + math.fabs(self.pos.y) + math.fabs(self.pos.z)

    def get_kinetic_energy(self):
        return math.fabs(self.vel.x) + math.fabs(self.vel.y) + math.fabs(self.vel.z)


class SolarSystem:
    def __init__(self, planets: List[Planet]):
        self.step = 0
        self.planets = planets

    def do_step(self):
        positions = [copy(planet.pos) for planet in self.planets]
        for planet in self.planets:
            planet.apply_gravity(positions)
            planet.apply_velocity()
        self.step += 1

    def print(self):
        print(f'After {self.step} steps')
        for planet in self.planets:
            print(f'pos=<x={planet.pos.x}, y=  {planet.pos.y}, z= {planet.pos.z}>, vel=<x= {planet.vel.x}, y= {planet.vel.y}, z= {planet.vel.z}>')

    def get_total_energy(self):
        return sum([x.get_potential_energy() * x.get_kinetic_energy() for x in self.planets])


with open('input.txt', 'r') as f:
    planets = []
    for line in f.readlines():
        coord_step1 = line.strip()[1:-1].split(',')
        coord_step1 = [coord.strip().split('=') for coord in coord_step1]
        coordinates = {coord_str[0]:int(coord_str[1]) for coord_str in coord_step1}
        pos = Position(coordinates["x"], coordinates["y"], coordinates["z"])
        planet = Planet(f'Planet {len(planets) + 1}', pos, Velocity(0, 0, 0))
        planets.append(planet)

    solar_system = SolarSystem(planets)
    for _ in range(1000):
        solar_system.do_step()
        if solar_system.step % 10 == 0:
            solar_system.print()
            print(solar_system.get_total_energy())
