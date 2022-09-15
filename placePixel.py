import requests
import re
from termcolor import colored
import time
import refreshBearers
import sys

if(len(sys.argv) != 4):
    print("[*] Usage: placePixel.py x y stencil\n")
    exit(0)

baseX = int(sys.argv[1])
baseY = int(sys.argv[2])

print(colored("[-] Updaing bearer tokens, this may take a while...", "yellow"))
refreshBearers.main()
print(colored("[+] Bearer tokens updated!", "green"))


print(colored("[-] Checking to see if pixels can be placed yet", "yellow"))
f = open("data/lastPixel.txt")
data = f.read()
f.close()

secsIn5Min = 300
if(time.time() - float(data) < secsIn5Min):
    print(colored("[-] Pixels not ready, try again in "+str(secsIn5Min - (time.time() - float(data)))+" seconds", "red"))
    exit(0)
print(colored("[+] Pixels ready, launching attack!\n", "green"))

#Get bearers for all the users
f = open("data/bearers.txt", "r")
lines = f.readlines()
users = []
bearers = []
for line in lines:
    line = line.strip()
    line = line.split(":")
    users.append(line[0])
    bearers.append(line[1])
f.close()

#Get coords for all the users
f = open(sys.argv[3], "r")
coords = f.readlines()
f.close()

for i,coord in enumerate(coords):
    postUrl = "https://gql-realtime-2.reddit.com/query"
    headers = {'Authorization': 'Bearer '+bearers[i]}

    coord = coord.strip()
    coord = coord.split(",")
    addX = int(coord[0])
    addY = int(coord[1]) 
    colorIndex = int(coord[2])

    x = baseX + addX
    y = baseY + addY
    
    print(colored("[+] Placing pixel at "+str(x)+","+str(y)+" with color index "+str(colorIndex)+" as user "+users[i], "green"))
    
    canvasIndex = 0
    if(x > 999 and y <= 999):
        x = x-1000
        canvasIndex = 1
    elif(x <= 999 and y > 999):
        y = y-1000
        canvasIndex = 2
    elif(x > 999 and y > 999):
        x = x-1000
        y = y-1000
        canvasIndex = 3

    json = {"operationName":"setPixel","variables":{"input":{"actionName":"r/replace:set_pixel","PixelMessageData":{"coordinate":{"x":x,"y":y},"colorIndex":colorIndex,"canvasIndex":canvasIndex}}},"query":"mutation setPixel($input: ActInput!) {\n  act(input: $input) {\n    data {\n      ... on BasicMessage {\n        id\n        data {\n          ... on GetUserCooldownResponseMessageData {\n            nextAvailablePixelTimestamp\n            __typename\n          }\n          ... on SetPixelResponseMessageData {\n            timestamp\n            __typename\n          }\n          __typename\n        }\n        __typename\n      }\n      __typename\n    }\n    __typename\n  }\n}\n"}

    r = requests.post(postUrl, headers=headers, json=json)
    response = r.text.encode('utf-8')
    if not (b'nextAvailablePixelTimestamp' in response and b'"__typename":"BasicMessage"' in response and b'id' in response):
        print(colored("[-] Potential Error:" + str(r.text.encode('utf-8')), "red"))

f = open("data/lastPixel.txt", "w")
f.write(str(time.time()))
f.close()
