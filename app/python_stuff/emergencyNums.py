class EmergencyNums:
    count_id = 0
    def __init__(self, emergency_num, contact_name):
        EmergencyNums.count_id+=1 
        self.__num_id = EmergencyNums.count_id
        self.__emergency_num = emergency_num
        self.__contact_name = contact_name
    
    def get_num_id(self):
        return self.__num_id
    def get_emergency_num(self):
        return self.__emergency_num
    def get_contact_name(self):
        return self.__contact_name
    
    def set_emergency_num(self, emergency_num):
        self.__emergency_num = emergency_num
    def set_contact_name(self, contact_name ):
        self.__contact_name = contact_name


