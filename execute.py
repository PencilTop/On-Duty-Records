import os, sys
import pandas as pd
import datetime
from db import Member, OriginDuty, ShiftDuty, Session
from enums import DutyPeriod, Month
from operation import DBOperation

           

def insert_members():
    session = Session()
    mdf = pd.read_csv('data/application_team_data.csv')
    try:
        for i in mdf.index:
            member = Member(int(mdf['ID'][i]), mdf['Name'][i])
            session.add(member)
        session.commit()
    except Exception as e:
        print(e)
        session.rollback()
    finally:
        session.close()
        
def init_origin_duty_data(month):
    if not DBOperation.hasInitDutyData(month):
        table_name = Month(month).name + "_origin_on_duty.csv"
        table_path = os.path.join('data', table_name)
        session = Session()
        odf = pd.read_csv(table_path).fillna('')
        try:
            for i in odf.index:
                if odf['DayDutyID'][i] == '':
                    datenum = [int(p) for p in odf['Date'][i].split('/')]
                    duty_date = datetime.date(*datenum)
                    member = DBOperation.getMemberById(int(odf['NightDutyID'][i]))           
                    duty = OriginDuty(duty_date, DutyPeriod.NightDuty, member.member_id)
                    session.add(duty)
                else:
                    datenum = [int(p) for p in odf['Date'][i].split('/')]
                    duty_date = datetime.date(*datenum)
                    day_member = DBOperation.getMemberById(int(odf['DayDutyID'][i])) 
                    night_member = DBOperation.getMemberById(int(odf['NightDutyID'][i])) 
                    duty_day = OriginDuty(duty_date, DutyPeriod.DayDuty, day_member.member_id)
                    duty_night = OriginDuty(duty_date, DutyPeriod.NightDuty, night_member.member_id)
                    session.add(duty_day)
                    session.add(duty_night)
            session.commit()       
        except Exception as e:
            print(e)
            session.rollback()
        finally:
            session.close()
    else:
        print("origin duty data of {} has been init.".format(Month(month).name))


def shift_duty(duty_date_str, duty_period_str, member_name):
    if len(duty_date_str.split('/')) == 3:
        date_list = duty_date_str.split('/')
    elif len(duty_date_str.split('-')) == 3:
        date_list = duty_date_str.split('/')
    else:
        sys.exit("Unkown date format string.")
    date_str = date_list[0] + date_list[1].zfill(2) + date_list[2].zfill(2)
    duty_date = datetime.date.fromisoformat(date_str)
    if duty_period_str == "白班":
        duty_period = DutyPeriod.DayDuty
    elif duty_period_str == "晚班":
        duty_period = DutyPeriod.NightDuty
    member = DBOperation.getMemberByName(member_name)
    if member is None:
        sys.exit("can't find {} in application team.".format(member_name))
        
    
        


if __name__ == '__main__':
    insert_members()
    init_origin_duty_data(4)
    
#    mdf = pd.read_csv('data/application_team_data.csv')
#    print(mdf)
#    insert_members()
    
    