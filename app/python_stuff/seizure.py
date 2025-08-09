class Seizure:
    count_id = 0

    def __init__(self, date, time, seizure_type, duration, severity, calendar_color, triggers, notes):
        Seizure.count_id += 1
        self.__seizure_id = Seizure.count_id
        self.__date = date
        self.__time = time
        self.__seizure_type = seizure_type
        self.__duration = duration
        self.__severity = severity
        self.__calendar_color = calendar_color
        self.__triggers = triggers
        self.__notes = notes

    def get_seizure_id(self): return self.__seizure_id
    def get_date(self): return self.__date
    def get_time(self): return self.__time
    def get_seizure_type(self): return self.__seizure_type
    def get_duration(self): return self.__duration
    def get_severity(self): return self.__severity
    def get_calendar_color(self): return self.__calendar_color
    def get_triggers(self): return self.__triggers
    def get_notes(self): return self.__notes