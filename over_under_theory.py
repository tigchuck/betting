import pandas as pd

# NFL22 = pd.read_excel('./nfl odds 2022-23.xlsx')
NFL21 = pd.read_excel('./nfl odds 2021-22.xlsx')
NFL20 = pd.read_excel('./nfl odds 2020-21.xlsx')
NFL19 = pd.read_excel('./nfl odds 2019-20.xlsx')
NFL18 = pd.read_excel('./nfl odds 2018-19.xlsx')
NFL17 = pd.read_excel('./nfl odds 2017-18.xlsx')


def prev_game(struct, i):
    team = struct.iloc[i, :]['Team']
    i -= 1
    while (i >= 0):
        if (struct.iloc[i, :]['Team'] == team):
            return i
        i -= 1
    return i

def opponent(struct, i):
    if (struct.iloc[i, :]['VH'] == 'V'):
        return i + 1
    else:
        return i - 1

def last_game_over(struct, i):
    i = prev_game(struct, i)
    if (i < 0):
        return False
    else:
        j = opponent(struct, i)
        line = get_line(struct, min(i, j))
        total = get_total(struct, min(i, j))
        return over(total, line)

def last_game_under(struct, i):
    i = prev_game(struct, i)
    if (i < 0):
        return False
    else:
        j = opponent(struct, i)
        line = get_line(struct, min(i, j))
        total = get_total(struct, min(i, j))
        return under(total, line)

def last_game_win(struct, i):
    i = prev_game(struct, i)
    if (i < 0):
        return False
    else:
        j = opponent(struct, i)
        return struct.iloc[i, :]['Final'] > struct.iloc[j, :]['Final']

def get_line(struct, i):
    a = struct.iloc[i, :]['Close']
    b = struct.iloc[i + 1, :]['Close']
    if (a == 'pk'):
        return b
    elif(b == 'pk'):
        return a
    else:
        return max(float(a), float(b))

def get_total(struct, i):
    a = struct.iloc[i, :]['Final']
    b = struct.iloc[i + 1, :]['Final']
    return a + b

def over(total, line):
    return total > line

def under(total, line):
    return total < line

def last_game_win_and_cover(struct, i):
    i = prev_game(struct, i)
    if (i < 0):
        return False
    else:
        j = opponent(struct, i)
        a = struct.iloc[i, :]['Final']
        b = struct.iloc[j, :]['Final']
        s = spread(struct, i)
        if (underdog(struct, i)):
            return a - b > 0
        else:
            return a - s - b > 0

def last_game_loss_and_fail(struct, i):
    i = prev_game(struct, i)
    if (i < 0):
        return False
    else:
        j = opponent(struct, i)
        a = struct.iloc[i, :]['Final']
        b = struct.iloc[j, :]['Final']
        s = spread(struct, i)
        if (underdog(struct, i)):
            return a + s - b < 0
        else:
            return a - b < 0

def spread(struct, i):
    j = opponent(struct, i)
    a = struct.iloc[i, :]['Close']
    b = struct.iloc[j, :]['Close']
    if (a == 'pk' or b == 'pk'):
        return 0
    else:
        return min(float(a), float(b))

def underdog(struct, i):
    j = opponent(struct, i)
    a = struct.iloc[i, :]['Close']
    b = struct.iloc[j, :]['Close']
    if (a == 'pk' or b == 'pk'):
        return False
    else:
        return float(a) > float(b)

def favorite(struct, i):
    j = opponent(struct, i)
    a = struct.iloc[i, :]['Close']
    b = struct.iloc[j, :]['Close']
    if (a == 'pk' or b == 'pk'):
        return False
    else:
        return float(a) < float(b)

wins = 0
losses = 0
ties = 0

for struct in [NFL21, NFL20, NFL19, NFL18, NFL17]:
    for i in range(0, len(struct), 2):
        if (underdog(struct, i) and last_game_loss_and_fail(struct, i) and last_game_win_and_cover(struct, i + 1)):
            a = int(struct.iloc[i, :]['Final']) + spread(struct, i)
            b = int(struct.iloc[i + 1, :]['Final'])
            # print(struct.iloc[i, :]['Team'], a, struct.iloc[i + 1, :]['Team'], b)
            if (a > b):
                wins += 1
            elif (a < b):
                losses += 1
            else:
                ties += 1
            

print(f'{wins} - {losses} - {ties}  ({(wins / (wins + losses)) * 100}%)')
