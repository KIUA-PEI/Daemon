

def somefuncA(a, b, bool):
    print("on somefuncA: ")
    print("bolb value:" + str(bool))
    if "boolx" in globals():
        print("bolbx value:" + str(boolx))
    else:
        print("variable boolx dont exists")

def somefuncB(bool):
    print("on somefuncB: ")
    print("changed from True to False")
    global boolx
    bool = False
    boolx = bool
    



def main():
    boolb = True

    somefuncA("2", "4", boolb)

    somefuncB(boolb)

    somefuncA("2", "4", boolb)

main()

