from datetime import datetime


def ts_from_dt(dt):
    """
    convert datetime to timestamp
    :param dt:
    :return:
    """
    ts = datetime.timestamp(dt)
    return ts


def dt_from_ts(ts):
    """
    convert timestamp to datetime
    :param ts:
    :return:
    """
    dt = datetime.fromtimestamp(ts)
    return dt
