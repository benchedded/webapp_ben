class Medication:
    count_id = 0

    def __init__(self, name, dosage, start_date, end_date, time_to_take, frequency, calendar_color, instructions):
        Medication.count_id += 1
        self.__medication_id = Medication.count_id
        self.__name = name
        self.__dosage = dosage
        self.__start_date = start_date
        self.__end_date = end_date
        self.__time_to_take = time_to_take
        self.__frequency = frequency
        self.__calendar_color = calendar_color
        self.__instructions = instructions

    def get_medication_id(self): return self.__medication_id
    def get_name(self): return self.__name
    def get_dosage(self): return self.__dosage
    def get_start_date(self): return self.__start_date
    def get_end_date(self): return self.__end_date
    def get_time_to_take(self): return self.__time_to_take
    def get_frequency(self): return self.__frequency
    def get_calendar_color(self): return self.__calendar_color
    def get_instructions(self): return self.__instructions