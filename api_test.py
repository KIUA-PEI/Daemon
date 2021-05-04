import requests 
import json
#import pycurl
#       Host: https://wso2-gw.ua.pt
#       Context: /primecore_primecore-ws/1.0.0
#       Consumer key: j_mGndxK2WLKEUKbGrkX7n1uxAEa
#       Consumer secret: BrszH8oF9QsHRjiOAC1D9Ze0Iloa


#   curl --location --request POST 'https://wso2-gw.ua.pt/token?grant_type=client_credentials&state=123&scope=openid' \ --header 'Content-Type: application/x-www-form-urlencoded' \ --header 'Authorization: Basic al9tR25keEsyV0xLRVVLYkdya1g3bjF1eEFFYTpCcnN6SDhvRjlRc0hSamlPQUMxRDlaZTBJbG9h'
def get_acess_token():
    request_token = requests.post('https://wso2-gw.ua.pt/token?grant_type=client_credentials&state=123&scope=openid', \
    headers = {'Content-Type': 'application/x-www-form-urlencoded','Authorization': 'Basic al9tR25keEsyV0xLRVVLYkdya1g3bjF1eEFFYTpCcnN6SDhvRjlRc0hSamlPQUMxRDlaZTBJbG9h'})
    print('new token -> %s' % request_token.json()['access_token'])
    
    return 'Bearer ' + request_token.json()['access_token']

token = get_acess_token()

