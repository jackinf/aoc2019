from typing import List, Tuple


class Solution:
    def run(self, input_str) -> Tuple[int, int]:
        start, end = [int(x) for x in input_str.split('-')]

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

    def check_asc_order(self, arr: List[int]) -> bool:
        """
        Check if numbers are in increasing order. Easiest way to check if the array is sorted
        """
        return arr == sorted(arr)

    def check_two_adjacent_digits(self, arr: List[int]) -> bool:
        """
        Check if the abcdef has at least 2 adjacent numbers
        """
        a, b, c, d, e, f = arr
        return a == b or b == c or c == d or d == e or e == f

    def check_two_adjacent_digits_strictly(self, arr: List[int]) -> bool:
        """
        Part 2 of the exersize: check for abcdef if there's at least one match where only a==b or b==c or c==d or d==e
        or e==f where number does not equal to neighbour
        """
        a, b, c, d, e, f = arr
        return a == b and b != c \
               or b == c and b != a and c != d \
               or c == d and c != b and d != e \
               or d == e and d != c and e != f \
               or e == f and e != d


sol = Solution()
print(sol.run('272091-815432'))
