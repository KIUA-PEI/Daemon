import time
import json
import kafka
import requests
import socket

from consts import *
from datetime import datetime
from kafka import KafkaProducer
from kafka import BrokerConnection
from influxdb import InfluxDBClient
from apscheduler.schedulers.background import BackgroundScheduler

from metrics import get_acess_token
from metrics import parking_data, parking_format_influx
from metrics import wirelessUsers_data, wirelessUsers_format_influx

# jobs
def five_min_job(producer, influx, keys):
    # parking data
    parking = parking_data()
    keys["parking"] = keys["parking"] + 1

    if kafkaConnection():
        if producer == "":
            producer = ProducerStart()
        try:
            producer.send("parking", value={"PARK"+str(keys["parking"]) : parking})
        except:
            print("producer is bad, or not connected...")

    # parking data influx formated
    parking = parking_format_influx(parking)
    parking = [park[0] for park in parking]
    influx.write_points(parking, database="Metrics")

def thirty_min_job(producer, influx, token, keys):
    # number of wireless users data
    wireless_users = wirelessUsers_data(token)
    keys["wirelessUsers"] = keys["wirelessUsers"] + 1
    if kafkaConnection():
        if producer == "":
            producer = ProducerStart()
        try:
            producer.send("wifiusr", value={"WIFIUSR"+str(keys["wirelessUsers"]) : wireless_users})
        except:
            print("producer is bad, or not connected...")

    # wifiuseres data influx formated
    wireless_users = wirelessUsers_format_influx(wireless_users)
    wireless_users = [w[0] for w in wireless_users]
    influx.write_points(wireless_users, database="Metrics")

def kafkaConnection():
    # test connection to kafka
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
    print("runs main")
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

    # test connection to kafka
    conn = kafkaConnection()

    producer = ""
    if conn:
        # start Kafka Python Client
        producer = ProducerStart()()

    # start influxDBClient
    influx = InfluxDBClient(host='40.68.96.164', port=8086, username="peikpis", password="peikpis_2021")

    # add jobs
    scheduler.add_job(five_min_job, trigger="interval", args=[producer, influx, KAFKAKEYS], minutes=5, id="5minjob", next_run_time=datetime.now())
    scheduler.add_job(thirty_min_job, trigger="interval", args=[producer, influx, token, KAFKAKEYS], minutes=30, id="30minjob", next_run_time=datetime.now())

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

