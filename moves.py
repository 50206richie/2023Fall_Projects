"""
This file is for dealing moves (detect, select, generate)
"""

from collections import Counter
from cards import *
from itertools import combinations

# action types, referred from https://github.com/kwai/DouZero
TYPE_0_PASS = 0
TYPE_1_SINGLE = 1
TYPE_2_PAIR = 2
TYPE_3_TRIPLE = 3
TYPE_4_BOMB = 4
TYPE_5_KING_BOMB = 5
TYPE_6_3_1 = 6
TYPE_7_3_2 = 7
TYPE_8_SERIAL_SINGLE = 8
TYPE_9_SERIAL_PAIR = 9
TYPE_10_SERIAL_TRIPLE = 10
TYPE_11_SERIAL_3_1 = 11
TYPE_12_SERIAL_3_2 = 12
TYPE_13_4_2 = 13
TYPE_14_4_22 = 14
TYPE_15_WRONG = 15
TYPE_16_2_1 = 16

MIN_SERIAL_SINGLE = 5
MIN_SERIAL_PAIR = 3
MIN_SERIAL_TRIPLE = 2


def is_continuous(move: list) -> bool:
    """
    check if a list contains sequential number
    :param move: a list of ints
    :return: True if move is continuous
    >>> is_continuous([3, 4, 5, 6, 7, 8])
    True
    >>> is_continuous([11, 12, 13, 14, 16])
    False
    """
    for i in range(len(move)-1):
        if move[i+1] - move[i] != 1:
            return False
    return True


def get_move_type(move: list) -> dict:
    """
    get the type of move
    :param move: a list of ints
    :return: a dict of info about the move
    >>> get_move_type([30])
    {'type': 1, 'rank': 30}
    >>> get_move_type([8, 8, 8, 8, 5, 5, 6, 6])
    {'type': 14, 'rank': 8}
    >>> get_move_type([3, 3, 3, 4, 4, 4, 5, 6])
    {'type': 11, 'rank': 3, 'len': 2}
    >>> get_move_type([3, 3, 3, 4, 4, 4, 5, 5, 6, 6])
    {'type': 12, 'rank': 3, 'len': 2}
    """
    move_size = len(move)
    move_dict = Counter(move)
    move_uniq = sorted(move_dict.keys())
    move_dict_cnt = Counter(move_dict.values())

    match move_size:  # do we need type 15
        case 0:
            return {'type': TYPE_0_PASS}

        case 1:
            return {'type': TYPE_1_SINGLE, 'rank': move[0]}

        case 2:
            if move == [20, 30]:
                return {'type': TYPE_5_KING_BOMB}
            elif move[0] == move[1]:
                return {'type': TYPE_2_PAIR, 'rank': move[0]}
            else:
                return {'type': TYPE_15_WRONG}

        case 3:
            if len(move_dict) == 1:
                return {'type': TYPE_3_TRIPLE, 'rank': move[0]}
            elif len(move_dict) == 2:
                return {'type': TYPE_16_2_1, 'rank': move[1]}
            else:
                return {'type': TYPE_15_WRONG}

        case 4:  # 3+1, 4
            if move_dict_cnt == {3: 1, 1: 1}:
                return {'type': TYPE_6_3_1, 'rank': move[1]}
            elif move_dict_cnt == {4: 1}:
                return {'type': TYPE_4_BOMB,  'rank': move[0]}

        case 5:  # 12345, 3+2
            if move_dict_cnt == {3: 1, 2: 1}:
                return {'type': TYPE_7_3_2, 'rank': move[2]}  # XXXYY or YYXXX will all be X
            elif is_continuous(move):
                return {'type': TYPE_8_SERIAL_SINGLE, 'rank': move[0], 'len': len(move)}

        case _:
            if is_continuous(move):
                return {'type': TYPE_8_SERIAL_SINGLE, 'rank': move[0], 'len': len(move)}
            # 2 * n
            elif len(move_dict) == move_dict_cnt.get(2) and is_continuous(move_uniq):
                return {'type': TYPE_9_SERIAL_PAIR, 'rank': move[0], 'len': len(move_dict)}
            # 3 * n
            elif len(move_dict) == move_dict_cnt.get(3) and is_continuous(move_uniq):
                return {'type': TYPE_10_SERIAL_TRIPLE, 'rank': move[0], 'len': len(move_dict)}
            # (3+1) * n
            elif move_dict_cnt.get(3) == move_dict_cnt.get(1) and move_dict_cnt.get(3, 0) > 1:
                threes = sorted([k for k, v in move_dict.items() if v == 3])
                if is_continuous(threes):
                    return {'type': TYPE_11_SERIAL_3_1, 'rank': threes[0], 'len': len(threes)}
            # (3+2) * n
            elif move_dict_cnt.get(3) == move_dict_cnt.get(2) and move_dict_cnt.get(3, 0) > 1:
                threes = sorted([k for k, v in move_dict.items() if v == 3])
                if is_continuous(threes):
                    return {'type': TYPE_12_SERIAL_3_2, 'rank': threes[0], 'len': len(threes)}
            # 4+2, 4+1+1
            elif move_dict_cnt == {4: 1, 2: 1} or move_dict_cnt == {4: 1, 1: 2}:
                return {'type': TYPE_13_4_2, 'rank': move[2]}
            # 4+2+2
            elif move_dict_cnt == {4: 1, 2: 2}:
                return {'type': TYPE_14_4_22, 'rank': [num for num, cnt in move_dict.items() if cnt == 4].pop()}


