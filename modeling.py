#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Import essential libraries
import random as rnd
import pandas as pd

# Define class Team
class Team:
    # Set LUCK as a static variable
    LUCK = float(0)

    def __init__(self, name, strength = None):
        self.name = name
        self.strength = strength if strength else rnd.uniform(0,1)

    # Redefine __str__ and __repr__ so the class can return string itself
    def __str__(self):
        return self.name

    def __repr__(self):
        return self.name

    # Redefine __lt__
    def __lt__(self, t):
        return self.strength < t.strength + rnd.gauss(0, Team.LUCK)

# Simulating the Data
## Take teams' strength from FIFA rankings pre-Euro 2020
teams_data = [[("Italy", 7), ("Wales", 17), ("Switzerland", 13), ("Turkey", 29)],
              [("Belgium", 1), ("Denmark", 10), ("Finland", 54), ("Russia", 38)],
              [("Netherlands", 16), ("Austria", 23), ("Ukraine", 24), ("North Macedonia", 62)],
              [("England", 4), ("Croatia", 14), ("Czech Republic", 40), ("Scotland", 44)],
              [("Sweden", 18), ("Spain", 6), ("Slovakia", 36), ("Poland", 21)],
              [("France", 2), ("Germany", 12), ("Portugal", 5), ("Hungary", 37)]]

ratings = sum([[rating for _,rating in group_data] for group_data in teams_data], [])
smallest = min(ratings)
largest = max(ratings)
teams = [[Team(name, 1 - (rating - smallest) / (largest - smallest))
         for name,rating in group_data] for group_data in teams_data]

## A function to simulate the data
def champion():
    ## Simulating the group stage
    after_groups = [sorted(group, reverse=True) for group in teams]
    third_placers = sorted([g[2] for g in after_groups], reverse=True)
    winners = sum([g[:2] for g in after_groups], [])
    teams16 = winners + third_placers

    ## Shuffle the 16 teams to arrange them into pairs for the knock-out stage
    rnd.shuffle(teams16)
    pairs16 = list(zip(teams16[::2], teams16[1::2]))

    # Find round of 16 teams and quarter-finalists
    teams8 = [sorted(g, reverse=True)[0] for g in pairs16]
    pairs8 = list(zip(teams8[::2], teams8[1::2]))
    teams4 = [sorted(g, reverse=True)[0] for g in pairs8]
    pairs4 = list(zip(teams4[::2], teams4[1::2]))

    # Find the semi-finalists
    teams2 = [sorted(g, reverse=True) for g in pairs4]
    first, second = sorted([teams2[0][0], teams2[1][0]], reverse=True)
    third, _ = sorted([teams2[0][1], teams2[1][1]], reverse=True)
    return first, second

# Create a dictionary to store teams and their win times
def result_list():
    team_list = [item for sublist in teams for item in sublist]
    result_lst = []
    for team in team_list:
        result_dict = {}
        result_dict['name'] = team
        result_dict['win'] = 0
        result_dict['runner_up'] = 0
        result_lst.append(result_dict)
    return (result_lst)

# Let run the simulation for certain trial times and count the number of times that a team would win

def simulation(result_list, trial_times: int):
    for i in range(1,trial_times):
        first, second = champion()
        for team in result_list:
            if first == team['name']:
                team['win'] += 1
            if second == team['name']:
                team['runner_up'] += 1
        i += 1
    return result_list

# Define main function
def main(trial_times: int):
    result_lst = result_list()
    df = pd.DataFrame(simulation(result_lst, trial_times))
    df['win_probability'] = df['win'] * 100 / trial_times
    df['runner_up_probability'] = df['runner_up'] * 100 / trial_times
    df = df.sort_values(by=['win','runner_up'], ascending=False)
    df.to_csv('result.csv')
    return df

if __name__ == '__main__':
    try:
        times = int(input("Number of times you want to simulate: "))
        print(main(times))
    except Exception as e:
        print(type(e).__name__ + str(e))
