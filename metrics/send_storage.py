import requests
import json
import base64
from pytz import timezone, common_timezones
from datetime import datetime
from kafka import KafkaProducer
from kafka import BrokerConnection
from influxdb import InfluxDBClient
from apscheduler.schedulers.background import BackgroundScheduler
import time
import socket
import pprint as p
from .util import *


def filter_request(vals):
    result = []
    #print(vals)
    
    for node in vals:
        #name = node['InstanceName']
        # print(node)
        result.append({"time":get_timestamp(),"measurement":"Node_Storage","tags":node['NodeName'],"fields":node['BytesUsed']})
    
    return result 

# days = 1 ... hours = 24


def make_storage_request(url,token_url,key,secret,content_type=None,auth_type=None):
    # request_token
    count = 0
    token = None 
    
    while not token:
        token = get_token(token_url,key,secret,content_type,auth_type)
        count += 1
        if count >= 4:
            print('token request failed')
            return None
    
    count = 0
    while count < 4:
        request = requests.get(url,headers={'Authorization': token},timeout=120)
        # print(request.status_code)
        # print(request.json())
        if request.status_code==200:
            try:
                result = filter_request(request.json()['Nodes'])
                return result
            except:
                print("FILTER FAILED") 
                break
        elif request.status_code == 401:
            token = get_token(token_url,key,secret,content_type,auth_type)
            print("UNAUTHORIZED")
            return False
        elif request.status_code == 403:
            print("REQUEST FORBIDDEN")
            return False
        else:
            count += 1

    return

def main():
    url = 'https://wso2-gw.ua.pt/scom/v1.0/Storage'
    token_url = 'https://wso2-gw.ua.pt/token?grant_type=client_credentials&state=123&scope=openid'
    secret = 'BrszH8oF9QsHRjiOAC1D9Ze0Iloa'
    auth_type = 'Bearer'
    content_type = 'application/x-www-form-urlencoded'
    key = 'j_mGndxK2WLKEUKbGrkX7n1uxAEa'

    make_storage_request(url,token_url,key,secret,content_type,auth_type)
    
    pass


if __name__=="__main__":
    main()