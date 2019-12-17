import copy
import math
from typing import List


class ReqElement:
    def __init__(self, name: str, count: int):
        self.name = name
        self.count = count

    def __repr__(self):
        return f"{self.count} {self.name}"


class TargetElem:
    def __init__(self, name: str, count: int, requirements: List[ReqElement]):
        self.name = name
        self.count = count
        self.requirements = requirements

    def __repr__(self):
        return f"{self.count} {self.name} + req: {self.requirements}"


def collect_values():
    with open('test-input-2.txt', 'r') as f:
        target_elements: List[TargetElem] = []
        for line in f.readlines():
            left, right = line.split(' => ')
            right_count, right_name = right.split(' ')

            req_elements: List[ReqElement] = []
            for left_item in left.split(', '):
                left_count, left_name = left_item.split(' ')
                req_elements.append(ReqElement(left_name.strip(), int(left_count)))

            target_elements.append(TargetElem(right_name.strip(), int(right_count), req_elements))

        return target_elements


def calculate_ore(target_elements: List[TargetElem]):
    fuel_element: TargetElem = next(x for x in target_elements if x.name == "FUEL")
    requirements = copy.deepcopy(fuel_element.requirements)

    while [x.name for x in requirements] != ["ORE"]:
        # pop the current requirement
        current_requirement = [x for x in requirements if x.name != "ORE"].pop(0)
        requirements = [x for x in requirements if x.name != current_requirement.name]

        target_element = next(x for x in target_elements if x.name == current_requirement.name)
        for target_requirement in target_element.requirements:
            # take the minimum required amount of elements, if required count is below target count
            result_quantity = math.ceil(current_requirement.count / target_element.count) * target_requirement.count

            # add or update the element count
            found = next((x for x in requirements if x.name == target_requirement.name), None)
            if found is None:
                requirements.append(ReqElement(target_requirement.name, result_quantity))
            else:
                found.count += result_quantity

    return requirements[0]


targets = collect_values()
ore_element = calculate_ore(targets)
print(ore_element)
