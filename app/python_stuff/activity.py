class Activity:
    count_id = 0

    def __init__(self, name, time, reps, instructions):
        Activity.count_id += 1
        self.__activity_id = Activity.count_id
        self.__name = name
        self.__time = time
        self.__reps = reps
        self.__instructions = instructions

    def get_activity_id(self): return self.__activity_id
    def get_name(self): return self.__name
    def get_time(self): return self.__time
    def get_reps(self): return self.__reps
    def get_instructions(self): return self.__instructions

    def set_name(self, name): self.__name = name
    def set_time(self, time): self.__time = time
    def set_reps(self, reps): self.__reps = reps
    def set_instructions(self, instructions): self.__instructions = instructions

