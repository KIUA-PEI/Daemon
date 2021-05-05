import requests
import json
from .consts import *
from .util import *

def wirelessUsers_data(token):
    number_users = WIFIUSERS
    for i in range(8):
        r = requests.get('https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/AccessPoint?maxResult=1000&firstResult='+str(i*100), headers={'Authorization': token})
        
        if r.status_code == 401:
            token = get_acess_token()
            wirelessUsers_data(token)
            break
        
        elif r.status_code == 200:
            data = json.loads(r.text)
            for ap in data["accessPoints"]:
                for dep in DEP:
                    try:
                        if ap["name"].split("-ap")[0] == dep:
                            number_users[dep] = number_users[dep] + ap["clientCount"]
                    except Exception:
                        print("Error parsing...")

        elif r.status_code == 400:
            pass
            ## loggar para um ficheiro a dizer que a api parking deu erro para posterior investigação
            ## a defenir

    return [{"Timestamp" : get_timestamp()}, number_users]

def wirelessUsers_format_influx(wirelessUsers):
    db_entrys = []
    timestamp = wirelessUsers.pop(0)["Timestamp"]
    for wifi in wirelessUsers[0]:
        db_entrys.append(create_entry("wifiusr", {"Nome": wifi}, str(timestamp), {"wifiCount": wirelessUsers[0][wifi]}))
    return db_entrys
    

# print(number_users) 29 abril, 18:36
# {
#     'deti': 201, 'biblioteca': 288, 'aauav': 10, 'dbio': 126, 'deca': 105, 
#     'dmat': 107, 'decivil': 52, 'fis': 132, 'dem': 95, 'geo': 29, 'cpct': 210, 
#     'dcspt': 45, 'essua': 175, 'cicfano': 63, 'degeit': 116, 'dq': 87, 
#     'it': 54, 'dao': 38, 'dep': 54, 'dlc': 69, 'isca': 75, 'ietta': 0
# }