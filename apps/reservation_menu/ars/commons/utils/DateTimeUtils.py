import datetime

class DateTimeUtils(object):

    @classmethod
    def get_now(cls):
        return datetime.datetime.now()

    @classmethod
    def format(cls, datetime):

        datetime_format = "%Y-%m-%d %H:%M:%S"

        return datetime.strftime(datetime_format)
