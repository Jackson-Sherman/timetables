import numpy as np
import pandas as pd
import re
from datetime import time
from tiempo import mytime

TIME_REGEX = re.compile("(1?\d:\d\d [AP]M) - (1?\d:\d\d [AP]M) \[([^]]+)\]")

NICKNAMES = {
    "North Planet Snoopy": "N Pie",
    "South Planet Snoopy": "S Pie",
    "East Planet Snoopy": "E Pie",
    "West Planet Snoopy": "W Pie",
    "Flight of Fear": "FoF",
    "Antique Autos": "Antiques",
    "Monster": "MSD",
    "Drop Tower": "Drop/Bat",
    "Invertigo": "GoGo",
    "Adventure Express": "Adv Exp"
}

SHIFTS = {
    "AD":  ((mytime( "4:30 AM"),mytime("10:44 AM")), (mytime("9:30 PM"),mytime("4:29 AM"))),
    "O":   ((mytime( "4:30 AM"),mytime("10:44 AM")), (mytime("4:30 AM"),mytime("6:29 PM"))),
    "OS":  ((mytime( "4:30 AM"),mytime("10:44 AM")), (mytime("6:30 PM"),mytime("9:29 PM"))),
    "OpoS":((mytime("10:45 AM"),mytime( "1:29 PM")), (mytime("4:30 AM"),mytime("6:29 PM"))),
    "S":   ((mytime("10:45 AM"),mytime( "1:29 PM")), (mytime("6:30 PM"),mytime("9:29 PM"))),
    "CpoS":((mytime( "1:30 PM"),mytime("11:59 PM")), (mytime("6:30 PM"),mytime("9:29 PM"))),
    "SC":  ((mytime("10:45 AM"),mytime( "1:29 PM")), (mytime("9:30 PM"),mytime("4:29 AM"))),
    "C":   ((mytime( "1:30 PM"),mytime("11:59 PM")), (mytime("9:30 PM"),mytime("4:29 AM")))
}

SHIFT_ORDER = ("AD", "O", "OS", "S", "SC", "C")

def between(val, low, high):
    if high == low: return val == high
    if high == val or val == low: return True
    if high < low:
        return low < val or val < high
    return low < val and val < high

def shift_type(start, end):
    for shift in SHIFTS:
        spans = SHIFTS[shift]
        if between(start, *spans[0]) and between(end, *spans[1]):
            return shift
    return "Null"

def time_match_to_vals(match):
    groups = match.groups()
    
    t0, t1 = [mytime(groups[i]) for i in (0,1)]
    length = float(groups[-1])
    return t0, t1, length

PLACE_REGEX = re.compile("(\d{4}) ([^/]+)/Ride Operator")

place_match_to_vals = lambda match: (int(match.groups()[0]), match.groups()[1])

def get_data(fp="shifts.txt"):
    output = {
        "id": [],
        "pos": [],
        "type": [],
        "start": [],
        "end": [],
        "len": []
    }
    with open(fp, 'r') as file:
        lines = [line for line in file.readlines() if line]
    
    times = [TIME_REGEX.search(line) for line in lines]
    times = [time_match_to_vals(t) for t in times if t is not None]

    places = [PLACE_REGEX.search(line) for line in lines]
    places = [place_match_to_vals(p) for p in places if p is not None]

    for t, p in zip(times, places):
        output["id"].append(p[0])
        output["pos"].append(NICKNAMES[p[1]] if p[1] in NICKNAMES else p[1])
        output["type"].append(shift_type(t[0], t[1]))
        output["start"].append(t[0])
        output["end"].append(t[1])
        output["len"].append(t[2])
    
    return pd.DataFrame(output)

df = get_data()

print(df)
print()

for p in sorted(set(df.get("pos"))):
    print(p)
