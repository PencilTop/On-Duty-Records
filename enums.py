from enum import Enum, unique

@unique
class DutyPeriod(Enum):
    DayDuty = 1
    NightDuty = 2
    
