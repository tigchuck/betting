import pandas as pd

# NFL22 = pd.read_excel('./nfl odds 2022-23.xlsx')
NFL21 = pd.read_excel('./nfl odds 2021-22.xlsx')
NFL20 = pd.read_excel('./nfl odds 2020-21.xlsx')
NFL19 = pd.read_excel('./nfl odds 2019-20.xlsx')
NFL18 = pd.read_excel('./nfl odds 2018-19.xlsx')
NFL17 = pd.read_excel('./nfl odds 2017-18.xlsx')


def spread(v, h, vs, hs):
    """ Returns scores adjusted by spread """
    if (vs == 'pk' or hs == 'pk'):
        return v, h
    elif (vs < hs):
        return v - vs, h
    else:
        return v, h - hs

def result(visitor, i, home, j, arr):
    """ Determines Winner """
    v_score = visitor['Final']
    h_score = home['Final']
    if (v_score > h_score):
        arr[i] = 'W'
        arr[j] = 'L'
    elif (v_score < h_score):
        arr[i] = 'L'
        arr[j] = 'W'
    else:
        arr[i] = arr[j] = 'T'

def result_ats(visitor, i, home, j, arr):
    v_score, h_score = spread(visitor['Final'], home['Final'], visitor['Close'], home['Close'])
    if (v_score > h_score):
        arr[i] = 'W'
        arr[j] = 'L'
    elif (v_score < h_score):
        arr[i] = 'L'
        arr[j] = 'W'
    else:
        arr[i] = arr[j] = 'T'

def win_ats(team, opponent):
    team_score, opp_score = spread(team['Final'], opponent['Final'], team['Close'], opponent['Close'])
    return team_score > opp_score

def road_dog(visitor, home):
    vs = visitor['Close']
    hs = home['Close']
    return vs != 'pk' and hs != 'pk' and vs > hs

def next_date(date):
    days = [31, 28, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31]
    date = str(date)
    n = len(date)
    month = int(date[:n - 2])
    day = int(date[n - 2:])
    if (day + 7 > days[month - 1]):
        day = (day + 7) % days[month - 1]
        if (month + 1 > 12):
            month = 1
        else:
            month += 1
    else:
        day += 7
    if (day < 10):
        return f'{month}0{day}'
    else:
        return f'{month}{day}'

def next_week(date1, date2):
    date1 = str(date1)
    n1 = len(date1)
    date2 = str(date2)
    n2 = len(date2)
    month1 = int(date1[:n1 - 2])
    day1 = int(date1[n1 - 2:])
    month2 = int(date2[:n2 - 2])
    day2 = int(date2[n2 - 2:])
    if (month1 > month2 or (month1 == 1 and month2 == 12)):
        return True
    elif (month1 == month2 and day1 >= day2):
        return True
    else:
        return False

def clean(teams, arr1, arr2):
    for team in teams:
        arr1[team] = None
        arr2[team] = None

def initialize(struct, arr1, arr2, teams):
    for i in range(0, 32, 2):
        a = struct.iloc[i, :]
        b = struct.iloc[i + 1, :]
        teams[a['Team']] = i
        teams[b['Team']] = i + 1
        result(a, i, b, i + 1, arr1)
        result_ats(a, i, b, i + 1, arr2)

prev_wl = [None] * 32
prev_wl_ats = [None] * 32
wins = 0
losses = 0


for struct in [NFL20, NFL21]:
    teams = dict()
    initialize(struct, prev_wl, prev_wl_ats, teams)
    i = 32
    week = 2
    date = struct.iloc[i, :]['Date']
    while (week < 18):
        not_played = set(range(32))
        date = next_date(date)
        while (not next_week(str(struct.iloc[i, :]['Date']), date)):
            a = struct.iloc[i, :]
            b = struct.iloc[i + 1, :]
            try:
                v = teams[a['Team']]
                h = teams[b['Team']]
            except KeyError:
                i += 2
                continue
            if (road_dog(a, b) and prev_wl[v] == 'L' and prev_wl_ats[v] == 'L' and prev_wl[h] == 'W' and prev_wl_ats[h] == 'W'):
                if (win_ats(a, b)):
                    if (a['Close'] > b['Close']):
                        print(f"Week {week} Matchup: {a['Team']} {a['Final']} @ {b['Team']} -{b['Close']} {b['Final']} -> WIN")
                    else:
                        print(f"Week {week} Matchup: {a['Team']} -{a['Close']} {a['Final']} @ {b['Team']} {b['Final']} -> WIN")
                    wins += 1
                else:
                    if (a['Close'] > b['Close']):
                        print(f"Week {week} Matchup: {a['Team']} {a['Final']} @ {b['Team']} -{b['Close']} {b['Final']} -> LOSS")
                    else:
                        print(f"Week {week} Matchup: {a['Team']} -{a['Close']} {a['Final']} @ {b['Team']} {b['Final']} -> LOSS")
                    losses += 1

            not_played.remove(v)
            not_played.remove(h)
            result(a, v, b, h, prev_wl)
            result_ats(a, v, b, h, prev_wl_ats)
            i += 2
        clean(not_played, prev_wl, prev_wl_ats)
        week += 1


print(f'Wins: {wins}, Losses: {losses}')
