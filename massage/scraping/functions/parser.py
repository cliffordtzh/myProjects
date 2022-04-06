import pandas as pd
import json
import re

def parse_basic_info(df, data):
    basic_info = ["Name", "Address", "Rating", "Phone", "Website"]

    res = []
    for info in basic_info:
        if data[info] != None:
            if info == "Rating":
                idx = data[info].find("\n")
                res.append(data[info][0:idx])
            elif type(data[info]) == str:
                res.append(data[info].replace("\n", ""))
            else:
                res.append(data[info])
        else:
            res.append(data[info])

    entry = pd.DataFrame([res], columns = basic_info)
    df = df.append(entry, ignore_index = True)
    return df


def parse_opening_hours(df, data):
    dow = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    raw_string = data["Opening Hours"]
    name = data["Name"]
    if raw_string != None:
        raw_string = raw_string.replace("\u2013", "-")
        indices = sorted([raw_string.find(day) for day in dow])
        
        res = []
        i = 0
        while i < len(dow): 
            if i == len(dow)-1:
                curr_idx = indices[-1]
                next_idx = 999
            else:
                curr_idx = indices[i]
                next_idx = indices[i + 1]

            string_subset = raw_string[curr_idx: next_idx]
            matched = re.search("([0-9]+:)?([0-9]+)(am|pm)\-([0-9]+:)?([0-9]+)(am|pm)", string_subset)
            if matched:
                opening_hours = matched.group(0)
            else:
                opening_hours = None
            res.append(opening_hours)
            i += 1
    else:
        res = [None] * 7


    entry = pd.DataFrame([[name] + res], columns = ["Name"] + dow)
    df = df.append(entry, ignore_index = True)
    return df


def parse_reviews(data, path):
    all_reviews = data["Reviews"]
    if all_reviews != None:
        name = data["Name"].strip("\n")
        name = re.sub("[/|]", "", name)

        with open(f"{path}/{name}.txt", 'w') as f:
            no_ascii = list(map(lambda x: x.encode("ascii", "ignore").decode(), all_reviews))
            f.writelines(no_ascii)

