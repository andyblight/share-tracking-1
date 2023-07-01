from datetime import datetime


def str_to_datetime(raw) -> datetime:
    # Raw is like this '2022-07-25 00:00:00'
    #                   0123456789012345678
    # This should work but fails with this output: '1900-01-01 00:00:00'
    # self.date_obj.strptime(raw, "%Y-%m-%d %H:%M:%S")
    # So we do this the hard way...
    year = int(raw[0:4])
    month = int(raw[5:7])
    day = int(raw[8:10])
    hour = int(raw[11:13])
    minute = int(raw[14:16])
    second = int(raw[17:])
    return datetime(year, month, day, hour=hour, minute=minute, second=second)
