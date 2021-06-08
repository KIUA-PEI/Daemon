# para cada entrada do values
# enviar uma entrada para a DB
# timestamp,instanceName,status,count
import requests
import json

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


#def dhcp_format_influx(val):
    # enviar a timestamp de val como timestamp
    # enviar o valor lido 
    # enviar o status
    # enviar o nome como nome da tabela + DHCP
#    pass

def filter_request(vals,status):
    result = []
    #print(vals)
    for metric in vals:
        name = metric['InstanceName']
        #print(metric)
        for value in metric['Values']:
            #print(name,status,value,metric['Values'][value])
            result.append({"time":value,"measurement":"dhcp_pool","tags":name,"fields":metric['Values'][value]})
    return result 

def make_dhcp_request(url,token_url,key,secret,content_type=None,auth_type=None):
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
        if request.status_code<=200:
            for row in request.json():
                print(row)
            try:
                result = []
                for val in request.json():
                    result = filter_request(val['Metrics'],val['Status'])
                return result
            except:
                print("FILTER FAILED")  
        elif request.status_code == 401:
            token = get_token(token_url,key,secret,content_type,auth_type)
        elif request.status_code == 403:
            print("TOKEN REQUEST FORBIDDEN")
        else:
            count += 1

    return

def main():
    url = 'https://wso2-gw.ua.pt/scom/v1.0/DHCP/Pools?days=1&hours=24'
    token_url = 'https://wso2-gw.ua.pt/token?grant_type=client_credentials&state=123&scope=openid'
    secret = 'BrszH8oF9QsHRjiOAC1D9Ze0Iloa'
    auth_type = 'Bearer'
    content_type = 'application/x-www-form-urlencoded'
    key = 'j_mGndxK2WLKEUKbGrkX7n1uxAEa'

    result = make_dhcp_request(url,token_url,key,secret,content_type,auth_type)
    # for val in result:
    #     # print(val)
    # pass


if __name__=="__main__":
    main()