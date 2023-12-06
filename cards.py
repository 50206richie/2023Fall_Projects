"""This file mainly contains objects for reaction, mainly cards
Action Type Weight ref: https://arxiv.org/pdf/2106.06135.pdf
"""

ranks = ['3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2', 'X', 'D']  # X: small king, D: big king
ranks_int = [3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 16, 20, 30]  # 2 is not 15 (sequential) for chain check
# rank2weight = {'3', '4', '5', '6', '7', '8', '9', 'T', 'J', 'Q', 'K', 'A', '2', 'X', 'D'}
deck = {'3': 4, '4': 4, '5': 4, '6': 4, '7': 4, '8': 4, '9': 4,
        'T': 4, 'J': 4, 'Q': 4, 'K': 4, 'A': 4, '2': 4, 'X': 1, 'D': 1}
LANDLORD = 0
PEASANT = 1
PEASANT_1 = 1
PEASANT_2 = 2
GAME_CONTINUE = 3
char_int_to_str = {
    0: 'LANDLORD',
    1: 'PEASANT_1',
    2: 'PEASANT_2'
}


def deal_cards(cards, player1, player2, player3):
    """
    deal 17 cards to 3 players, No shuffling in doctests
    :param cards: 54 cards in a list
    :param player1: a player object
    :param player2: a player object
    :param player3: a player object
    >>> a = Deck()
    >>> a.add_new_deck()
    >>> p1, p2, p3 = Player(), Player(), Player()
    >>> deal_cards(a.cards, p1, p2, p3)
    >>> p1.hand.cards
    [30, 16, 14, 14, 13, 12, 11, 11, 10, 9, 8, 8, 7, 6, 5, 5, 4]
    >>> a.cards
    [3, 3, 3]
    """
    for _ in range(17):
        player1.hand.cards.append(cards.pop())
        player2.hand.cards.append(cards.pop())
        player3.hand.cards.append(cards.pop())


class Deck:
    """As title"""
    deckTypeWeightDict = {'Solo': 1, 'Pair': 2, 'Trio': 4, 'ChainSolo': 6, 'ChainPair': 6,
                          'Plane': 8, 'Quad': 8, 'Bomb': 10, 'Rocket': 16, 'Pass': 0}

    def __init__(self):
        self.points = 0
        self.cards = []

    def add_new_deck(self):
        """
        Append 54 cards to self.cards
        >>> a = Deck()
        >>> a.add_new_deck()
        >>> a.cards
        [3, 3, 3, 3, 4, 4, 4, 4, 5, 5, 5, 5, 6, 6, 6, 6, 7, 7, 7, 7, 8, 8, 8, 8, 9, 9, 9, 9, 10, 10, 10, 10, \
11, 11, 11, 11, 12, 12, 12, 12, 13, 13, 13, 13, 14, 14, 14, 14, 16, 16, 16, 16, 20, 30]
        """
        self.cards = []
        for i in range(3, 17):
            if i != 15:
                for j in range(4):
                    self.cards.append(i)
        self.cards.extend([20, 30])

    def shuffle_cards(self, shuffles=1):
        """
        shuffle cards to random order
        :param shuffles: how many shuffles to do, defaulted to 1 time
        >>> a = Deck()
        >>> a.add_new_deck()
        >>> a.shuffle_cards()
        >>> a.cards != Deck().add_new_deck()
        True
        # >>> a.cards
        """
        import random
        for i in range(shuffles):
            random.shuffle(self.cards)

    def get_deck_points(self):
        """

        :return:
        >>> a = Deck()
        >>> a.cards.extend([5, 6, 7, 8, 9, 20])
        >>> a.get_deck_points()
        55
        """
        return sum(self.cards)

    def get_deck_length(self):
        """
        :return:
        """
        return len(self.cards)

    def remove_card_from_hand(self, move):
        """
        :param move: a list containg cards in the move
        >>> a = Deck()
        >>> a.cards = [3, 4, 5, 6, 7, 8, 9]
        >>> a.remove_card_from_hand([4, 5, 6, 7, 8])
        >>> a.cards
        [3, 9]
        """
        for card in move:
            if card in self.cards:
                # print(f"removed {card}")
                self.cards.remove(card)
            else:
                print(f"cannot remove {card}")
                # self.cards.remove(card)


class Player:
    """As title"""
    def __init__(self):
        self.character = -1
        self.hand = Deck()
        self.hand_points = 0
        self.first_player_next_round = False
        self.strength = 0  # 0-9, the higher the character will play stronger moves

    def update_hand_points(self):
        """
        as title
        >>> a = Player()
        >>> a.hand_points
        0
        >>> a.hand.cards.extend([6, 6, 6, 9])
        >>> a.update_hand_points()
        >>> a.hand_points
        27
        """
        self.hand_points = self.hand.get_deck_points()

    def assign_character(self, char_num):
        """
        Takes a char_num input and assigns it to attribute "self.character",
        landlord = 0, peasant1 (next opponent of landlord) = 1, peasant2 = 2
        :param char_num: The number of character
        """
        self.character = char_num
