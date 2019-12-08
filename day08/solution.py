import sys
from typing import List, Dict


def parse_inputs(test_case: str) -> List[int]:
    return [int(x) for x in list(test_case)]


class Layer:
    def __init__(self, index: int, grid: List[List[int]]):
        self.index = index
        self.grid = grid
        self.flat = [x for sublist in grid for x in sublist]

    def get_number_of_elements(self, element: int):
        return self.flat.count(element)

    def __str__(self):
        return f"\n<Layer {self.index} with {self.grid}>"

    def __repr__(self):
        return self.__str__()


class Solution:
    def run(self, inputs: List[int], rows: int, cols: int) -> int:
        layers = self.build_layers(inputs, rows, cols)
        print(f"Layers: {layers}")
        layer = self.find_layer_with_fewest_zeros(layers)
        print(f"Found layer: {layer}")
        return self.get_product_of_ones_and_twos_in_layer(layer)

    def build_layers(self, inputs: List[int], rows: int, cols: int) -> List[Layer]:
        #   0     1      2     3    4     5
        # [0,0] [0,1] [0,2] [1,0] [1,1] [1,2]
        # rows = 3, cols = 2

        layers: List[Layer] = []
        layer_size = rows * cols
        layer_count = len(inputs) // layer_size

        for layer_i in range(layer_count):
            arr = [[-1 for y in range(rows)] for x in range(cols)]
            for i in range(rows * cols):
                row_i = i // rows
                col_i = int(i % rows)
                inputs_index = layer_i * layer_size + i
                arr[row_i][col_i] = inputs[inputs_index]
            layers.append(Layer(layer_i, arr))

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


test_case_1 = "123456789012"

sol = Solution()
print(sol.run(parse_inputs(test_case_1), 3, 2))

with open("input.txt", "r") as f:
    parsed_inputs = parse_inputs(f.readline())
    print(sol.run(parsed_inputs, 25, 6))