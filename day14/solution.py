import copy
import math
from typing import List, Set


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
    with open('input.txt', 'r') as f:
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


def calculate_all_requirements(target_elements: List[TargetElem], requirements: List[ReqElement]) -> Set[str]:
    if len(requirements) == 0:
        return set()

    acc: Set[str] = set()
    for requirement in requirements:
        next_requirements = next((x.requirements for x in target_elements if x.name == requirement.name and x.name != "ORE"), None)
        if next_requirements is None:
            continue
        acc.update([x.name for x in next_requirements if x.name != "ORE"])
        acc.update(calculate_all_requirements(target_elements, next_requirements))
    return acc


def calculate_ore(target_elements: List[TargetElem]):
    fuel_element: TargetElem = next(x for x in target_elements if x.name == "FUEL")

    # this will be handled like a queue: first elements will be popped, and new ones appended to the end
    requirements = copy.deepcopy(fuel_element.requirements)

    while [x.name for x in requirements] != ["ORE"]:
        # pop the current requirement
        current_requirement = [x for x in requirements if x.name != "ORE"].pop(0)
        requirements = [x for x in requirements if x.name != current_requirement.name]

        # check if this element is still required for some different chemical reaction
        all_dependencies = list(calculate_all_requirements(target_elements, requirements))
        if current_requirement.name in all_dependencies:
            requirements.append(current_requirement)  # add to the end
            continue

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
