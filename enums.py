from enum import Enum, unique

@unique
class DutyPeriod(Enum):
    DayDuty = 1
    NightDuty = 2
    
@unique
class Month(Enum):
    Jan = 1
    Feb = 2
    Mar = 3
    Apr = 4
    May = 5
    June = 6
    July = 7
    Aug = 8
    Sept = 9
    Oct = 10
    Nov = 11
    Dec = 12
    
    
if __name__ == '__main__':
    dp1 = DutyPeriod.DayDuty
    print(dp1.name, dp1.value)
    dp2 = DutyPeriod(2)
    print(dp2.name, dp2.value)
    print(DutyPeriod.NightDuty.value)
    
