from typing import List
from collections import defaultdict
import math


class Chemical:
    def __init__(self, name: str, count: int):
        self.name = name
        self.count = count

    def __str__(self):
        return f"{self.count} {self.name}"

    def __repr__(self):
        return self.__str__()


class SourceChemical(Chemical):
    pass


class TargetChemical(Chemical):
    def __init__(self, name: str, count: int, source_chemicals: List['Chemical']):
        super().__init__(name, count)
        self.name = name
        self.count = count
        self.source_chemicals = source_chemicals

    def __str__(self):
        return f"{super().__str__()} & source: {self.source_chemicals}"

# Have list of materials, which can be made using ORE
# Take all the target materials -> create list of Materials
# Start from the FUEL: take element names and make a connection to ORE through different elements


class Lab:
    def __init__(self, target_chemicals: List[TargetChemical]):
        self.target_chemicals = target_chemicals

    def part1_calculate_ore(self):
        fuel = next(x for x in target_chemicals if x.name == "FUEL")
        simple_chemicals = self.get_simple_chemicals(fuel, 1)
        print(simple_chemicals)

        grouped = defaultdict(int)
        for item in simple_chemicals:
            grouped[item.name] += item.count
        print(grouped)

        ore_count = 0
        for _, (checmical_name, chemical_count) in enumerate(grouped.items()):
            target_chemical = self.find_target_chemical_by_name(checmical_name)
            if not (len(target_chemical.source_chemicals) == 1 and target_chemical.source_chemicals[0].name == "ORE"):
                raise Exception("I messed up! This is not a chemical which contains only ORE")
            target_chemical_ore_count = target_chemical.source_chemicals[0].count
            ore_count += math.ceil(chemical_count / target_chemical.count) * target_chemical_ore_count

        print(f'Ore count needed: {ore_count}')

    def get_simple_chemicals(self, target_chemical: TargetChemical, count: int) -> List[Chemical]:
        source_chemicals = target_chemical.source_chemicals
        if len(source_chemicals) == 0:
            raise Exception("Each chemical requires at least 1 source chemical")

        # basic case: "simple" chemicals can be created from ORE
        if len(source_chemicals) == 1 and source_chemicals[0].name == "ORE":
            return [Chemical(target_chemical.name, count)]

        simple_chemicals = []
        for source_chemical in source_chemicals:
            next_target = self.find_target_chemical_by_name(source_chemical.name)
            simple_chemicals += self.get_simple_chemicals(next_target, source_chemical.count * count)
        return simple_chemicals

    def find_target_chemical_by_name(self, chemical_name: str) -> TargetChemical:
        return next(x for x in self.target_chemicals if x.name == chemical_name)


with open('test-input-2.txt', 'r') as f:
    target_chemicals: List[TargetChemical] = []
    for line in f.readlines():
        line_split = line.split('=>')

        source_items = line_split[0].split(',')
        source_chemicals: List[SourceChemical] = []
        for source_item in source_items:
            source_item_split = source_item.strip().split(' ')
            source_chemicals.append(SourceChemical(source_item_split[1], int(source_item_split[0])))

        target_item = line_split[1].strip()
        target_item_split = target_item.split(' ')
        target_chemical = TargetChemical(target_item_split[1], int(target_item_split[0]), source_chemicals)
        target_chemicals.append(target_chemical)

    print(target_chemicals)

    lab = Lab(target_chemicals)
    lab.part1_calculate_ore()
