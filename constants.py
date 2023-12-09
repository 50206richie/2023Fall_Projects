"""This module contains all constants that are used in the program"""

ORIGINAL_RULE = 0
SPECIAL_RULE1 = 1  # Have 2+1 type
SPECIAL_RULE2 = 2  # Have 2+2+1 type
SPECIAL_RULE3 = 3  # Landlord can play twice the first round
rules_int2str = {ORIGINAL_RULE: 'ORIGINAL_RULE', SPECIAL_RULE1: 'SPECIAL_RULE1',
                 SPECIAL_RULE2: 'SPECIAL_RULE2', SPECIAL_RULE3: 'SPECIAL_RULE3'}

LANDLORD = 0
PEASANT = 1
PEASANT_1 = 1
PEASANT_2 = 2
GAME_CONTINUE = 3

# X: small king, D: big king
# 2 is not 15 (sequential) for chain check
rank2int = {'3': 3, '4': 4, '5': 5, '6': 6, '7': 7, '8': 8, '9': 9, 'T': 10,
            'J': 11, 'Q': 12, 'K': 13, 'A': 14, '2': 16, 'X': 20, 'D': 30}
int2rank = {3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: 'T',
            11: 'J', 12: 'Q', 13: 'K', 14: 'A', 16: '2', 20: 'X', 30: 'D'}
DECK_DICT = {'3': 4, '4': 4, '5': 4, '6': 4, '7': 4, '8': 4, '9': 4,
             'T': 4, 'J': 4, 'Q': 4, 'K': 4, 'A': 4, '2': 4, 'X': 1, 'D': 1}
deckTypeWeightDict = {'Solo': 1, 'Pair': 2, 'Trio': 4, 'ChainSolo': 6, 'ChainPair': 6,
                      'Plane': 8, 'Quad': 8, 'Bomb': 10, 'Rocket': 16, 'Pass': 0}
char_int_to_str = {
    0: 'LANDLORD',
    1: 'PEASANT_1',
    2: 'PEASANT_2'
}

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
TYPE_17_2_2_1 = 17

MIN_SERIAL_SINGLE = 5
MIN_SERIAL_PAIR = 3
MIN_SERIAL_TRIPLE = 2
