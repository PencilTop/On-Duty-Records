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
        try:
            odf = pd.read_csv(table_path).fillna('')
        except Exception as e:
            print(e)
            sys.exit("data file {} read failed.".format(table_name))
        session = Session()
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
        sys.exit("origin duty data of {} has already init.".format(Month(month).name))


def shift_duty(duty_date, duty_period, member):
    if duty_date is None or duty_period is None or member is None:
        sys.exit("shift duty message is not right, please check.")
    shift_chain = DBOperation.getDutyShiftChain(duty_date, duty_period)
    if shift_chain is not None and shift_chain.getOnDutyMember() != member:
        DBOperation.shiftDuty(duty_date, duty_period, member)
    else:
        sys.exit("can not find duty shift-chain or the on-duty member is the shift member.")
    print('shift duty executed successfully.')
    
def select_duty_record(duty_date, duty_period):
    return DBOperation.getDutyShiftChain(duty_date, duty_period)
    

        
        
    
        


if __name__ == '__main__':
    insert_members()
    #init_origin_duty_data(4)
    #shift_duty('2019-4-4', '晚班', '李会')
    
#    mdf = pd.read_csv('data/application_team_data.csv')
#    print(mdf)
#    insert_members()
    
    