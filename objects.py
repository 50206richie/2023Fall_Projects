"""This file mainly contains objects for the simulation"""


class Deck:
    """As title"""

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
        :return: sum of cards
        >>> a = Deck()
        >>> a.cards.extend([5, 6, 7, 8, 9, 20])
        >>> a.get_deck_points()
        55
        """
        return sum(self.cards)

    def get_deck_length(self):
        """
        :return: length of cards
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
            try:
                # print(f"removed {card}")
                self.cards.remove(card)
            except ValueError:
                print(f"cannot remove {card}")


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

    def assign_character(self, char_num: int):
        """
        Takes a char_num input and assigns it to attribute "self.character",
        landlord = 0, peasant1 (next opponent of landlord) = 1, peasant2 = 2
        :param char_num: The number of character
        """
        self.character = char_num
