import re

class InvalidTime(RuntimeError):
    pass

class TimeOfDay:
    def __init__(self, hour, minute=0):
        self._raise_if_not_valid_time(hour, minute)
        
        self.hour = int(hour)
        self.minute = int(minute)
        self._duration = self.hour + (self.minute/60)

    @classmethod
    def from_24_hour_time(cls, time_str):
        hour, min = TimeOfDay.parse_24hr_time_str_to_hour_min(time_str)
        
        return cls(hour, min)
        
    @classmethod
    def from_12_hour_time(cls, time_str):
        hour, min = TimeOfDay.parse_12hr_time_str_to_hour_min(time_str)
        
        return cls(hour, min)
            
    @staticmethod
    def parse_12hr_time_str_to_hour_min(time_str):
        REGEX_12_HOUR_TIME = r'^([1][0-2]|[1-9]):([0-5][0-9])\s{0,}([a|A|p|P])'
        
        try:
            match = re.match(REGEX_12_HOUR_TIME, time_str)
            hour = int(match.group(1))
            min = int(match.group(2))
            period = match.group(3)
            
            # Convert the hour from 12 to 24 hour clock.
            hour = (hour + 12) % 24 if 'p' in period.lower() else hour
        
            return hour, min
        except (AttributeError, IndexError, TypeError) as e:
            raise InvalidTime(f'\'{time_str}\' is not a parseable time string. ({e.__class__.__name__})')
        
    @staticmethod
    def parse_24hr_time_str_to_hour_min(time_str):
        REGEX_24_HOUR_TIME = r'^([0-1][\d]|[2][0-3]):{0,1}([0-5][\d])$'
        
        try:
            match = re.match(REGEX_24_HOUR_TIME, time_str)
            hour = int(match.group(1))
            min = int(match.group(2))
            
            return hour, min
        except (AttributeError, IndexError, TypeError) as e:
            raise InvalidTime(f'\'{time_str}\' is not a parseable time string. ({e.__class__.__name__})')

    def hours_since(self, time):
        return time.hours_until(self)

    def hours_until(self, future):
        diff = future._duration - self._duration
        
        if diff > 0:
            return diff
        else: # Crossed midnight.
            return 24 - self._duration + future._duration

    def __str__(self):
        return f'{self.hour}:{self.minute}'

    @staticmethod
    def _raise_if_not_valid_time(hour, minute):    
        VALID_HOURS = range(0,24)
        VALID_MINS = range(0,60)
        
        if int(hour) not in VALID_HOURS or int(minute) not in VALID_MINS:
            raise InvalidTime(f'The time {hour}:{str(minute).zfill(2)} is not a valid time.')
