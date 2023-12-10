"""The main py file for execution"""

from game_functions import *
from game_moves import *
from time import process_time
import csv


def execute_simulation(
        rules,
        games=1234,
        landlord_lv=0,
        peasants_lv=0,
        single_sim=True,
        print_details=False,
        write_file=False
) -> None:
    """
    The function for executing the whole simulation, takes a few variables from the caller for customization.
    :param games: How many games a simulation plays
    :param landlord_lv: Level of the landlord
    :param peasants_lv: Level of the peasants
    :param rules:
    :param single_sim: Does the simulation run once or multiple times
    :param print_details: Prints details of each game when true
    :param write_file: Writes into csv when true
    """
    rules = rules
    if single_sim:
        landlord_lvs = range(landlord_lv, landlord_lv+1)
        peasants_lvs = range(peasants_lv, peasants_lv+1)
    else:
        landlord_lvs = range(10)
        peasants_lvs = range(10)

    for rule in rules:
        game_results = []  # Saves all results in a list
        for i in landlord_lvs:
            for j in peasants_lvs:
                games = games
                wins_landlord = 0
                wins_peasants = 0

                start_time = process_time()

                for _ in range(games):
                    player_list = [Player() for _ in range(3)]
                    set_up_new_game(player_list, landlord_lv=i, peasants_lv=j)
                    if rule == SPECIAL_RULE3:
                        play_a_round(player_list, rule, print_details=print_details, is_rule3_1st_round=True)
                    while True:
                        round_result = play_a_round(player_list, rule, print_details=print_details)
                        if round_result == LANDLORD:
                            if print_details:
                                print("Landlord Won\n")
                            wins_landlord += 1
                            break
                        elif round_result == PEASANT:
                            wins_peasants += 1
                            if print_details:
                                print("Peasants Won\n")
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
                                'win_rate_landlord': landlord_win_rate,
                                'win_rate_peasants': peasants_win_rate}
                game_results.append(games_result)

        if write_file:
            filename = "DouDiZhu_results_" + rules_int2str[rule] + ".csv"
            with open(filename, "w", encoding="utf-8", newline='') as ddz_csv:
                fieldnames = game_results[0].keys()
                writer = csv.DictWriter(ddz_csv, fieldnames=fieldnames)

                writer.writeheader()
                for games_result in game_results:
                    writer.writerow(games_result)


if __name__ == '__main__':
    t0 = process_time()
    rules_list = [ORIGINAL_RULE, SPECIAL_RULE1, SPECIAL_RULE2, SPECIAL_RULE3]
    games_per_simulation = 1234
    level_of_landlord = 2
    level_of_peasants = 4

    execute_simulation(rules=rules_list[:],
                       games=games_per_simulation,
                       landlord_lv=level_of_landlord,
                       peasants_lv=level_of_peasants,
                       single_sim=False,
                       print_details=False,
                       write_file=True)

    t = process_time() - t0
    print('Total runtime:', t, 'seconds')
