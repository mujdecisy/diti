from dateutil.relativedelta import relativedelta
from datetime import timedelta
from enum import Enum

class DitiRound(Enum):
    ROUND_DOWN = 0
    ROUND_UP = 1


class DitiParts(Enum):
    YEARS = 0
    MONTHS = 1
    WEEKS = 2
    DAYS = 3
    HOURS = 4
    MINUTES = 5
    SECONDS = 6
    MICROSECONDS = 7