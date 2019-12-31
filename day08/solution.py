import sys
from typing import List, Dict, Tuple


def parse_inputs(test_case: str) -> List[int]:
    return [int(x) for x in list(test_case)]


BLACK = 0
WHITE = 1
TR = 2  # transparent

class Layer:
    def __init__(self, index: str, grid: List[List[int]]):
        self.index = index
        self.grid = grid
        self.flat = [x for sublist in grid for x in sublist]

    def get_number_of_elements(self, element: int):
        return self.flat.count(element)

    def get_pixel(self, i: int, j: int):
        return self.grid[j][i]

    def decode_message(self) -> str:
        res = ""
        for cols in self.grid:
            for item in cols:
                res += str("     " if item == BLACK else "#####")
            res += "\n"
        return res

    def __str__(self):
        return f"\n<Layer {self.index} with {self.grid}>"

    def __repr__(self):
        return self.__str__()


class Solution:
    def run(self, inputs: List[int], rows: int, cols: int) -> Tuple[int, str]:
        layers = self.build_layers(inputs, rows, cols)
        # print(f"Layers: {layers}")
        layer = self.find_layer_with_fewest_zeros(layers)
        print(f"[PART 1] Found layer: {layer}")
        merged_layer = self.merge_layers(layers, rows, cols)

        print(f"[PART 2] Merged layer: {merged_layer}")
        part1_result = self.get_product_of_ones_and_twos_in_layer(layer)
        part2_result = merged_layer.decode_message()
        return part1_result, part2_result

    def build_layers(self, inputs: List[int], rows: int, cols: int) -> List[Layer]:
        #   0     1      2     3    4     5
        # [0,0] [0,1] [0,2] [1,0] [1,1] [1,2]
        # rows = 3, cols = 2

        layers: List[Layer] = []
        layer_size = rows * cols
        layer_count = len(inputs) // layer_size

        for layer_i in range(layer_count):
            grid = self.build_empty_grid(rows, cols)
            for i in range(rows * cols):
                grid[i // rows][int(i % rows)] = inputs[layer_i * layer_size + i]
            layers.append(Layer(str(layer_i), grid))

        return layers

    def find_layer_with_fewest_zeros(self, layers: List[Layer]) -> Layer:
        found_min = sys.maxsize
        found_layer = None
        for layer in layers:
            layer_zeros = layer.get_number_of_elements(0)
            if layer_zeros < found_min:
                found_min = layer_zeros
                found_layer = layer
        return found_layer

    def get_product_of_ones_and_twos_in_layer(self, layer: Layer) -> int:
        return layer.get_number_of_elements(1) * layer.get_number_of_elements(2)

    def build_empty_grid(self, rows: int, cols: int):
        return [[-1 for _ in range(rows)] for _ in range(cols)]

    def merge_layers(self, layers: List[Layer], rows: int, cols: int) -> Layer:
        grid = self.build_empty_grid(rows, cols)
        for i in range(rows):
            for j in range(cols):
                for layer in layers:
                    pixel = layer.get_pixel(i, j)
                    if pixel == WHITE or pixel == BLACK:
                        grid[j][i] = pixel
                        break
                if grid[j][i] == -1:
                    grid[j][i] = TR
        return Layer("Merged", grid)


sol = Solution()
print("TEST CASE 1")
print(sol.run(parse_inputs("123456789012"), 3, 2))
print("\nTEST CASE 2")
print(sol.run(parse_inputs("0222112222120000"), 2, 2))

with open("test-case-2.txt", "r") as f:
    parsed_inputs = parse_inputs(f.readline())
    print("\nSOLUTION")

    part1, part2 = sol.run(parsed_inputs, 25, 6)
    print(part1)
    print(part2)