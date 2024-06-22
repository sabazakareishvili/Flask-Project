import datetime

def timechanger(time):
    dt_object = datetime.datetime.fromtimestamp(time)
    formatted_date = dt_object.strftime('%Y-%m-%d %H:%M:%S')
    return formatted_date