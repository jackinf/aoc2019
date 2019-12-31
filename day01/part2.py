class Solution:
    def calculate(self, mass: int) -> int:
        return self.get_fuel(mass, 0)

    def get_fuel(self, mass: int, acc: int) -> int:
        result = mass // 3 - 2
        if result <= 0:
            return acc
        return self.get_fuel(result, acc + result)


sol = Solution()
print(sol.calculate(14))
print(sol.calculate(1969))
print(sol.calculate(100756))

with open('test-case-2.txt', 'r') as f:
    answer = sum([sol.calculate(int(x.strip())) for x in f.readlines()])
print(answer)
