import requests
from datetime import datetime as dt
from .consts import *
from .util import *


def parking_data():
    """
    Returns data on response.status_code == 200
    
    returns None on response.status_code == 400
    """
    r = requests.get("http://services.web.ua.pt/parques/parques")
    # print(r.json())
    if r.status_code == 200:
        parking = r.json()
        timestamp = parking.pop(0)
        parking = [{"Nome":park["Nome"], "Capacidade" : park["Capacidade"], "Ocupado" : park["Ocupado"], "Livre" : park["Livre"]} for park in parking]
        parking.insert(0, timestamp)
        return parking

    elif r.status_code == 400:
        print("\n[parking]: API response 400, skipped...")
        return None

def parking_format_influx(parking):
    """gets a list of json like database entrys"""
    db_entrys = []
    timestamp = parking.pop(0)["Timestamp"]
    time = dt.fromtimestamp(timestamp).isoformat()
    for park in parking:
        db_entrys.append(create_entry("parking", {"Nome": park["Nome"]}, str(time), {"Ocupado" : park["Ocupado"], "Livre" : park["Livre"], "Capacidade" : park["Capacidade"]}))
    return db_entrys
