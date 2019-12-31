import math
import copy
from typing import List, Tuple, Union, Dict


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
        self.initial_pos_found: Union[int, None] = None

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

        copied = copy.deepcopy(planets)
        self.initial_planets = {planet.name:{"pos": planet.pos, "vel": planet.vel} for planet in copied}

    def do_step(self):
        positions = [copy.copy(planet.pos) for planet in self.planets]
        for planet in self.planets:
            planet.apply_gravity(positions)
            planet.apply_velocity()
        self.step += 1

    def print(self):
        print(f'After {self.step} steps')
        for planet in self.planets:
            print(f'pos=<x={planet.pos.x}, y=  {planet.pos.y}, z= {planet.pos.z}>, vel=<x= {planet.vel.x}, y= {planet.vel.y}, z= {planet.vel.z}>')

    def get_total_energy(self) -> int:
        return sum([x.get_potential_energy() * x.get_kinetic_energy() for x in self.planets])

    def get_initial_planet_pos_and_vel(self, planet_name: str) -> Tuple[Position, Velocity]:
        initial_planet = self.initial_planets[planet_name]
        return initial_planet["pos"], initial_planet["vel"]

    def is_initial_x(self, initial_pos: Position, initial_vel: Velocity) -> Union[int, None]:
        return self.step if initial_pos.x == planet.pos.x and initial_vel.x == planet.vel.x else None

    def is_initial_y(self, initial_pos: Position, initial_vel: Velocity) -> Union[int, None]:
        return self.step if initial_pos.y == planet.pos.y and initial_vel.y == planet.vel.y else None

    def is_initial_z(self, initial_pos: Position, initial_vel: Velocity) -> Union[int, None]:
        return self.step if initial_pos.z == planet.pos.z and initial_vel.z == planet.vel.z else None

    def get_step_for_single_planet_when_at_initial(self, current_planet: Planet) -> Union[int, None]:
        initial_pos, initial_vel = self.get_initial_planet_pos_and_vel(current_planet.name)
        pos_x_at_initial = True if initial_pos.x == current_planet.pos.x else False
        vel_x_at_initial = True if initial_vel.x == current_planet.vel.x else False

        pos_y_at_initial = True if initial_pos.y == current_planet.pos.y else False
        vel_y_at_initial = True if initial_vel.y == current_planet.vel.y else False

        pos_z_at_initial = True if initial_pos.z == current_planet.pos.z else False
        vel_z_at_initial = True if initial_vel.z == current_planet.vel.z else False

        if not pos_x_at_initial or not pos_y_at_initial or not pos_z_at_initial \
                and not vel_x_at_initial or not vel_y_at_initial or not vel_z_at_initial:
            return None
        return self.step

    def get_steps_for_all_planets_when_at_initial(self) -> Dict[str, int]:
        results = {}
        for current_planet in self.planets:
            if current_planet.initial_pos_found is not None:
                continue
            step = self.get_step_for_single_planet_when_at_initial(current_planet)
            if step is not None:
                current_planet.initial_pos_found = step
                results[current_planet.name] = step
        return results

    def all_initial_positions_found(self) -> bool:
        return all(True if planet.initial_pos_found is not None else False for planet in self.planets)


def lcm(a, b):
    """Compute the lowest common multiple of a and b"""
    return a * b / math.gcd(a, b)


with open('test-case-2.txt', 'r') as f:
    planets = []
    for line in f.readlines():
        coord_step1 = line.strip()[1:-1].split(',')
        coord_step1 = [coord.strip().split('=') for coord in coord_step1]
        coordinates = {coord_str[0]:int(coord_str[1]) for coord_str in coord_step1}
        pos = Position(coordinates["x"], coordinates["y"], coordinates["z"])
        planet = Planet(f'Planet {len(planets) + 1}', pos, Velocity(0, 0, 0))
        planets.append(planet)

    solar_system = SolarSystem(copy.deepcopy(planets))
    while not solar_system.all_initial_positions_found():
        solar_system.do_step()

        # PART 1
        if solar_system.step // 1001 == 0 and solar_system.step % 1000 == 0:
            solar_system.print()
            print(solar_system.get_total_energy())

        # PART 2
        # if solar_system.is_initial_for_all_planets():
        #     solar_system.print()
        #     print(solar_system.get_total_energy())
        #     break

        results = solar_system.get_steps_for_all_planets_when_at_initial()
        for i, (name, steps) in enumerate(results.items()):
            print(f"{name} at initial on step {steps}")
            planets = [planet for planet in planets if not planet.name == name]