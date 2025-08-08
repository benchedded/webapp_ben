class Module:
    count_id = 0
    def __init__(self, module_type, module_num):
        Module.count_id += 1
        self.__module_assign_id = Module.count_id
        self.__module_type = module_type
        self.__module_num = module_num
    
    def get_module_assign_id(self):
        return self.__module_assign_id
    def get_module_type(self):
        return self.__module_type
    def get_module_num(self):
        return self.__module_num
    

    def set_module_type(self, module_type):
        self.__module_type = module_type
    def set_module_num(self, module_num):
        self.__module_num = module_num
    def set_module_assign_id(self, module_assign_id):
        self.__module_assign_id = module_assign_id

        