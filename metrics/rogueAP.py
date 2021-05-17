import requests
import json
import datetime as dt

from .consts import *
from .util import *
from datetime import datetime, timedelta


#temp
import pprint as p

def num_rogue_ap_data(token, week_ago=None):
    num_rogue_ap = 0
    if week_ago == None:
        week_ago = datetime.now() - timedelta(days=7)

    r = requests.get("https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/RogueAccessPointAlarm/Count", headers={'Authorization': token})

    print("r.status_code:" +  str(r.status_code))
    
    if r.status_code == 401:
        token = get_acess_token()
        return num_rogue_ap_data(token, week_ago)

    if r.status_code == 400:
        
        return None
    
    elif r.status_code == 200:
        num_entrys = json.loads(r.text)["count"]
        past_week_ago = False

        while not past_week_ago:
            print("teste")
            num_entrys = num_entrys - 100
            print("https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/RogueAccessPointAlarm?maxResult=100&firstResult="+str(num_entrys))
            r = requests.get("https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/RogueAccessPointAlarm?maxResult=100&firstResult="+str(num_entrys), headers={'Authorization': token})
            print(r.status_code)
            
            if r.status_code == 401:
                token = get_acess_token()
                return num_rogue_ap_data(token, week_ago)

            if r.status_code == 500:
                print("internal server error!")

            if r.status_code == 200:
                data = json.loads(r.text)
                for rogue in data["rogueAccessPointAlarms"]:
                    time = dt.datetime.strptime(rogue["timeStamp"], '%Y-%m-%dT%H:%M:%S.%fZ')
                    print(time.isoformat())
                    print("time > week_ago: "+str(time > week_ago))
                    if time > week_ago:
                        num_rogue_ap = num_rogue_ap + 1 if rogue["severity"] == "MINOR" or rogue["severity"] == "CRITICAL" else num_rogue_ap
                    else:
                        past_week_ago = True
    return num_rogue_ap
                    


