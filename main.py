"""The main py file for execution"""
# Change Rules: can 1+2+3

from cards import *
from moves import *
import random
from time import process_time


def set_up_new_game(players):
    """
    create a new deck of shuffled cards, deal 51 to players, bid for the landlord, deal the last 3 cards to the landlord
    :param players: a list of 3 player objects
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

    # Add the 3 cards left in new_deck to the landlord (different with normal, peasants don't know the 3 cards here)
    players[landlord_player_index].hand.cards.extend([new_deck.cards.pop() for _ in range(3)])

    players[landlord_player_index].first_player_next_round = True


def check_winner(players) -> int:
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


def play_a_round(players: list[Player()]):
    """

    :param players:
    :return:
    """
    in_play_player_index = -1
    for i in range(3):
        if players[i].first_player_next_round:
            in_play_player_index = i
    move_list = []
    while len(move_list) < 2 or (move_list[-1] != [] and move_list[-2] != []):
        # TODO: change player playing strength for more randomness
        move = play_a_move(players[in_play_player_index].hand, move_list, strength=0)
        player_name = char_int_to_str[players[in_play_player_index].character]
        # print(f"Player: {player_name} plays move {move}")
        players[in_play_player_index].update_hand_points()
        remaining_cards = players[in_play_player_index].hand.cards
        # print(f"    {player_name} remains card {remaining_cards}")
        winner = check_winner(players)
        if winner == LANDLORD or winner == PEASANT:
            return winner
        move_list.append(move)
        # ## players[in_play_player_index].hand.play_cards()
        in_play_player_index = (in_play_player_index+1) % 3
    return GAME_CONTINUE


if __name__ == '__main__':
    simulations = 100
    wins_landlord = 0
    wins_peasants = 0

    start_time = process_time()

    for _ in range(simulations):
        player_list = [Player() for _ in range(3)]
        set_up_new_game(player_list)
        while True:
            round_result = play_a_round(player_list)
            if round_result == LANDLORD:
                print("Landlord Won")
                wins_landlord += 1
                break
            elif round_result == PEASANT:
                wins_peasants += 1
                print("Peasants Won")
                break
            elif round_result == GAME_CONTINUE:
                continue

    landlord_win_rate = wins_landlord / simulations
    peasants_win_rate = wins_peasants / simulations

    elapsed_time = process_time() - start_time

    print(elapsed_time, 'seconds')
