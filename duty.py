#################################################################
#Author : Guanghui Hu
#Title : for on-duty records of the application team of pufa bank
#Date : 2019-7-6
#################################################################
import datetime
from staff import GroupMember

class DutyShiftList:
    def __init__(self, member):
        assert isinstance(member, GroupMember)
        self.__members_list = [member, ]
    
    def getMembers(self):
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
        

class Duty:
    def __init__(self, date, duty_period, duty_shift_list):
        self.date = date
        self.duty_period = duty_period
        self.duty_stack = duty_shift_list
        
        

if __name__ == '__main__':
    pass









        
        
        
        
        