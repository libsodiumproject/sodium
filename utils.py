import datetime as dt
from datetime import datetime

def seconds(seconds):
    return int((datetime.now() + dt.timedelta(seconds=seconds) - datetime(1970, 1, 1)).total_seconds())

