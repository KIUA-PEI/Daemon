import requests
from datetime import datetime as dt
from .consts import *
from .util import *


def parking_data():
    parking = ""
    r = requests.get("http://services.web.ua.pt/parques/parques")
    # print(r.json())
    if r.status_code == 200:
        parking = r.json()
        timestamp = parking.pop(0)
        parking = [{"Nome":park["Nome"], "Capacidade" : park["Capacidade"], "Ocupado" : park["Ocupado"], "Livre" : park["Livre"]} for park in parking]
        parking.insert(0, timestamp)

    elif r.status_code == 400:
        pass
        ## loggar para um ficheiro a dizer que a api parking deu erro para posterior investigação
        ## a defenir
    return parking

def parking_format_influx(parking):
    """gets a list of json like database entrys"""
    db_entrys = []
    timestamp = parking.pop(0)["Timestamp"]
    time = dt.fromtimestamp(timestamp).isoformat()
    for park in parking:
        db_entrys.append(create_entry("parking", {"Nome": park["Nome"]}, str(time), {"Ocupado" : park["Ocupado"], "Livre" : park["Livre"], "Capacidade" : park["Capacidade"]}))
    return db_entrys
