import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from metrics import parking_data, parking_format_influx
import json

parking = [ 
    {"Timestamp":1423519992},
    {"Nome":"Residencias","Capacidade":663,"Ocupado":5,"Livre":658}, 
    {"Nome":"Biblioteca","Capacidade":249,"Ocupado":2,"Livre":247}, 
    {"Nome":"ZTC","Capacidade":10,"Ocupado":0,"Livre":10}, 
    {"Nome":"Subterraneo","Capacidade":74,"Ocupado":0,"Livre":74}, 
    {"Nome":"Ceramica","Capacidade":42,"Ocupado":4,"Livre":38}, 
    {"Nome":"Linguas","Capacidade":36,"Ocupado":2,"Livre":34}, 
    {"Nome":"Incubadora","Capacidade":74,"Ocupado":22,"Livre":52}, 
    {"Nome":"ISCAA Publico","Capacidade":95,"Ocupado":0,"Livre":95}, 
    {"Nome":"ISCAA Funcionarios","Capacidade":46,"Ocupado":1,"Livre":45}, 
    {"Nome":"ESTGA","Capacidade":188,"Ocupado":15,"Livre":173}
]

r = parking_format_influx(parking)

print(json.dumps(r[0], indent=4))


