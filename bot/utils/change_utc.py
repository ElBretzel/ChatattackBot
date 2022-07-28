from constants import TIMEZONE

def convert_timezone(dt):
    return dt.astimezone(TIMEZONE)