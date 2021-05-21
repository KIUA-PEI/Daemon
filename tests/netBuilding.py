
import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from metrics import netBuilding_format_influx
from metrics import get_acess_token
import json


token = get_acess_token()

netBuilding_format_influx(token)

