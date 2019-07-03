import json
import numpy as np

champion_to_tier = {}
with open("champions.json", 'r') as f:
    for champion in json.loads(f.read()):
        champion_to_tier[champion['name']] = champion['tier']

champion_to_index = dict(zip(list(champion_to_tier.keys()), range(len(champion_to_tier))))
index_to_champion = dict([(champion_to_index[x], x) for x in champion_to_index])
NUM_CHAMPIONS = len(champion_to_index)

level_tier_probability = np.array([
    [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, 1.0, 0.0, 0.0, 0.0, 0.0],
    [0.0, .65, .30, .05, 0.0, 0.0],
    [0.0, .50, .35, .15, 0.0, 0.0],
    [0.0, .37, .35, .25, .03, 0.0],
    [0.0, .245, .35, .30, .1, 0.005],
    [0.0, .20, .30, .33, .15, .02],
    [0.0, .15, .25, .35, .2, .05],
    [0.0, .10, .15, .35, .30, .1],
])

def get_champion_distribution(board, level):
    # board is a list of Champion name and level pair [(Yasuo, 3)]
    # Given the board as well as your level, give a distribution over all possible champions you can draw
    champion_to_remaining = {}
    tier_to_initial_count = {
        1: 39,
        2: 26,
        3: 21,
        4: 13,
        5: 10
    }
    for champion in champion_to_tier:
        tier = champion_to_tier[champion]
        champion_to_remaining[champion] = tier_to_initial_count[tier]

    for (champion, level) in board:
        if level == 1:
            champion_to_remaining[champion] -= 1
        elif level == 2:
            champion_to_remaining[champion] -= 3
        elif level == 3:
            champion_to_remaining[champion] -= 9

    tier_count = {1: 0, 2: 0, 3: 0, 4: 0, 5: 0}
    for champion in champion_to_remaining:
        remaining = champion_to_remaining[champion]
        tier = champion_to_tier[champion]
        tier_count[tier] += remaining

    champion_distribution = np.zeros(NUM_CHAMPIONS)

    for i in range(NUM_CHAMPIONS):
        tier = champion_to_tier[index_to_champion[i]]
        champion_distribution[i] = level_tier_probability[level][tier]*champion_to_remaining[index_to_champion[i]]/tier_count[tier]

    return champion_distribution

champion_distribution = get_champion_distribution([('Nidalee', 3)], 3)
print(champion_distribution.sum())
