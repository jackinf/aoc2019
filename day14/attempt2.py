from typing import List, Tuple
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
    def __init__(self, name: str, count: int, source_chemicals: List['SourceChemical']):
        super().__init__(name, count)
        self.name = name
        self.count = count
        self.source_chemicals = source_chemicals
        self.target_chemicals = []

    def __str__(self):
        return f"{super().__str__()} & target: {self.target_chemicals}"


# ChemDiv = Tuple[List['Chemical'], int]

class HierarchicalChemical(Chemical):
    def __init__(self, name: str, count: int, divisor: int, chemicals: List['HierarchicalChemical']):
        super().__init__(name, count)
        self.name = name
        self.count = count
        self.divisor = divisor
        self.chemicals = chemicals

    def __str__(self):
        return f"{self.count} {self.name}/{self.divisor} & target: {self.chemicals}"

    # def __str__(self):
    #     return f"{self.count} {self.name}/{self.divisor}"


class Lab:
    def __init__(self, target_chemicals: List[TargetChemical]):
        self.target_chemicals = target_chemicals

    def part1_calculate_ore(self):
        fuel = self.find_target_chemical_by_name("FUEL")
        fuel_chems = self.get_target_chemicals(fuel)
        fuel_2 = HierarchicalChemical(fuel.name, fuel.count, 1, fuel_chems)
        print(fuel_2)

        ore = self.get_ore(fuel_2)
        print(ore)

    def get_target_chemicals(self, current_chemical: TargetChemical) -> List[HierarchicalChemical]:
        sources = current_chemical.source_chemicals
        if len(sources) == 0:
            raise Exception("Each chemical requires at least 1 source chemical")
        if len(sources) == 1 and sources[0].name == "ORE":
            ore = sources[0]
            return [HierarchicalChemical(ore.name, ore.count, 1, [])]

        founds = []
        for source in sources:
            next_target = self.find_target_chemical_by_name(source.name)
            found = self.get_target_chemicals(next_target)
            hier_chem = HierarchicalChemical(source.name, source.count, next_target.count, found)
            founds.append(hier_chem)

        return founds

    def get_ore(self, root: HierarchicalChemical) -> HierarchicalChemical:
        if root.chemicals is None or len(root.chemicals) == 0:
            return root

        total_ore_count = 0
        for item in root.chemicals:
            ore = self.get_ore(item)
            res1 = root.count * ore.count
            total_ore_count += res1

        return HierarchicalChemical('ORE', total_ore_count, 1, [])

    def find_target_chemical_by_name(self, chemical_name: str) -> TargetChemical:
        return next(x for x in self.target_chemicals if x.name == chemical_name)

    def group_simple_chemicals(self, simple_chemicals: List[Chemical]):
        grouped = defaultdict(int)
        for item in simple_chemicals:
            grouped[item.name] += item.count
        return grouped


with open('test-input-1.txt', 'r') as f:
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
