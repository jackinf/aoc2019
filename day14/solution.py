import copy
import math
import sys
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


def collect_values(file_name: str):
    with open(file_name, 'r') as f:
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


def calculate_ore(target_elements: List[TargetElem], multiplier: int):
    fuel_element: TargetElem = next(x for x in target_elements if x.name == "FUEL")

    # this will be handled like a queue: first elements will be popped, and new ones appended to the end
    requirements = copy.deepcopy(fuel_element.requirements)
    for fuel_requirement in requirements:
        fuel_requirement.count *= multiplier

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


targets = collect_values('test-case-2.txt')
print(f"PART 1: {calculate_ore(targets, 1)}")

TRILLION = 1_000_000_000_000
print(f'PART 2: calculating million')
def find_trillion():
    x = 1
    step1 = 5
    margin = .01

    bottom = TRILLION
    top = TRILLION
    min_distance = TRILLION

    growing = True
    changed = False
    while True:
        res = calculate_ore(targets, x).count
        print(f'res: {res}, x: {x}')
        if res < TRILLION:
            if growing is False:
                changed = True
                growing = True
        else:
            if growing is True:
                changed = True
                growing = False

        if changed:
            step1 = round(step1 - margin, 4)
            print(step1)

        diff1 = TRILLION - res
        if math.fabs(min_distance) > math.fabs(diff1):
            if diff1 >= 0:
                bottom = x
            elif diff1 < 0:
                top = x

        if step1 > 1:
            if growing:
                x *= step1
            else:
                x //= step1
        elif step1 == 1:
            step2 = TRILLION - res
            print(step2)
            print(f'TOP: {top}, BOTTOM: {bottom}')

            for step_x in [10000, 1000, 100, 10, 1]:
                for i in range(bottom, top, step_x):
                    res = calculate_ore(targets, i).count
                    if res > TRILLION:
                        print(f'PART 2: found {i-1}')
                        bottom = i - step_x
                        break
            break
        x = round(x)


# find_trillion()

def part2_manually():
    for i in range(1863700, 1872236, 1):  # I've found these numbers using find_trillion() -> BOTTOM and TOP. Then, I've experimented manually with step, and came close to those values
        res = calculate_ore(targets, i).count
        if res > TRILLION:
            print(f'PART 2: found {i - 1}')  # it should find 1863741
            break
part2_manually()
