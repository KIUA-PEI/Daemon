import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

import json
from metrics import wirelessUsers_data, wirelessUsers_format_influx


wirelessUsers = [
    {"Timestamp":1423519992},
    {'deti': 201, 'biblioteca': 288, 'aauav': 10, 'dbio': 126, 'deca': 105, 
    'dmat': 107, 'decivil': 52, 'fis': 132, 'dem': 95, 'geo': 29, 'cpct': 210, 
    'dcspt': 45, 'essua': 175, 'cicfano': 63, 'degeit': 116, 'dq': 87, 
    'it': 54, 'dao': 38, 'dep': 54, 'dlc': 69, 'isca': 75, 'ietta': 0}
]

r = wirelessUsers_format_influx(wirelessUsers)

print(r)

print(json.dumps(r, indent=4))