class MoveGeneration:
    """generate legal moves
    this class was inspired by https://github.com/kwai/DouZero and has referenced some code from it
    """
    def __init__(self, cards, rival_move, rule=0):
        self.cards = cards
        self.cards_unique = sorted(list(set(self.cards)))
        self.cards_dict = Counter(cards)
        self.rival_move = rival_move
        self.rival_move_length = len(rival_move)
        self.new_move = []
        self.rule = rule
        self.move_type_weight_and_function = {
            TYPE_1_SINGLE: {'weight': 1, 'function': self.gen_type_1_single},
            TYPE_2_PAIR: {'weight': 2, 'function': self.gen_type_2_pair},
            TYPE_3_TRIPLE: {'weight': 4, 'function': self.gen_type_3_triple},
            TYPE_4_BOMB: {'weight': 10, 'function': self.gen_type_4_bomb},
            TYPE_5_KING_BOMB: {'weight': 16, 'function': self.gen_type_5_king_bomb},
            TYPE_6_3_1: {'weight': 4, 'function': self.gen_type_6_3_1},
            TYPE_7_3_2: {'weight': 4, 'function': self.gen_type_7_3_2},
            TYPE_8_SERIAL_SINGLE: {'weight': 6, 'function': self.gen_type_8_serial_single},
            TYPE_9_SERIAL_PAIR: {'weight': 6, 'function': self.gen_type_9_serial_pair},
            TYPE_10_SERIAL_TRIPLE: {'weight': 8, 'function': self.gen_type_10_serial_triple},
            TYPE_11_SERIAL_3_1: {'weight': 8, 'function': self.gen_type_11_serial_3_1},
            TYPE_12_SERIAL_3_2: {'weight': 8, 'function': self.gen_type_12_serial_3_2},
            TYPE_13_4_2: {'weight': 8, 'function': self.gen_type_13_4_2},
            TYPE_14_4_22: {'weight': 8, 'function': self.gen_type_14_4_22}
        }
        if self.rule:
            self.move_type_weight_and_function[TYPE_16_2_1] = {'weight': 3, 'function': self.gen_type_16_2_1}

    def generate_move(self):
        """get rival move and generate corresponding moves
        >>> mg = MoveGeneration([4, 4, 4, 5, 5, 5, 20, 30], [3, 3])
        >>> mg.generate_move()
        >>> mg.new_move
        [[4, 4], [5, 5]]
        """
        rival_move_dict = get_move_type(self.rival_move)

        if rival_move_dict['type'] == TYPE_0_PASS:
            self.gen_all_moves()

        else:
            self.move_type_weight_and_function[rival_move_dict['type']]['function']()

        self.gen_type_4_bomb()
        self.gen_type_5_king_bomb()

    def gen_all_moves(self):
        """generate any available moves by calling other gen methods, add weight of move types
        >>> mg = MoveGeneration([4, 4, 4, 5, 5, 5, 20, 30], [])
        >>> mg.gen_all_moves()
        >>> mg.new_move
        [[4], [5], [20], [30], [4, 4], [5, 5], [4, 4, 4], [5, 5, 5], [4, 4, 4, 5], [4, 4, 4, 20], \
[4, 4, 4, 30], [4, 5, 5, 5], [5, 5, 5, 20], [5, 5, 5, 30], [4, 4, 4, 5, 5], [4, 4, 5, 5, 5], \
[4, 4, 4, 5, 5, 5], [4, 4, 4, 5, 5, 5, 20, 30], [20, 30]]
        """

        for k, v in dict(sorted(self.move_type_weight_and_function.items(), key=lambda x: x[1]['weight'])).items():
            # print(k, 'and', v['function'])
            v['function']()

    def gen_type_1_single(self):
        """
        >>> mg = MoveGeneration([4, 4, 4, 5, 5, 5, 6, 6, 8], [5])
        >>> mg.gen_type_1_single()
        >>> mg.new_move
        [[6], [8]]
        >>> mg = MoveGeneration([4, 4, 4, 5, 5, 5, 6, 6, 8], [])
        >>> mg.gen_type_1_single()
        >>> mg.new_move
        [[4], [5], [6], [8]]
        """
        for i in set(self.cards):
            if not self.rival_move_length or i > self.rival_move[0]:
                self.new_move.append([i])
        self.new_move.sort()

    def gen_type_2_pair(self):
        """
        >>> mg = MoveGeneration([4, 4, 4, 5, 5, 5, 6, 6, 8], [5, 5])
        >>> mg.gen_type_2_pair()
        >>> mg.new_move
        [[6, 6]]
        >>> mg = MoveGeneration([4, 4, 4, 5, 5, 5, 6, 6, 8], [])
        >>> mg.gen_type_2_pair()
        >>> mg.new_move
        [[4, 4], [5, 5], [6, 6]]
        """
        for k, v in self.cards_dict.items():
            if v >= 2 and (not self.rival_move_length or k > self.rival_move[0]):
                self.new_move.append([k, k])

    def gen_type_3_triple(self):
        """
        >>> mg = MoveGeneration([4, 4, 4, 5, 5, 5, 6, 6, 6, 8], [5, 5, 5])
        >>> mg.gen_type_3_triple()
        >>> mg.new_move
        [[6, 6, 6]]
        >>> mg = MoveGeneration([4, 4, 4, 5, 5, 5, 6, 6, 8], [])
        >>> mg.gen_type_3_triple()
        >>> mg.new_move
        [[4, 4, 4], [5, 5, 5]]
        """
        for k, v in self.cards_dict.items():
            if v >= 3 and (not self.rival_move_length or k > self.rival_move[0]):
                self.new_move.append([k, k, k])

    def gen_type_4_bomb(self):
        """
        >>> mg = MoveGeneration([4, 4, 4, 4, 5, 5, 5, 6, 6, 6, 6], [5, 5, 5, 5])
        >>> mg.gen_type_4_bomb()
        >>> mg.new_move
        [[6, 6, 6, 6]]
        >>> mg = MoveGeneration([4, 4, 4, 4, 5, 5, 5, 6, 6, 6, 8], [])
        >>> mg.gen_type_4_bomb()
        >>> mg.new_move
        [[4, 4, 4, 4]]
        >>> mg = MoveGeneration([4], [])
        >>> mg.gen_type_4_bomb()
        >>> mg.new_move
        []
        """
        for k, v in self.cards_dict.items():
            if v == 4 and (not self.rival_move_length or k > self.rival_move[0]):
                self.new_move.append([k, k, k, k])

    def gen_type_5_king_bomb(self):
        """Do not care about rival move since it is the biggest move"""
        if 20 in self.cards and 30 in self.cards:
            self.new_move.append([20, 30])

    def gen_type_6_3_1(self):
        """
        3+1
        >>> mg = MoveGeneration([4, 4, 4, 5, 5, 5, 6, 6, 8], [3, 4, 4, 4])
        >>> mg.gen_type_6_3_1()
        >>> mg.new_move
        [[4, 5, 5, 5], [5, 5, 5, 6], [5, 5, 5, 8]]
        >>> mg = MoveGeneration([4, 4, 5, 5, 5, 6, 6, 8], [])
        >>> mg.gen_type_6_3_1()
        >>> mg.new_move
        [[4, 5, 5, 5], [5, 5, 5, 6], [5, 5, 5, 8]]
        """
        rival_3 = [x for x in self.rival_move if Counter(self.rival_move)[x] == 3][0] if self.rival_move_length else 0
        for k, v in self.cards_dict.items():
            if v >= 3 and k > rival_3:
                for i in self.cards:
                    if i != k and [k, k, k, i] not in self.new_move:
                        self.new_move.append([k, k, k, i])
        for i in self.new_move:
            i.sort()

    def gen_type_7_3_2(self):
        """
        3+2
        >>> mg = MoveGeneration([4, 4, 4, 5, 5, 5, 6, 6, 8, 8, 9], [3, 3, 3, 4, 4])
        >>> mg.gen_type_7_3_2()
        >>> mg.new_move
        [[4, 4, 4, 5, 5], [4, 4, 4, 6, 6], [4, 4, 4, 8, 8], [4, 4, 5, 5, 5], [5, 5, 5, 6, 6], [5, 5, 5, 8, 8]]
        """
        rival_3 = [x for x in self.rival_move if Counter(self.rival_move)[x] == 3][0] if self.rival_move_length else 0
        for k, v in self.cards_dict.items():
            if v >= 3 and k > rival_3:
                for i, j in self.cards_dict.items():
                    if i != k and j >= 2 and [k, k, k, i, i] not in self.new_move:
                        self.new_move.append([k, k, k, i, i])
        for i in self.new_move:
            i.sort()

    def gen_serial(self, move_type, min_chain):
        """

        :param move_type: [3, 4, 5, 6, 7] is TYPE_8_SERIAL_SINGLE, [3, 3, 4, 4, 5, 5] is TYPE_9_SERIAL_PAIR
        :param min_chain: how many sequential numbers to form a chain
        """
        # single = 8 - 7 == 1, pair == 2, triple == 3
        repeat = move_type - 7
        card_set = []
        for k, v in self.cards_dict.items():
            if v >= repeat:
                card_set.append(k)

        for start_card in card_set:
            if start_card > 15 - min_chain:
                break

            if self.rival_move_length == 0:
                # can generate length 5-12 cards for serial_single, 3-10 serial pair, 2-6 serial triple
                for length in range(min_chain, len(card_set)+1):
                    possible_chain = [start_card + x for x in range(length)]
                    if all(x in card_set for x in possible_chain):
                        self.new_move.append(sorted(possible_chain*repeat))
            else:
                rival_move_serial_unique = []
                for k, v in Counter(self.rival_move).items():
                    if v >= repeat:
                        rival_move_serial_unique.append(k)
                possible_chain = [start_card + x for x in range(len(rival_move_serial_unique))]
                if all(x in card_set for x in possible_chain) and possible_chain[0] > self.rival_move[0]:
                    self.new_move.append(sorted(possible_chain*repeat))

    def gen_type_8_serial_single(self):
        """chain
        >>> mg = MoveGeneration([4, 4, 5, 5, 5, 6, 6, 8, 8, 9, 10, 10, 10, 11, 12, 13, 14, 14, 16], [3, 4, 5, 6, 7, 8])
        >>> mg.gen_type_8_serial_single()
        >>> mg.new_move
        [[8, 9, 10, 11, 12, 13], [9, 10, 11, 12, 13, 14]]
        >>> mg = MoveGeneration([4, 4, 6, 6, 8, 8, 9, 10, 10, 10, 11, 12, 13, 14, 14, 16, 20], [8, 9, 10, 11, 12, 13])
        >>> mg.gen_type_8_serial_single()
        >>> mg.new_move
        [[9, 10, 11, 12, 13, 14]]
        >>> mg = MoveGeneration([3, 4, 5, 6, 7, 8, 10, 11, 12, 13, 14], [])
        >>> mg.gen_type_8_serial_single()
        >>> mg.new_move
        [[3, 4, 5, 6, 7], [3, 4, 5, 6, 7, 8], [4, 5, 6, 7, 8], [10, 11, 12, 13, 14]]
        """
        self.gen_serial(TYPE_8_SERIAL_SINGLE, MIN_SERIAL_SINGLE)

    def gen_type_9_serial_pair(self):
        """chain pair
        >>> mg = MoveGeneration([4, 4, 5, 5, 5, 6, 6, 8, 8, 9, 9, 10, 10, 11, 12, 13, 14, 14, 16], [4, 4, 5, 5, 6, 6])
        >>> mg.gen_type_9_serial_pair()
        >>> mg.new_move
        [[8, 8, 9, 9, 10, 10]]
        >>> mg = MoveGeneration([4, 4, 5, 5, 6, 6, 7, 7, 8, 8, 8, 10], [])
        >>> mg.gen_type_9_serial_pair()
        >>> mg.new_move
        [[4, 4, 5, 5, 6, 6], [4, 4, 5, 5, 6, 6, 7, 7], [4, 4, 5, 5, 6, 6, 7, 7, 8, 8], [5, 5, 6, 6, 7, 7], \
[5, 5, 6, 6, 7, 7, 8, 8], [6, 6, 7, 7, 8, 8]]
        """
        self.gen_serial(TYPE_9_SERIAL_PAIR, MIN_SERIAL_PAIR)

    def gen_type_10_serial_triple(self):
        """chain triple
        >>> mg = MoveGeneration([4, 4, 4, 5, 5, 5, 6, 6, 6, 9, 9, 9, 10, 10, 10, 11, 11, 11, 16], [4, 4, 4, 5, 5, 5])
        >>> mg.gen_type_10_serial_triple()
        >>> mg.new_move
        [[5, 5, 5, 6, 6, 6], [9, 9, 9, 10, 10, 10], [10, 10, 10, 11, 11, 11]]
        >>> mg = MoveGeneration([4, 4, 5, 5, 6, 6, 7, 7, 7, 8, 8, 8, 10], [])
        >>> mg.gen_type_10_serial_triple()
        >>> mg.new_move
        [[7, 7, 7, 8, 8, 8]]
        """
        self.gen_serial(TYPE_10_SERIAL_TRIPLE, MIN_SERIAL_TRIPLE)

    def gen_type_11_serial_3_1(self):
        """(3+1)*n
        >>> mg = MoveGeneration([4, 4, 4, 5, 6, 6, 6, 10, 11, 11, 11, 16], [4, 4, 4, 5, 5, 5, 6, 7])
        >>> mg.gen_type_11_serial_3_1()
        >>> mg.new_move
        []
        >>> mg = MoveGeneration([3, 4, 4, 4, 5, 5, 5, 6, 16], [])
        >>> mg.gen_type_11_serial_3_1()
        >>> mg.new_move
        [[3, 4, 4, 4, 5, 5, 5, 6], [3, 4, 4, 4, 5, 5, 5, 16], [4, 4, 4, 5, 5, 5, 6, 16]]
        >>> mg = MoveGeneration([4, 4, 4, 5, 5, 5, 20, 30], [])
        >>> mg.gen_type_11_serial_3_1()
        >>> mg.new_move
        [[4, 4, 4, 5, 5, 5, 20, 30]]
        """
        serial_3_1_moves = []
        serial_3_1_moves.extend(self.new_move)
        # The above two lines saves existing self.new_move in serial_3_1_moves
        # when assigning self.new_move = serial_3_1_moves the existing moves will not be erased
        len_1 = len(self.new_move)
        self.gen_type_10_serial_triple()
        len_2 = len(self.new_move)
        serial_3_moves = self.new_move[len_1:len_2]

        for s3 in serial_3_moves:
            s3_set = set(s3)
            one_cards = [x for x in self.cards_unique if x not in s3_set]

            one_cards_comb = [list(x) for x in combinations(one_cards, len(s3_set))]

            for i in one_cards_comb:
                serial_3_1_moves.append(sorted(s3 + i))

        self.new_move = serial_3_1_moves

    def gen_type_12_serial_3_2(self):
        """(3+2)*n
        >>> mg = MoveGeneration([4, 4, 4, 5, 5, 5, 6, 6, 6, 11, 11, 11, 16], [3, 3, 3, 4, 4, 4, 5, 5, 6, 6, 7])
        >>> mg.gen_type_12_serial_3_2()
        >>> mg.new_move
        [[4, 4, 4, 5, 5, 5, 6, 6, 11, 11], [4, 4, 5, 5, 5, 6, 6, 6, 11, 11]]
        >>> mg = MoveGeneration([4, 4, 4, 5, 5, 5, 6, 6, 16, 16], [])
        >>> mg.gen_type_12_serial_3_2()
        >>> mg.new_move
        [[4, 4, 4, 5, 5, 5, 6, 6, 16, 16]]
        """
        serial_3_2_moves = []
        serial_3_2_moves.extend(self.new_move)
        len_1 = len(self.new_move)
        self.gen_type_10_serial_triple()
        len_2 = len(self.new_move)
        serial_3_moves = self.new_move[len_1:len_2]
        pairs = sorted([k for k, v in self.cards_dict.items() if v >= 2])

        for s3 in serial_3_moves:
            s3_set = set(s3)
            two_cards = [x for x in pairs if x not in s3_set]

            two_cards_comb = [list(x) for x in combinations(two_cards, len(s3_set))]

            for i in two_cards_comb:
                serial_3_2_moves.append(sorted(s3 + i*2))

        self.new_move = serial_3_2_moves

    def gen_type_13_4_2(self):
        """
        4_2 means 4+1+1
        >>> mg = MoveGeneration([3, 3, 3, 3, 5, 5, 5, 5, 8, 12], [4, 4, 4, 4, 5, 6, 13])
        >>> mg.gen_type_13_4_2()
        >>> mg.new_move
        [[3, 5, 5, 5, 5, 8], [3, 5, 5, 5, 5, 12], [5, 5, 5, 5, 8, 12]]
        >>> mg = MoveGeneration([4, 5, 5, 5, 5, 8, 12], [])
        >>> mg.gen_type_13_4_2()
        >>> mg.new_move
        [[4, 5, 5, 5, 5, 8], [4, 5, 5, 5, 5, 12], [5, 5, 5, 5, 8, 12]]
        """
        four_cards = [k for k, v in self.cards_dict.items() if v == 4]
        type_13_4_2_moves = []
        type_13_4_2_moves.extend(self.new_move)

        for fc in four_cards:
            one_cards = [x for x in self.cards_unique if x != fc]

            one_cards_comb = [list(x) for x in combinations(one_cards, 2)]

            for i in one_cards_comb:
                rival_4 = 0
                if self.rival_move_length:
                    for k, v in Counter(self.rival_move).items():
                        if v == 4:
                            rival_4 = k
                if not self.rival_move_length or (self.rival_move_length and fc > rival_4):
                    type_13_4_2_moves.append(sorted([fc]*4 + i))

        self.new_move = type_13_4_2_moves

    def gen_type_14_4_22(self):
        """
        4_2 means 4+2+2
        >>> mg = MoveGeneration([3, 3, 3, 3, 4, 5, 5, 5, 5, 12, 12], [4, 4, 4, 4, 6, 6, 13, 13])
        >>> mg.gen_type_14_4_22()
        >>> mg.new_move
        [[3, 3, 5, 5, 5, 5, 12, 12]]
        >>> mg = MoveGeneration([3, 3, 3, 3, 4, 5, 5, 5, 5, 12, 12], [])
        >>> mg.gen_type_14_4_22()
        >>> mg.new_move
        [[3, 3, 3, 3, 5, 5, 12, 12], [3, 3, 5, 5, 5, 5, 12, 12]]
        """
        four_cards = [k for k, v in self.cards_dict.items() if v == 4]
        type_14_4_22_moves = []
        type_14_4_22_moves.extend(self.new_move)
        pairs = sorted([k for k, v in self.cards_dict.items() if v >= 2])

        for fc in four_cards:
            two_cards = [x for x in pairs if x != fc]

            two_cards_comb = [list(x) for x in combinations(two_cards, 2)]

            for i in two_cards_comb:
                rival_4 = 0
                if self.rival_move_length:
                    for k, v in Counter(self.rival_move).items():
                        if v == 4:
                            rival_4 = k
                if not self.rival_move_length or (self.rival_move_length and fc > rival_4):
                    type_14_4_22_moves.append(sorted([fc]*4 + i + i))

        self.new_move = type_14_4_22_moves

    def gen_type_16_2_1(self):
        """
        2+1
        >>> mg = MoveGeneration([4, 4, 4, 5, 5, 5, 6, 6, 8], [3, 4, 4])
        >>> mg.gen_type_16_2_1()
        >>> mg.new_move
        [[4, 5, 5], [5, 5, 6], [5, 5, 8], [4, 6, 6], [5, 6, 6], [6, 6, 8]]
        >>> mg = MoveGeneration([4, 4, 5, 5, 5, 6, 6, 8], [])
        >>> mg.gen_type_16_2_1()
        >>> mg.new_move
        [[4, 4, 5], [4, 4, 6], [4, 4, 8], [4, 5, 5], [5, 5, 6], [5, 5, 8], [4, 6, 6], [5, 6, 6], [6, 6, 8]]
        """
        rival_2 = [x for x in self.rival_move if Counter(self.rival_move)[x] == 2][0] if self.rival_move_length else 0
        for k, v in self.cards_dict.items():
            if v >= 2 and k > rival_2:
                for i in self.cards:
                    if i != k and [k, k, i] not in self.new_move:
                        self.new_move.append([k, k, i])
        for i in self.new_move:
            i.sort()


def play_a_move(player_hand: Deck, move_list: list, strength: int = 0, rule: int = 0) -> list:
    """

    :param player_hand:
    :param move_list:
    :param strength:
    :param rule: original = 0, special = 1
    :return: the move played
    >>> a = Deck()
    >>> b = [[6, 6]]
    >>> a.cards = [5, 5, 5, 6, 7, 8, 9, 20, 30]
    >>> play_a_move(a, b)
    [20, 30]
    """
    rival_move = []
    if len(move_list) != 0:
        if len(move_list[-1]) == 0:
            rival_move = move_list[-2]
        else:
            rival_move = move_list[-1]

    move_generator = MoveGeneration(player_hand.cards, rival_move, rule)
    move_generator.generate_move()
    moves = move_generator.new_move

    # move as a move list, modify for difference
    idx = int(strength / 10 * len(moves))
    move = moves[idx] if len(moves) else []
    player_hand.remove_card_from_hand(move)

    return move
