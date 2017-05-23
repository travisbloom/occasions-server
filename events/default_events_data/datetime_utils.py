from calendar import monthrange
from datetime import date, timedelta

MON, TUE, WED, THU, FRI, SAT, SUN = range(7)
_, JANUARY, FEBRUARY, MARCH, APRIL, MAY, JUNE, JULY, AUGUST, SEPTEMBER, OCTOBER, NOVEMBER, DECEMBER = range(13)


def get_nth_weekday_in_month(year, month, weekday, n=1, start=None):
    """Get the nth weekday in a given month. e.g:
    >>> # the 1st monday in Jan 2013
    >>> get_nth_weekday_in_month(2013, 1, MON)
    datetime.date(2013, 1, 7)
    >>> # The 2nd monday in Jan 2013
    >>> get_nth_weekday_in_month(2013, 1, MON, 2)
    datetime.date(2013, 1, 14)
    """
    day = date(year, month, 1)
    if start:
        day = start
    counter = 0
    while True:
        if day.month != month:
            # Don't forget to break if "n" is too big
            return None
        if day.weekday() == weekday:
            counter += 1
        if counter == n:
            break
        day = day + timedelta(days=1)
    return day


def get_last_weekday_in_month(year, month, weekday):
    """Get the last weekday in a given month. e.g:
    >>> # the last monday in Jan 2013
    >>> get_last_weekday_in_month(2013, 1, MON)
    datetime.date(2013, 1, 28)
    """
    day = date(year, month, monthrange(year, month)[1])
    while True:
        if day.weekday() == weekday:
            break
        day = day - timedelta(days=1)
    return day
