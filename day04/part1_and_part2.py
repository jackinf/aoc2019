from typing import List, Tuple


class Solution:
    def run(self, input_str) -> Tuple[int, int]:
        start_str, end_str = input_str.split('-')
        start, end = int(start_str), int(end_str)

        total_combinations_part1 = 0
        total_combinations_part2 = 0
        for i in range(start, end):
            i_arr = [int(x) for x in str(i)]
            if self.check_asc_order(i_arr):
                if self.check_two_adjacent_digits(i_arr):
                    total_combinations_part1 += 1
                if self.check_two_adjacent_digits_strictly(i_arr):
                    total_combinations_part2 += 1
        return total_combinations_part1, total_combinations_part2

    def check_asc_order(self, arr: List[int]):
        return arr == sorted(arr)

    def check_two_adjacent_digits(self, arr: List[int]):
        return arr[0] == arr[1] or arr[1] == arr[2] or arr[2] == arr[3] or arr[3] == arr[4] or arr[4] == arr[5]

    def check_two_adjacent_digits_strictly(self, arr: List[int]):
        return arr[0] == arr[1] and arr[1] != arr[2] \
               or arr[1] == arr[2] and arr[1] != arr[0] and arr[2] != arr[3] \
               or arr[2] == arr[3] and arr[2] != arr[1] and arr[3] != arr[4] \
               or arr[3] == arr[4] and arr[3] != arr[2] and arr[4] != arr[5] \
               or arr[4] == arr[5] and arr[4] != arr[3]

sol = Solution()
print(sol.run('272091-815432'))
