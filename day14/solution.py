from typing import List


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

    def part1_calculate_ore(self, fuel: TargetChemical):
        simple_chemicals = self.get_simple_chemicals(fuel)
        print(simple_chemicals)

    def get_simple_chemicals(self, target_chemical: TargetChemical) -> List[TargetChemical]:
        source_chemicals = target_chemical.source_chemicals
        if len(source_chemicals) == 0:
            raise Exception("Each chemical requires at least 1 source chemical")

        # basic case: "simple" chemicals can be created from ORE
        if len(source_chemicals) == 1 and source_chemicals[0].name == "ORE":
            return [target_chemical]

        simple_chemicals = []
        for current_source_chemical in source_chemicals:
            current_target_chemical = self.find_target_chemical_by_name(current_source_chemical)
            found_simple_chemicals = self.get_simple_chemicals(current_target_chemical)
            simple_chemicals.append(*found_simple_chemicals)

        return simple_chemicals

    def find_target_chemical_by_name(self, chemical: Chemical):
        return next(x for x in self.target_chemicals if x.name == chemical.name)


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
    fuel = next(x for x in target_chemicals if x.name == "FUEL")
    print(fuel)