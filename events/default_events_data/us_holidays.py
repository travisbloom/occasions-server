from pendulum import Date
from .datetime_utils import *
get_us_holidays_initial_data = lambda: {
    'mlk_day': {
        'name': 'Martin Luther King, Jr. Day',
        'event_types': ['american', 'geopolitical'],
        'date_start': lambda year: get_nth_weekday_in_month(year, JANUARY, MON, 3)
    },
    'presidents_day': {
        'name': "President's Day",
        'event_types': ['american', 'geopolitical'],
        'date_start': lambda year: get_nth_weekday_in_month(year, FEBRUARY, MON, 3)
    },
    'mothers_day': {
        'name': "Mother's Day",
        'event_types': ['feminine', 'american', 'appreciation'],
        'date_start': lambda year: get_nth_weekday_in_month(year, MAY, SUN, 3)
    },
    'memorial_day': {
        'name': "Memorial Day",
        'event_types': ['military', 'american', 'geopolitical'],
        'date_start': lambda year: get_last_weekday_in_month(year, MAY, MON)
    },
    'fathers_day': {
        'name': "Father's Day",
        'event_types': ['masculine', 'american', 'appreciation'],
        'date_start': lambda year: get_nth_weekday_in_month(year, JUNE, SUN, 3)
    },
    'independence_day': {
        'name': 'Independence Day',
        'event_types': ['military', 'american', 'geopolitical'],
        'date_start': lambda year: Date.create(year, JULY, 4)
    },
    'labor_day': {
        'name': 'Labor Day',
        'event_types': ['american', 'geopolitical'],
        'date_start': lambda year: get_nth_weekday_in_month(year, SEPTEMBER, MON, 1)
    },
    'veterans_day': {
        'name': 'Veterans Day',
        'event_types': ['military', 'american', 'geopolitical'],
        'date_start': lambda year: Date.create(year, NOVEMBER, 11)
    },
    'thanksgiving': {
        'name': 'Thanksgiving',
        'event_types': ['food', 'american', 'geopolitical'],
        'date_start': lambda year: get_nth_weekday_in_month(year, NOVEMBER, THU, 4)
    }
}
