from sqlalchemy import or_, and_, not_
from db import *
from datetime import date

class DBOperation:
    
    @staticmethod
    def getMemberById(member_id):
        session = Session()
        try:
            return session.query(Member).filter(Member.member_id == member_id).first()
        except Exception as e:
            print(e)
        finally:
            session.close()
            
    @staticmethod
    def hasInitDutyData(month, year=2019):
        session = Session()
        try:
            #print(d.duty_date.year==2019)
            query = session.query(OriginDuty)
            for q in query:
                if q.duty_date.year == year and q.duty_date.month == month:
                    return True
            else:
                return False   
        except Exception as e:
            print(e)
        finally:
            session.close()
    
    @staticmethod
    def shiftDuty(duty_date, duty_period, member):
        session = Session()
        try:
            shift_duty = ShiftDuty(duty_date, duty_period, member.member_id)
            duty = session.query(OriginDuty).filter(and_(OriginDuty.duty_date==duty_date,
                                                         OriginDuty.duty_period==duty_period.value)).first()
            if duty is not None:
                print(duty)
                if duty.shift_duty_id is None:
                    shift_duty.previous_shift_duty_id = duty.duty_id
                    duty.shift_duty_id = shift_duty.shift_duty_id
                    session.add(shift_duty)
                    session.commit()
                else:
                    print(duty.member)
                    shift_id = duty.shift_duty_id
                    while shift_id is not None:
                        pre_shift_duty = session.query(ShiftDuty).filter(ShiftDuty.shift_duty_id==shift_id).first()
                        shift_id = pre_shift_duty.next_shift_duty_id
                    pre_shift_duty.next_shift_duty_id = shift_duty.shift_duty_id
                    shift_duty.previous_shift_duty_id = pre_shift_duty.shift_duty_id
                    session.add(shift_duty)
                    session.commit()
               
        except Exception as e:
            print(e)
            session.rollback()
        finally:
            session.close()
    
    
    
    
if __name__ == '__main__':
    duty_date = date(2019, 4, 1)
    member = DBOperation.getMemberById(8003)
    DBOperation.shiftDuty(duty_date, DutyPeriod.NightDuty, member)
    #print(DBOperation.hasInitDutyData(4, 2020))





