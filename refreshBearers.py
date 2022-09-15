import time
import requests
import re
from termcolor import colored
import getSessionCookie

def main(session):
    f = open("data/userlist.txt", "r")
    lines = f.readlines()
    users = []
    passwords = []
    for line in lines:
        line = line.strip()
        line = line.split(":")
        users.append(line[0])
        passwords.append(line[1])
    f.close()
    
    bearersFile = open("data/bearers.txt", "r")
    lines = bearersFile.readlines()
    bearers = []
    secsInHour = 3600
    for i,line in enumerate(lines):
        line = line.strip()
        lineArr = line.split(":")
        if(len(lineArr) == 3 and lineArr[0] in users and time.time() - float(lineArr[-1]) < secsInHour):
            bearers.append(line)
            index = users.index(lineArr[0])
            users[index] = ""
            passwords[index] = ""
    bearersFile.close()
    
    for i,user in enumerate(users):
        if(user == ""):
            continue
        print(colored("[-] Getting bearer token for "+user, "yellow"))
        reSessionCookie = getSessionCookie.getSessionCookie(user, passwords[i], session)
    
        url = "https://www.reddit.com"
        cookies = {'reddit_session': reSessionCookie}
        r = session.get(url, cookies=cookies)
        
        text = r.text.encode('utf-8')
        bearerToken = re.findall(b'"accessToken":"(.*?)"', text)
        bearerToken = bearerToken[0].decode()
          
        bearers.append(user+":"+bearerToken+":"+str(time.time()))
    
    with open('../data/bearers.txt', 'w') as f:
        for i,bearer in enumerate(bearers):
            f.write(bearer+"\n")

if __name__ == "__main__":
    main()
