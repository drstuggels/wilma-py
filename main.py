import requests
from bs4 import BeautifulSoup as bs
from pprint import pprint as print
from dotenv import load_dotenv
from os import getenv

load_dotenv()

wilma_url = "https://yvkoulut.inschool.fi"

username = getenv("username")
password = getenv("password")

date = "1.11.2020"

with requests.Session() as r:
    g = r.get(wilma_url)

    soup = bs(g.text, 'html.parser')
    token = soup.select_one('input[name=SESSIONID]').get('value')

    data = {
        "Login": username,
        "Password": password,
        "SESSIONID": token,
    }
    p = r.post(f'{wilma_url}/login', data=data)

    g = r.get(wilma_url)
    soup = bs(g.text, 'html.parser')
    token = soup.select_one('input[name=formkey]').get('value')

    data = {
        "date": date,
        "getfullmonth": True,
        "formkey": token,
    }
    o = r.post(f'{wilma_url}/overview', data=data)

    schedule = o.json()["Schedule"]
    # Exams?

    classes = []
    for s in schedule:
        group = s["Groups"][0]
        next_class = {
            "day": s["Day"],
            "start": s["Start"],
            "end": s["End"],
            "name": group["Caption"],
            "long_name": group["FullCaption"],
            "classes": group["Class"],
            "room": group["Rooms"][0]["Caption"],
            "teacher_id": group["Teachers"][0]["Caption"],
            "teacher_name": group["Teachers"][0]["LongCaption"],
        }
        classes.append(next_class)

    print(classes)
