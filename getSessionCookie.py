import requests
import re

def getSessionCookie(username, password, session):
    session.cookies.clear()
    r = session.get("https://www.reddit.com/login/")
    
    response = r.text.encode('utf-8')
    sessionCookie = session.cookies.get_dict()['session']
    
    crsfToken = re.findall(b'name="csrf_token" value="(.*?)"', response)
    crsfToken = crsfToken[0].decode()
    
    data = {"csrf_token": crsfToken, "username": username, "password": password} 
    r = session.post("https://www.reddit.com/login", data=data)
    return session.cookies.get_dict()['reddit_session']

