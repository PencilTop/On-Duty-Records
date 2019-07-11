#################################################################
#Author : Guanghui Hu
#Title : for on-duty records of the application team of pufa bank
#Date : 2019-7-6
#################################################################

class GroupMember:
    def __init__(self, id, name):
        self.__name = name
        self.__id = id
    
    def getName(self):
        return self.__name
    
    def getId(self):
        return self.__id
    
    def __repr__(self):
        return "id : {}  name : {}".format(self.getId(), self.getName())
    
class ApplicationTeam:
    def __init__(self, teamName, members=None):
        self.__teamName = teamName
        if members is None:
            self.__members = []
        else:
            self.__members = list(members)
            
    def getTeamName(self):
        return self.__teamName
        
    def getMembers(self):
        return self.__members
    
    def addMember(self, member):
        if member.getId() not in [ member.getId() for member in self.__members ]:
            self.__members.append(member)
        else:
            print("dulplicated member id , {} \nadd member failed".format(member))
    
    def addMembers(self, members):
        for member in members:
            self.addMember(member)
    
    def __repr__(self):
        return "team name : {}\nmembers : {}".format(self.__teamName,
                                                     ' '.join([ member.getName() for member in self.__members ]))
        
        
if __name__ == '__main__':
    g1 = GroupMember(8001, '张佳伟')
    print(g1)
    g2 = GroupMember(8002, '贺春玮')
    print(g2)
    g3 = GroupMember(8001, '李文明')
    print(g3)
    t1 = ApplicationTeam('应用组')
    t1.addMember(g1)
    t1.addMember(g2)
    t1.addMember(g3)
    print(t1)
    
    
    
    
    
    
    
    
    
    