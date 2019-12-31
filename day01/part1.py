def get_fuel_requirement(mass: int):
    return mass // 3 - 2


# Example:
# print(get_fuel_requirement(73617))
# print(get_fuel_requirement(14))
# print(get_fuel_requirement(1969))
# print(get_fuel_requirement(100756))


file = open('test-case-2.txt', 'r')
with file as f:
    answer = sum([get_fuel_requirement(int(x.strip())) for x in f.readlines()])
print(answer)

# Correct answer: 3271095
