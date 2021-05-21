import json
import requests
from requests.models import DEFAULT_REDIRECT_LIMIT
from .consts import *
from .util import *

def netBuilding_format_influx(token):
    r = requests.get("https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/Building", headers={'Authorization': token})

    if r.status_code == 200:
        buildings = json.loads(r.text)["buildings"]
        print(buildings)
        
        # data structure
        # data = {building = [ [timestamp, [rx], [tx]], [...] }
        
        # rx = tráfego recebido (incoming)
        # tx = tráfego transmitido (outgoing)
        for b in buildings:
            # r = requests.get("https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/NetworkMetric/"+b+"?metric=rx&timeInterval=1", headers={'Authorization': token})
            # datarx = json.loads(r.text)["metricsData"]["values"]
            # print(datarx)
            # r = requests.get("https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/NetworkMetric/"+b+"?metric=tx&timeInterval=1", headers={'Authorization': token})

            if r.status_code == 200:
                
                pass

            elif r.status_code == 401:
                pass
            
            elif r.status_code == 400:
                pass

    elif r.status_code == 401:
        token = get_acess_token()
        return netBuilding_format_influx(token)

    elif r.status_code == 400:
        return None