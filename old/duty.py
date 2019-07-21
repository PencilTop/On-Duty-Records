#################################################################
#Author : Guanghui Hu
#Title : for on-duty records of the application team of pufa bank
#Date : 2019-7-6
#################################################################
import datetime
from old.staff import GroupMember
from enums import DutyPeriod

class DutyShift:
    def __init__(self, member):
        assert isinstance(member, GroupMember)
        self.__members_list = [member, ]
    
    def getMemberList(self):
        return self.__members_list
    
    def getOnDutyMember(self):
        return self.__members_list[-1]

    def shiftDuty(self, member):
        assert isinstance(member, GroupMember)
        on_duty = self.getOnDutyMember()
        if on_duty == member:
            print("shift duty failed for group member : {}".format(member.getName()))
        else:
            self.__members_list.append(member)
    
    def __repr__(self):
        return '->'.join([m.getName() for m in self.__members_list])
        

class Duty:
    def __init__(self, date, duty_period, duty_shift):
        self.__date = date
        self.__duty_period = duty_period
        self.__duty_shift = duty_shift
        
    def getDutyDate(self):
        return self.__date
    
    def getDutyPeriod(self):
        return self.__duty_period
    
    def getDutyShift(self):
        return self.__duty_shift
    
    def shiftDuty(self, member):
        self.__duty_shift.shiftDuty(member)
        
    def __repr__(self):
        return '\t'.join([self.__date.isoformat(), self.__duty_period.name, repr(self.__duty_shift)])
        
        

if __name__ == '__main__':
    m1 = GroupMember(8001, '张佳玮')
    m2 = GroupMember(8002, '贺春玮')
    m3 = GroupMember(8003, '李文明')
    m4 = GroupMember(8004, '许学成')
    
    duty_shift = DutyShift(m1)
    duty = Duty(datetime.date.today(), DutyPeriod.DayDuty, duty_shift)
    print(duty)
    duty.shiftDuty(m2)
    duty.shiftDuty(m3)
    print(duty)
    duty.shiftDuty(m4)









        
        
        
        
        