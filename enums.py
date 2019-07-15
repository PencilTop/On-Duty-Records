from enum import Enum, unique

@unique
class DutyPeriod(Enum):
    DayDuty = 1
    NightDuty = 2
    
    
if __name__ == '__main__':
    dp1 = DutyPeriod.DayDuty
    print(dp1.name, dp1.value)
    
