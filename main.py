import datetime as dt
from os import getenv
from pprint import pprint as print

import requests
from bs4 import BeautifulSoup as bs
from dotenv import load_dotenv

load_dotenv()

wilma_url = "https://yvkoulut.inschool.fi"

username = getenv("username")
password = getenv("password")

date = "1.11.2020"


class Lesson:
    def __init__(self, json: dict):
        # parse the date and time and make them datetime objects
        date = [int(d) for d in json["DateArray"][0].split("-")]
        start_time = [int(d) for d in json["Start"].split(":")]
        end_time = [int(d) for d in json["End"].split(":")]
        self.day = json["Day"]
        self.date = dt.date(*date)
        self.start = dt.datetime(*date, *start_time)
        self.end = dt.datetime(*date, *end_time)

        # parse the other useful information
        group = json["Groups"][0]
        self.name = group["Caption"]
        self.long_name = group["FullCaption"]
        self.groups = group["Class"]
        self.room = group["Rooms"][0]["Caption"]
        self.teacher_id = group["Teachers"][0]["Caption"]
        self.teacher_name = group["Teachers"][0]["LongCaption"]


class Schedule:
    def __init__(self, json: list):
        # make every lesson an instance and add it to the list
        self.lessons = []
        for l in json:
            lesson = Lesson(l)
            self.lessons.append(lesson)

    def next_lesson(self, add_days: int = 0):
        # add optional day shift
        date_today = dt.date.today()+dt.timedelta(days=add_days)

        # return mondays first lesson if weekend
        if add_days == 0:
            weekday = dt.date.weekday(date_today)
            if weekday == 5 or weekday == 6:
                for lesson in self.lessons:
                    if lesson.date == date_today + dt.timedelta(days=(7-weekday)):
                        return lesson

        # get todays lessons
        today = []
        for lesson in self.lessons:
            if lesson.date == date_today:
                today.append(lesson)

        # if no lessons, return empty list
        if today == []:
            return []

        # return the next lesson that hasn't yet begun
        for lesson in today:
            if lesson.start > dt.datetime.now():
                return lesson

        # if there are no lessons left, return False
        return False


def fetch():
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
        data = {
            "date": date,
            "getfullmonth": True,
            "formkey": token,
        }
        o = r.post(f'{wilma_url}/overview', data=data)

        # parse the schedule section of the json response
        schedule_json = o.json()["Schedule"]

    # create Schedule instance
    schedule = Schedule(schedule_json)

    # print test output
    next_lesson = schedule.next_lesson()
    print(
        f'The next lesson ({next_lesson.name}), which is also called "{next_lesson.long_name}", starts at {next_lesson.start.strftime("%H:%M")}. It is held in class "{next_lesson.room}". The teacher ({next_lesson.teacher_id}) is called {next_lesson.teacher_name}. The lesson ends at {next_lesson.end.strftime("%H:%M")}.')


if __name__ == "__main__":
    fetch()
