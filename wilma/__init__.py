import requests
from bs4 import BeautifulSoup as bs

from wilma.classes import Lesson, Schedule


def format_alfred(dikt: dict):
    print("heylllo", dikt)
    items = []
    for d in dikt:
        item = {
            "title": d,
            "subtitle": dikt[d],
            "type": "default",
        }
        items.append(item)

    return items


def fetch(wilma_url: str, username: str, password: str):
    with requests.Session() as r:
        # get the front page to get SESSIONID needed for login
        g = r.get(wilma_url)
        soup = bs(g.text, 'html.parser')
        token = soup.select_one('input[name=SESSIONID]').get('value')

        # create the payload and make the post request
        data = {
            "Login": username,
            "Password": password,
            "SESSIONID": token,
        }
        r.post(f'{wilma_url}/login', data=data)

        # get the front page to get formkey needed for api request
        g = r.get(wilma_url)
        soup = bs(g.text, 'html.parser')
        token = soup.select_one('input[name=formkey]').get('value')

        # create the payload and make the post request
        o = r.post(f'{wilma_url}/overview', data={"formkey": token})

        # parse the schedule section of the json response
        schedule_json = o.json()["Schedule"]

    # create Schedule instance
    schedule = Schedule(schedule_json)

    # return the schedule object
    return schedule
