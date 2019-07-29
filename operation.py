from sqlalchemy import or_, and_, not_
from sqlalchemy.orm import joinedload
from db import Member,OriginDuty, ShiftDuty, Session
from enums import DutyPeriod, Month 
from datetime import date

class DutyShiftChain:
    def __init__(self, origin_duty):
        self.shift_chain = [origin_duty, ]
        
    def addDutyShiftRecord(self, shift_duty):
        self.shift_chain.append(shift_duty)
        
    def getShiftMemberList(self):
        return [ duty.member for duty in self.shift_chain ]
    
    def getOnDutyMember(self):
        return self.getShiftMemberList()[-1]
    
    def __repr__(self):
        return "->".join([member.name for member in self.getShiftMemberList()])

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
    def getMemberByName(member_name):
        session = Session()
        try:
            return session.query(Member).filter(Member.name == member_name).first()
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
                if duty.shift_duty_id is None:
                    shift_duty.previous_shift_duty_id = duty.duty_id
                    duty.shift_duty_id = shift_duty.shift_duty_id
                    session.add(shift_duty)
                    session.commit()
                else:
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
            
    @staticmethod
    def getDutyShiftChain(duty_date, duty_period):
        session = Session()
        try:
            origin_duty = session.query(OriginDuty).options(joinedload('member')).filter(and_(OriginDuty.duty_date==duty_date,
                                                         OriginDuty.duty_period==duty_period.value)).first()
            #print(origin_duty)
            if origin_duty is not None:
                shift_chain = DutyShiftChain(origin_duty)
                if origin_duty.shift_duty_id is None:
                    return shift_chain
                else:
                    shift_id = origin_duty.shift_duty_id
                    while shift_id is not None:
                        shift_duty = session.query(ShiftDuty).options(joinedload('member')).filter(ShiftDuty.shift_duty_id==shift_id).first()
                        #print(shift_duty)
                        shift_chain.addDutyShiftRecord(shift_duty)
                        shift_id = shift_duty.next_shift_duty_id
                    return shift_chain
        except Exception as e:
                print(e)
                session.rollback()
        finally:
            session.close()                                                                      
        
    
    @staticmethod
    def getAllShiftList(month):
        pass
    
    @staticmethod
    def deleteShiftDutyRecord(shift_duty_date, shift_duty_period=DutyPeriod.NightDuty):
        session = Session()
        duty_shift_chain = DBOperation.getDutyShiftChain(shift_duty_date, shift_duty_period)
        if duty_shift_chain is None:
            print("无日期为{}的值班记录".format(shift_duty_date))
            return
        shift_chain_list = duty_shift_chain.shift_chain
        shift_count = len(shift_chain_list) - 1
        try:
            if shift_count == 0:
                print("can not delete origin duty.")
                return 
            elif shift_count == 1:
                session.query(OriginDuty).filter(OriginDuty==shift_chain_list[-2]).update({OriginDuty.shift_duty_id : None})
            else:
                session.query(ShiftDuty).filter(ShiftDuty==shift_chain_list[-2]).update({ShiftDuty.next_shift_duty_id : None})
            session.delete(shift_chain_list[-1])
            session.commit()     
        except Exception as e:
                print(e)
                session.rollback()
        finally:
            session.close()          
    
    @staticmethod
    def getShiftRecord(member):
        pass
    
    @staticmethod
    def undoShift(duty_date, duty_period, member=None):
        pass
            
    
    
    
    
    
if __name__ == '__main__':
    duty_date = date(2019, 4, 2)
    DBOperation.deleteShiftDutyRecord(duty_date)
    #member = DBOperation.getMemberById(8023)
    #DBOperation.shiftDuty(duty_date, DutyPeriod.NightDuty, member)
    print(DBOperation.getDutyShiftChain(duty_date, DutyPeriod.NightDuty))
    """
    
    
    
    #print(DBOperation.hasInitDutyData(4, 2020))
    """





