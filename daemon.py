import time
import json
import socket
import pprint as p

from datetime import datetime
from kafka import KafkaProducer
from kafka import BrokerConnection
from influxdb import InfluxDBClient
from apscheduler.schedulers.background import BackgroundScheduler

from metrics import get_acess_token
from metrics import parking_data, parking_format_influx
from metrics import wirelessUsers_data, wirelessUsers_format_influx
from metrics import make_dhcp_request, make_website_request, make_storage_request

# jobs
def five_min_job(producer, influx):
    # parking data
    parking = parking_data()
    if parking:
        if kafkaConnection():
            if producer == "":
                producer = ProducerStart()
            try:
                producer.send("parking", value={"PARK" : parking})
                # print("\nsended parking to kafka:")
                # p.pprint({"PARK":parking})
            except:
                print("producer is bad, or not connected...")
        # parking data influx formated
        parking = parking_format_influx(parking)
        parking = [park[0] for park in parking]
        # print("\nsended parking to Influx!")
        # p.pprint(parking)
        influx.write_points(parking, database="Metrics")

def thirty_min_job(producer, influx, token):
    # number of wireless users data
    wireless_users = wirelessUsers_data(token)
    if wireless_users:
        if kafkaConnection():
            if producer == "":
                producer = ProducerStart()
            try:
                producer.send("wifiusr", value={"WIFIUSR" : wireless_users})
                # print("\nsended wirelessUseres to kafka:")
                # p.pprint({"WIFIUSR" : wireless_users})
            except:
                print("producer is bad, or not connected...")

        # wifiuseres data influx formated
        wireless_users = wirelessUsers_format_influx(wireless_users)
        wireless_users = [wire[0] for wire in wireless_users]
        # print("\nsended wirelessUseres to Influx:")
        # p.pprint(wireless_users)
        influx.write_points(wireless_users, database="Metrics")

def daily_job(producer,influx):
    url = 'https://wso2-gw.ua.pt/scom/v1.0/DHCP/Pools?days=1&hours=24'
    token_url = 'https://wso2-gw.ua.pt/token?grant_type=client_credentials&state=123&scope=openid'
    secret = 'BrszH8oF9QsHRjiOAC1D9Ze0Iloa'
    auth_type = 'Bearer'
    content_type = 'application/x-www-form-urlencoded'
    key = 'j_mGndxK2WLKEUKbGrkX7n1uxAEa'
    
    try:
        # val -> [name,status,value]
        result_request = make_dhcp_request(url,token_url,key,secret,content_type,auth_type)
        """
        if kafkaConnection():
            if producer == "":
                producer = ProducerStart()
            try:
                producer.send("dhcp_request",value={"dhcp_request":result_request})
            except:
                print("dhcp producer bad")
        """
        try:
            influx.write_points(result_request, database="Metrics")
        except:
            print('dhcp influx failed')
            
        for row in result_request:
            print(row)
    except:
        print('DHCP REQUEST FAILED')

    url = 'https://wso2-gw.ua.pt/scom/v1.0/WebSites/Metrics?days=1&hours=24'
    
    try:
        # val -> [name,status,value]
        result_request = make_website_request(url,token_url,key,secret,content_type,auth_type)
        """
        if kafkaConnection():
            if producer == "":
                producer = ProducerStart()
            try:
                producer.send("website_request",value={"website_request":result_request})
            except:
                print("website producer bad")
        """
        try:
            influx.write_points(result_request, database="Metrics")
        except:
            print('website influx failed')
        for row in result_request:
            print(row)
    except:
        print('WEBSITE REQUEST FAILED')
    
    url = 'https://wso2-gw.ua.pt/scom/v1.0/Storage'
    
    try:
        # val -> [name,status,value]
        result_request = make_storage_request(url,token_url,key,secret,content_type,auth_type)
        print(result_request)
        """
        if kafkaConnection():
            if producer == "":
                producer = ProducerStart()
            try:
                producer.send("storage_request",value={"storage_request":result_request})
            except:
                print("storage producer bad")
        """
        try:
            influx.write_points(result_request, database="Metrics")
        except:
            print('STORAGE influx failed')
    except:
        print('STORAGE REQUEST FAILED')

    
    
    
    
def kafkaConnection():
    # test connection with kafka broker
    conn = BrokerConnection("13.69.49.187", 9092, socket.AF_INET)
    timeout = time.time() + 1
    while time.time() < timeout:
        conn.connect()
        if conn.connected():
            break
    return conn.connected()

def ProducerStart():
    assert kafkaConnection()
    return KafkaProducer(bootstrap_servers=['13.69.49.187:9092'], value_serializer=lambda x: json.dumps(x, indent=4, sort_keys=True, default=str).encode('utf-8'))

def main():
    # start scheduler
    scheduler = BackgroundScheduler()
    # configure scheduler
    job_defaults = {
        'coalesce': False,
        'max_instances': 10
    }
    scheduler.configure(job_defaults=job_defaults)
    # get primecoreAPI access token
    token = get_acess_token()
    # test connection
    conn = kafkaConnection()
    producer = ""
    if conn:
        # start Kafka Python Client
        producer = ProducerStart()
    # start influxDBClient
    influx = InfluxDBClient(host='40.68.96.164', port=8086, username="peikpis", password="peikpis_2021")
    # add jobs
    scheduler.add_job(five_min_job, trigger="interval", args=[producer, influx], minutes=5, id="5minjob", next_run_time=datetime.now())
    scheduler.add_job(thirty_min_job, trigger="interval", args=[producer, influx, token], minutes=30, id="30minjob", next_run_time=datetime.now())
    
    scheduler.add_job(daily_job, trigger="interval", args=[producer, influx], days=1, id="dailyjob_basic", next_run_time=datetime.now())
    
    # scheduler.add_job(seven_day_job, trigger="interval", args=[influx, token], days=7, id="seven_day_job", next_run_time=datetime.now())
    # start the scheduler
    scheduler.start()
    try:
        while True:
            # simulate activity (which keeps the main thread alive)
            time.sleep(2)
    except (KeyboardInterrupt, SystemExit):
        print("\nexiting...")
        scheduler.shutdown()

if __name__=="__main__":
    main()
