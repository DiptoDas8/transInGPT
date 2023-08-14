import json
from pprint import pprint

with open('./collinfo.json', 'r') as f:
    collinfo = json.load(f)
    collinfo = [entry['id'].replace('CC-MAIN-', '') for entry in collinfo]
    byyear = dict()
    for idx in collinfo:
        year = idx.split('-')[0]
        if year not in byyear.keys():
            byyear[year] = [idx]
        else:
            byyear[year].append(idx)
            byyear[year].sort(reverse=True)

with open('by_year_indices.json', 'w') as fout:
    json.dump(byyear, fout, indent=4)