import os,sys,inspect
currentdir = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
parentdir = os.path.dirname(currentdir)
sys.path.insert(0,parentdir) 

from metrics import num_rogue_ap_data
from metrics import get_acess_token

token = get_acess_token()

num_rogue_ap_data(token)