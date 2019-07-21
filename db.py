from sqlalchemy import Column, Integer, String, Date
from sqlalchemy import ForeignKey
from sqlalchemy.orm import relationship, backref
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine
from uuid import uuid4
from enums import DutyPeriod

Base = declarative_base()
engine = create_engine("sqlite:///db/OnDuty.sqlite", echo=True)

class Member(Base):
    __tablename__ = 'member'
    __table_args__ = {'extend_existing' : True}
    
    member_id = Column(Integer(), primary_key=True)
    name = Column(String(), nullable=False, unique=True)
    team = Column(String())
    
    def __init__(self, member_id, name, team='Application Team'):
        self.member_id = member_id
        self.name = name
        self.team = team
        
    def __eq__(self, other_member):
        return self.member_id == other_member.member_id or self.name == other_member.name
        
    def __repr__(self):
        return "id : {}, name : {}".format(self.member_id, self.name)

class OriginDuty(Base):
    __tablename__ = 'origin_duty'
    __table_args__ = {'extend_existing' : True}
    
    duty_id = Column(String(32), primary_key=True, default=uuid4().hex)
    duty_date = Column(Date(), nullable=False)
    duty_period = Column(Integer(), nullable=False)
    member_id = Column(Integer(), ForeignKey('member.member_id'))
    shift_duty_id = Column(String(32))
    
    member = relationship('Member', backref=backref('origin_duty', order_by=duty_id))  #a many-to-one relationship
    
    def __init__(self, duty_date, duty_period, member_id):
        self.duty_id = uuid4().hex
        self.duty_date = duty_date
        self.duty_period = duty_period.value
        self.member_id = member_id
        
    def __repr__(self):
        return "origin duty : {}\t{}\t{}".format(self.member.name,
                                                 self.duty_date.isoformat(),
                                                 DutyPeriod(self.duty_period).name)
                                                 
        
    
class ShiftDuty(Base):
    __tablename__ = 'shift_duty'
    __table_args__ = {'extend_existing' : True}
    
    shift_duty_id = Column(String(32), primary_key=True, default=uuid4().hex)
    shift_duty_date = Column(Date(), nullable=False)
    shift_duty_period = Column(Integer(), nullable=False)
    shift_member_id = Column(Integer(), ForeignKey('member.member_id'))
    previous_shift_duty_id = Column(String(32), nullable=False)
    next_shift_duty_id = Column(String(32))
    
    shift_member = relationship('Member', backref=backref('shift_duty', order_by=shift_duty_id))
    
    def __init__(self, shift_duty_date, shift_duty_period, shift_member_id, previous_shift_duty_id=None, next_shift_duty_id=None):
        self.shift_duty_id = uuid4().hex
        self.shift_duty_date = shift_duty_date
        self.shift_duty_period = shift_duty_period.value
        self.shift_member_id = shift_member_id
        self.previous_shift_duty_id = previous_shift_duty_id
        self.next_shift_duty_id = next_shift_duty_id
        
    def __repr__(self):
        return "shift duty : {}\t{}\t{}".format(self.shift_member.name,
                                                self.shift_duty_date.isoformat(),
                                                DutyPeriod(self.shift_duty_period).name)
        
    
    
Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)


#if __name__ == '__main__':
#    Base.metadata.create_all(engine)
    
    
    
    
    
    
    
    
    
    
    
    
