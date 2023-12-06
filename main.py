"""The main py file for execution"""
# Change Rules: can 1+2+3

from cards import *
from moves import *
import random
from time import process_time
import csv

ORIGINAL_RULE = 0
SPECIAL_RULE = 1


def set_up_new_game(players, landlord_lv=0, peasants_lv=0):
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


def play_a_round(players: list[Player()], rule: int = 0):
    """

    :param players:
    :param rule: original = 0, special = 1
    :return:
    """
    in_play_index = -1
    for i in range(3):
        if players[i].first_player_next_round:
            in_play_index = i
            players[i].first_player_next_round = False
    move_list = []
    while len(move_list) < 2 or (move_list[-1] != [] or move_list[-2] != []):
        if players[in_play_index].character == LANDLORD:
            # strength can be 0-9
            move = play_a_move(players[in_play_index].hand, move_list,
                               strength=players[in_play_index].strength, rule=rule)
        else:
            move = play_a_move(players[in_play_index].hand, move_list,
                               strength=players[in_play_index].strength, rule=rule)
        # player_name = char_int_to_str[players[in_play_index].character]
        # print(f"Player: {player_name} plays move {move}")

        players[in_play_index].update_hand_points()
        # remaining_cards = players[in_play_index].hand.cards
        # print(f"    {player_name} remains card {remaining_cards}")

        winner = check_winner(players)
        if winner == LANDLORD or winner == PEASANT:
            # players[in_play_index].first_player_next_round = True
            return winner
        move_list.append(move)
        # print(f"Now move list is {move_list}\n")
        # ## players[in_play_index].hand.play_cards()  # Can delete
        in_play_index = (in_play_index+1) % 3
    players[in_play_index].first_player_next_round = True
    return GAME_CONTINUE


if __name__ == '__main__':
    rules = [SPECIAL_RULE]
    # rules = [ORIGINAL_RULE, SPECIAL_RULE]
    game_results = []  # Saves all results in a list

    for rule in rules:
        for i in range(10):
            for j in range(10):
                games = 1234
                wins_landlord = 0
                wins_peasants = 0

                start_time = process_time()

                for _ in range(games):
                    player_list = [Player() for _ in range(3)]
                    set_up_new_game(player_list, landlord_lv=i, peasants_lv=j)
                    while True:
                        round_result = play_a_round(player_list, rule)
                        if round_result == LANDLORD:
                            # print("Landlord Won")
                            wins_landlord += 1
                            break
                        elif round_result == PEASANT:
                            wins_peasants += 1
                            # print("Peasants Won")
                            break
                        elif round_result == GAME_CONTINUE:
                            continue

                landlord_win_rate = wins_landlord / games
                peasants_win_rate = wins_peasants / games

                rule_str = 'special' if rule else 'original'
                print(f'\nAmong {games} {rule_str} games played, the win rates are:\n\t'
                      f'LANDLORD: {landlord_win_rate:.2%} with level {i}\n\t'
                      f'PEASANTS: {peasants_win_rate:.2%} with level {j}')

                elapsed_time = process_time() - start_time

                print('Runtime:', elapsed_time, 'seconds')

                games_result = {'games_played': games,
                                'landlord_lv': i,
                                'peasants_lv': j,
                                'win_rate_l': landlord_win_rate,
                                'win_rate_p': peasants_win_rate}
                game_results.append(games_result)

        # with open("DouDiZhu_results.csv", "w", encoding="utf-8", newline='') as ddz_csv:
        #     fieldnames = game_results[0].keys()
        #     writer = csv.DictWriter(ddz_csv, fieldnames=fieldnames)
        #
        #     writer.writeheader()
        #     for games_result in game_results:
        #         writer.writerow(games_result)

        with open("DouDiZhu_special_results.csv", "w", encoding="utf-8", newline='') as ddz_csv:
            fieldnames = game_results[0].keys()
            writer = csv.DictWriter(ddz_csv, fieldnames=fieldnames)

            writer.writeheader()
            for games_result in game_results:
                writer.writerow(games_result)
