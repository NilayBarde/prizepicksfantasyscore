import statsapi
import math
from statistics import mean, median
import requests
import pandas as pd
from decimal import Decimal

WIN_VAL = 6
QS_VAL = 4
ER_VAL = -3
SO_VAL = 3
O_VAL = 1

SINGLE_VAL = 3
DOUBLE_VAL = 5
TRIPLE_VAL = 8
HOMERUN_VAL = 10
RUN_VAL = 2
RBI_VAL = 2
BB_VAL = 2
HBP_VAL = 2
SB_VAL = 5

def get_player_ids(name):
    players = statsapi.lookup_player(name)
    player_ids = []
    for id_ in players:
        player_ids.append(id_['id'])
    
    if (len(player_ids) <= 0):
        print("Player does not exist.")
        exit()
    elif (len(player_ids) > 1):
        print("Too many players with this name. Enter complete name.")
        exit()
    else:
        return str(player_ids[0])

def get_pitching_fantasy_score(name):
    fantasy_scores = []
    player_id = get_player_ids(name)

    response = requests.get('https://statsapi.mlb.com/api/v1/people/' + player_id + '/stats?stats=gameLog&leagueListId=mlb_hist&group=pitching&gameType=R&sitCodes=1,2,3,4,5,6,7,8,9,10,11,12&hydrate=team&season=2022&language=en')
    data = response.json()
    stats = data['stats'][0]
    splits = stats['splits']
    for split in splits:
        if split['stat']['wins'] > 0:
            win_fs = WIN_VAL
        else:
            win_fs = 0
        er = split['stat']['earnedRuns']
        er_fs = er * ER_VAL
        so_fs = split['stat']['strikeOuts'] * SO_VAL
        outs = (split['stat']['inningsPitched'])
        outs = Decimal(outs)
        outs_fs = math.floor(outs) * 3 * O_VAL + Decimal(outs % 1 * 10) * O_VAL
        if outs >= 6 and er <= 3:
            qs_fs = QS_VAL
        else:
            qs_fs = 0

        total = win_fs + er_fs + so_fs + outs_fs + qs_fs
        fantasy_scores.append(total)
    return fantasy_scores
    
def get_hitting_fantasy_score(name):
    fantasy_scores = []
    player_id = get_player_ids(name)

    response = requests.get('https://statsapi.mlb.com/api/v1/people/' + player_id + '/stats?stats=gameLog&leagueListId=mlb_hist&group=hitting&gameType=R&sitCodes=1,2,3,4,5,6,7,8,9,10,11,12&hydrate=team&season=2022&language=en')
    data = response.json()
    stats = data['stats'][0]
    splits = stats['splits']
    for split in splits:
        doubles = split['stat']['doubles']
        doubles_fs = doubles * DOUBLE_VAL

        triples = split['stat']['triples']
        triples_fs = triples * TRIPLE_VAL

        homeruns = split['stat']['homeRuns']
        homeruns_fs = homeruns * HOMERUN_VAL

        runs_fs = split['stat']['runs'] * RUN_VAL
        rbi_fs = split['stat']['rbi'] * RBI_VAL
        bb_fs = split['stat']['baseOnBalls'] * BB_VAL
        hbp_fs = split['stat']['hitByPitch'] * HBP_VAL
        sb_fs = split['stat']['stolenBases'] * SB_VAL
        singles_fs = split['stat']['hits'] - doubles - triples - homeruns * SINGLE_VAL

        total = singles_fs + doubles_fs + triples_fs + homeruns_fs + runs_fs + rbi_fs + bb_fs + hbp_fs + sb_fs
        fantasy_scores.append(total)
    return fantasy_scores
        
def main():
    player_name = input("Enter player's name: ")
    type = input("Enter p for pitching stats or h for hitting stats: ")
    fantasy_scores = []
    if type == "p":
        fantasy_scores = get_pitching_fantasy_score(player_name)
    elif type == "h":
        fantasy_scores = get_hitting_fantasy_score(player_name)
    
    print("Average Fantasy Score: " + str(mean(fantasy_scores)))
    print("Median Fantasy Score: " + str(median(fantasy_scores)))
    print(*fantasy_scores)

if __name__ == "__main__":
    main()