def explore_access_points():
    # print(r.text)
    # print(r.headers)

    highest_aps = {
        "deti" : 0, "biblio" : 0, "aauav" : 0, "dbio" : 0, "deca" : 0,
        "dmat" : 0, "decivil" : 0, "fis" : 0, "dem" : 0, "geo" : 0, "cpct" : 0,
        "dcspt" : 0, "essua" : 0, "cicfano" : 0, "degeit" : 0, "dq" : 0, "it" : 0,
        "dao" : 0, "dep" : 0, "dlc" : 0, "isca" : 0, "ietta" : 0
    }

    for i in range(8):
        print("https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/AccessPoint?maxResult=1000&firstResult="+str(i*100))
        r = requests.get('https://wso2-gw.ua.pt/primecore_primecore-ws/1.0.0/AccessPoint?maxResult=1000&firstResult='+str(i*100), headers={'Authorization': token})
        acess_points = json.loads(r.text)
        for ap in acess_points["accessPoints"]:
            print(ap["name"])
            try:
                if ap["name"].find("deti") != -1:
                    ap_num = int(ap["name"][-2:])
                    highest_aps["deti"] = ap_num if ap_num > highest_aps["deti"] else highest_aps["deti"]
                    print(ap)

                if ap["name"].find("biblioteca") != -1:
                    ap_num = int(ap["name"][-2:])
                    highest_aps["biblio"] = ap_num if ap_num > highest_aps["biblio"] else highest_aps["biblio"]

                if ap["name"].find("aauav") != -1:
                    ap_num = int(ap["name"][-2:])
                    highest_aps["aauav"] = ap_num if ap_num > highest_aps["aauav"] else highest_aps["aauav"]

                if ap["name"].find("deca") != -1:
                    ap_num = int(ap["name"][-2:])
                    highest_aps["deca"] = ap_num if ap_num > highest_aps["deca"] else highest_aps["deca"]

                if ap["name"].find("dbio") != -1:
                    ap_num = int(ap["name"][-2:])
                    highest_aps["dbio"] = ap_num if ap_num > highest_aps["dbio"] else highest_aps["dbio"]

                if ap["name"].find("dmat") != -1:
                    ap_num = int(ap["name"][-2:])
                    highest_aps["dmat"] = ap_num if ap_num > highest_aps["dmat"] else highest_aps["dmat"]

                if ap["name"].find("decivil") != -1:
                    ap_num = int(ap["name"][-2:])
                    highest_aps["decivil"] = ap_num if ap_num > highest_aps["decivil"] else highest_aps["decivil"]

                if ap["name"].find("fis") != -1:
                    ap_num = int(ap["name"][-2:])
                    highest_aps["fis"] = ap_num if ap_num > highest_aps["fis"] else highest_aps["fis"]

                if ap["name"].find("dem") != -1:
                    ap_num = int(ap["name"][-2:])
                    highest_aps["dem"] = ap_num if ap_num > highest_aps["dem"] else highest_aps["dem"]

                if ap["name"].find("geo") != -1:
                    ap_num = int(ap["name"][-2:])
                    highest_aps["geo"] = ap_num if ap_num > highest_aps["geo"] else highest_aps["geo"]

                if ap["name"].find("cpct") != -1:
                    ap_num = int(ap["name"][-2:])
                    highest_aps["cpct"] = ap_num if ap_num > highest_aps["cpct"] else highest_aps["cpct"]

                if ap["name"].find("dcspt") != -1:
                    ap_num = int(ap["name"][-2:])
                    highest_aps["dcspt"] = ap_num if ap_num > highest_aps["dcspt"] else highest_aps["dcspt"]

                if ap["name"].find("essua") != -1:
                    ap_num = int(ap["name"][-2:])
                    highest_aps["essua"] = ap_num if ap_num > highest_aps["essua"] else highest_aps["essua"]

                if ap["name"].find("cicfano") != -1:
                    ap_num = int(ap["name"][-2:])
                    highest_aps["cicfano"] = ap_num if ap_num > highest_aps["cicfano"] else highest_aps["cicfano"]

                if ap["name"].find("degeit") != -1:
                    ap_num = int(ap["name"][-2:])
                    highest_aps["degeit"] = ap_num if ap_num > highest_aps["degeit"] else highest_aps["degeit"]

                if ap["name"].find("dq") != -1:
                    ap_num = int(ap["name"][-2:])
                    highest_aps["dq"] = ap_num if ap_num > highest_aps["dq"] else highest_aps["dq"]

                if ap["name"].find("it") != -1:
                    ap_num = int(ap["name"][-2:])
                    highest_aps["it"] = ap_num if ap_num > highest_aps["it"] else highest_aps["it"]

                if ap["name"].find("dao") != -1:
                    ap_num = int(ap["name"][-2:])
                    highest_aps["dao"] = ap_num if ap_num > highest_aps["dao"] else highest_aps["dao"]

                if ap["name"].find("dep") != -1:
                    ap_num = int(ap["name"][-2:])
                    highest_aps["dep"] = ap_num if ap_num > highest_aps["dep"] else highest_aps["dep"]

                if ap["name"].find("dlc") != -1:
                    ap_num = int(ap["name"][-2:])
                    highest_aps["dlc"] = ap_num if ap_num > highest_aps["dlc"] else highest_aps["dlc"]

                if ap["name"].find("isca") != -1:
                    ap_num = int(ap["name"][-2:])
                    highest_aps["isca"] = ap_num if ap_num > highest_aps["isca"] else highest_aps["isca"]

                if ap["name"].find("ietta") != -1:
                    ap_num = int(ap["name"][-2:])
                    highest_aps["ietta"] = ap_num if ap_num > highest_aps["ietta"] else highest_aps["ietta"]
            except Exception:
                print("ap name not string")
                print("-->" + ap["name"])

    print(highest_aps)

    # lista de departamentos e máximo ap:
    # deti-ap23
    # biblioteca-ap26
    # aauav-ap07
    # deca-ap19
    # dbio-ap26
    # dmat
    # decivil
    # fis
    # dem
    # geo
    # cpct
    # dcspt
    # essua
    # cicfano
    # degeit
    # dq
    # dao
    # it
    # dep
    # dlc
    # isca
    # ietta

    # máximo_ap
    # {'deti': 23, 'biblio': 26, 'aauav': 7, 'dbio': 26, 'deca': 19, 'dmat': 26,
    #  'decivil': 8, 'fis': 16, 'dem': 20, 'geo': 19, 'cpct': 22, 'dcspt': 14,
    #  'essua': 30, 'cicfano': 11, 'degeit': 21, 'dq': 24, 'it': 21, 'dao': 17, 
    #  'dep': 19, 'dlc': 15, 'isca': 16, 'ietta': 0}

def main():
    explore_access_points()
    



main()