import os
import pandas as pd
import datetime
from db import *
from enums import *
from operation import *

           

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



if __name__ == '__main__':
    init_origin_duty_data(4)
#    mdf = pd.read_csv('data/application_team_data.csv')
#    print(mdf)
#    insert_members()
    
    