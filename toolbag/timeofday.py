class TimeOfDay:
    VALID_HOURS = range(0,25)
    VALID_MINUTES = range(0,60)

    def __init__(self, hour, minute=0):    
        if not TimeOfDay.is_valid_time(hour, minute):
            raise ValueError(f'The time {hour}:{minute} is not a valid time.')
            
        self.hour = hour
        self.minute = minute
        
        
    @classmethod
    def from_24_hour_time(cls, time_str):
        hour, min = TimeOfDay._get_hour_and_min_from_24_hour_time_str(time_str)
        return cls(hour, min)
        
    @classmethod
    def from_12_hour_time(time_str):
        pass
            
    @staticmethod
    def is_valid_time(hour, minute):    
        if not hour in TimeOfDay.VALID_HOURS:
            return False
        elif not minute in TimeOfDay.VALID_MINUTES:
            return False
        elif TimeOfDay._is_past_2400(hour, minute):
            return False
        else:
            return True

    @staticmethod
    def _get_hour_and_min_from_24_hour_time_str(time_str):
        sanatized_time_str = time_str.replace(':', '')
        # TODO Handling 3 digit long strings, and handle index exceptions .
        hour = int(sanatized_time_str[0:2])
        min = int(sanatized_time_str[2:4])
        return hour, min
            
    @staticmethod
    def _is_past_2400(hour, minute):
        return (hour == 24 and minute > 0)