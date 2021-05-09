import requests
import json

from .consts import *
from .util import *
from datetime import datetime, timedelta

def num_rogue_ap_data(token, week_ago=None):
    if week_ago == None:
        week_ago = datetime.now() - timedelta(days=7)

    r = requests.get("https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/RogueAccessPointAlarm/Count", headers={'Authorization': token})
    
    if r.status_code == 401:
        token = get_acess_token()
        num_rogue_ap_data(token, week_ago)
    
    elif r.status_code == 200:
        num_entrys = json.loads(r.text)["count"]
        past_week_ago = False

        # while not past_week_ago:
        #     num_entrys = num_entrys - 100
        #     r = requests.get("https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/RogueAccessPointAlarm?firstResult="+str(num_entrys), headers={'Authorization': token})
        #     # do a loop calling a function to make the consecutive requests
