"""This module stores functions that run the simulation"""

from objects import *
from constants import *
from game_moves import MoveGeneration
import random


def deal_cards(cards: list, player1: Player(), player2: Player(), player3: Player()) -> None:
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


def set_up_new_game(players: list[Player()], landlord_lv=0, peasants_lv=0) -> None:
    """
    create a new deck of shuffled cards, deal 51 to players, bid for the landlord, deal the last 3 cards to the landlord
    :param players: a list of 3 player objects
    :param landlord_lv: the strength of the character, ranges from 0 to 9
    :param peasants_lv: the strength of the character, ranges from 0 to 9
    >>> a = [Player() for _ in range(3)]
    >>> set_up_new_game(a)
    >>> len(a[0].hand.cards) + len(a[1].hand.cards) + len(a[2].hand.cards)
    54
    # >>> a[0].hand.cards
    """
    new_deck = Deck()
    new_deck.add_new_deck()
    new_deck.shuffle_cards()
    deal_cards(new_deck.cards, players[0], players[1], players[2])
    # Now each player has 17 cards, 3 cards left in new deck

    # Calculate hand_points of players
    for player in players:
        player.update_hand_points()

    # Start bidding (maybe change points to moves available)
    player_handpoints = [player.hand_points for player in players]
    landlord_player_index = player_handpoints.index(random.choices(
        player_handpoints,
        weights=[n**2 for n in player_handpoints]
    )[0])
    players[landlord_player_index].assign_character(LANDLORD)
    players[(landlord_player_index+1) % 3].assign_character(PEASANT_1)
    players[(landlord_player_index+2) % 3].assign_character(PEASANT_2)

    # Assigning the strength of characters
    for player in players:
        if player.character == LANDLORD:
            player.strength = landlord_lv
        else:
            player.strength = peasants_lv

    # Add the 3 cards left in new_deck to the landlord (different with normal, peasants don't know the 3 cards here)
    players[landlord_player_index].hand.cards.extend([new_deck.cards.pop() for _ in range(3)])

    players[landlord_player_index].first_player_next_round = True
    for player in players:
        player.hand.cards.sort()


def play_a_move(player_hand: Deck(), move_list: list, strength=0, rule=0) -> list:
    """
    Gets last rival's move, generates legal moves, and returns a move stored in a list
    :param player_hand: A deck that a playe has
    :param move_list: The move list in the round
    :param strength: how strong a player should play
    :param rule: original = 0, special >= 1
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


def check_winner(players: list[Player()]) -> int:
    """
    as title
    :param players: the player list
    :return: the winner character code or continue code
    >>> a = [Player() for _ in range(3)]
    >>> set_up_new_game(a)
    >>> check_winner(a) == GAME_CONTINUE
    True
    >>> for player in a:
    ...     if player.character == LANDLORD:
    ...         player.hand.cards = []
    ...         player.hand.cards
    []
    >>> check_winner(a) == LANDLORD
    True
    >>> check_winner(a) == PEASANT
    False
    """
    for i in range(3):
        if players[i].hand.get_deck_length() == 0:
            if players[i].character == LANDLORD:
                return LANDLORD
            else:
                return PEASANT
    return GAME_CONTINUE


def play_a_round(players: list[Player()], rule=0, print_details=False, is_rule3_1st_round=False) -> int:
    """
    Play a round until two people pass
    :param players: A list of playes
    :param rule: original = 0, special .= 1
    :param print_details: Prints details of the game when true
    :param is_rule3_1st_round: Landlord plays an additional move before game when true (only used in SPECIAL_RULE3)
    :return: Returns an int that represents a winner or game continue
    """
    in_play_index = -1
    for i in range(3):
        if players[i].first_player_next_round:
            in_play_index = i
            players[i].first_player_next_round = False

    if is_rule3_1st_round:
        move = play_a_move(players[in_play_index].hand, move_list=[],
                           strength=players[in_play_index].strength, rule=rule)
        if print_details:
            player_name = char_int_to_str[players[in_play_index].character]
            print(f"Player: {player_name} plays move {move}")

            remaining_cards = players[in_play_index].hand.cards
            print(f"    {player_name} remains card {remaining_cards}")
            print(f"Now move list is {[move]}\n")
        players[in_play_index].first_player_next_round = True
        return GAME_CONTINUE

    move_list = []
    while len(move_list) < 2 or (move_list[-1] != [] or move_list[-2] != []):
        # strength can be 0-9
        move = play_a_move(players[in_play_index].hand, move_list,
                           strength=players[in_play_index].strength, rule=rule)
        if print_details:
            player_name = char_int_to_str[players[in_play_index].character]
            print(f"Player: {player_name} plays move {move}")

            remaining_cards = players[in_play_index].hand.cards
            print(f"    {player_name} remains card {remaining_cards}")

        players[in_play_index].update_hand_points()  # Not used

        winner = check_winner(players)
        if winner == LANDLORD or winner == PEASANT:
            # players[in_play_index].first_player_next_round = True
            return winner
        move_list.append(move)
        if print_details:
            print(f"Now move list is {move_list}\n")
        in_play_index = (in_play_index+1) % 3
    players[in_play_index].first_player_next_round = True
    return GAME_CONTINUE
