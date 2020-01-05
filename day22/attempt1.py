from typing import List
import numpy as np
import re
Deck = np.ndarray


def collect_input(file_name: str):
    with open(file_name, 'r') as f:
        return f.read().splitlines()


def create_deck(cards: int) -> Deck:
    return np.arange(0, cards, 1)


class CardOperations:
    def parse_operation(self, deck: Deck, line: str):

        # Cut cards operation
        res = re.search("^cut\\s-?\\d+$", line)
        if res is not None:
            split = line.split(' ')
            how_many = int(split[1])
            return self.cut_cards(deck, how_many)

        # Deal with incement operation
        res = re.search("^deal\\swith\\sincrement\\s\\d+$", line)
        if res is not None:
            split = line.split(' ')
            increment_step = int(split[3])
            return self.deal_with_increment(deck, increment_step)

        if line == "deal into new stack":
            return self.deal_into_new_stack(deck)

        raise Exception("Unsupported operation")

    def cut_cards(self, deck: Deck, how_many: int):
        return np.append(deck[how_many:], deck[0:how_many])

    def deal_into_new_stack(self, deck: Deck):
        return np.flip(deck)

    def deal_with_increment(self, deck: Deck, increment_step: int):
        new_arr = np.array([None] * len(deck))

        # new_arr_pointer = 0
        # deck_pointer = 0
        # while deck_pointer < len(deck):
        #     new_arr[new_arr_pointer] = deck[deck_pointer]
        #     deck_pointer += 1
        #     new_arr_pointer += increment_step
        #     if new_arr_pointer >= len(deck):
        #         new_arr_pointer -= len(deck)
        # return np.array(new_arr)

        for i in range(0, len(deck) * increment_step, increment_step):
            new_index = (i % len(deck))
            new_arr[new_index] = deck[i // increment_step]
        return np.array(new_arr)


if __name__ == "__main__":
    lines = collect_input("input.txt")
    # print(lines)

    deck = create_deck(10007)  # 10_007
    # print(deck)

    card_operations = CardOperations()

    # tests
    # res = card_operations.deal_with_increment(np.arange(0, 11, 1), 2)
    # print(res)

    for i in range(len(lines)):
        # print(f'Step: {i} - line: {lines[i]}')
        deck = card_operations.parse_operation(deck, lines[i])

    # print(deck)
    for i in range(len(deck)):
        if deck[i] == 2019:
            print(i)
            break
    # print(deck[2019])
