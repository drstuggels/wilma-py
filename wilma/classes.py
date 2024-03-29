import datetime as dt


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

    def to_dict(self):
        dikt = {
            "name": self.name,
            "long_name": self.long_name,
            "teacher_id": self.teacher_id,
            "teaher_name": self.teacher_name,
            "start": self.start.strftime("%d.%m.%Y %H:%M"),
            "end": self.end.strftime("%d.%m.%Y %H:%M"),
            "room": self.room,
            "groups": self.groups,
            "date": self.date.strftime("%d.%m.%Y"),
        }
        return dikt


class Schedule:
    def __init__(self, json: list):
        # make every lesson an instance and add it to the list
        self.lessons = []
        for l in json:
            lesson = Lesson(l)
            self.lessons.append(lesson)

    def next_lesson(self):
        # return the next lesson that hasn't yet begun
        for lesson in self.lessons:
            if lesson.start > dt.datetime.now():
                return lesson
