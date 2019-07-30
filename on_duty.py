import fire
from datetime import date
from enums import DutyPeriod
from operation import DBOperation
from execute import *

def init(month):
    init_origin_duty_data(month)
    
def shift(date_str, member_name, duty_period_str='晚班'):
    duty_date = parse_date_str(date_str)
    duty_period = parse_period_str(duty_period_str)
    member = parse_member_name(member_name)
    shift_duty(duty_date, duty_period, member)  
    
def parse_date_str(date_str):
    if len(date_str.split('/')) == 3:
        date_str_list = date_str.split('/')
    elif len(date_str.split('-')) == 3:
        date_str_list = date_str.split('-')
    else:
        return 
    return date(*[int(numstr) for numstr in date_str_list])
    
def parse_period_str(period_str):
    if period_str == "白班":
        return DutyPeriod.DayDuty
    elif period_str == "晚班":
        return DutyPeriod.NightDuty
    else:
        return 

def parse_member_name(member_name):
    return DBOperation.getMemberByName(member_name)


if __name__ == '__main__':
    fire.Fire()
    
    
    
    