from datetime import datetime


def str_to_datetime(raw) -> datetime:
    # Raw is like this '2022-07-25 00:00:00'
    #                   0123456789012345678
    # This should work but fails with this output: '1900-01-01 00:00:00'
    # self.date_obj.strptime(raw, "%Y-%m-%d %H:%M:%S")
    # So we do this the hard way...
    year_str = raw[0:4]
    month_str = int(raw[5:7])
    day_str = int(raw[8:10])
    hour_str = raw[11:13]
    minute_str = raw[14:16]
    second_str = raw[17:]
    # print("strs: y '{}', m '{}', d '{}'".format(year_str, month_str, day_str))
    # print("strs: h '{}', m '{}', s '{}'".format(hour_str, minute_str, second_str))
    if year_str:
        year = int(year_str)
    else:
        year = 0
    year_str = raw[0:4]
    if month_str:
        month = int(month_str)
    else:
        month = 0
    year_str = raw[0:4]
    if day_str:
        day = int(day_str)
    else:
        day = 0
    if hour_str:
        hour = int(hour_str)
    else:
        hour = 0
    if minute_str:
        minute = int(minute_str)
    else:
        minute = 0
    if second_str:
        second = int(second_str)
    else:
        second = 0
    return datetime(year, month, day, hour=hour, minute=minute, second=second)
