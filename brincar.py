import kafka
from kafka import BrokerConnection
import time
import socket

# def somefuncA(a, b, bool):
#     print("on somefuncA: ")
#     print("bolb value:" + str(bool))
#     if "boolx" in globals():
#         print("bolbx value:" + str(boolx))
#     else:
#         print("variable boolx dont exists")

# def somefuncB(bool):
#     print("on somefuncB: ")
#     print("changed from True to False")
#     global boolx
#     bool = False
#     boolx = bool
    



# def main():
#     boolb = True

#     somefuncA("2", "4", boolb)

#     somefuncB(boolb)

#     somefuncA("2", "4", boolb)

# main()


conn = BrokerConnection("13.69.49.187", 9092, socket.AF_INET)
timeout = time.time() + 1
while time.time() < timeout:
    conn.connect()
    if conn.connected():
        break
print("kafka begin state: " + str(conn.connected()))

while True:
    conn = BrokerConnection("13.69.49.187", 9092, socket.AF_INET)
    timeout = time.time() + 1
    while time.time() < timeout:
        conn.connect()
        if conn.connected():
            break
    print("kafka state: " + str(conn.connected()))
    time.sleep(4)
