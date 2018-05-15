import unittest
from unittest.mock import MagicMock, mock_open, patch

from toolbag.timeofday import TimeOfDay

HOUR = 18
MIN = 30

AFTERNOON_24_TIME_STR_NO_COLON = '1630'
AFTERNOON_24_TIME_STR_WITH_COLON = '16:30'
AFTERNOON_24_TIME_HOUR = 16
AFTERNOON_24_TIME_MIN = 30

INVALID_HOUR = 25
INVALID_MIN = 60

class TimeOfDayTestCase(unittest.TestCase):
    def test_contructor_saves_values(self):
        tod = TimeOfDay(HOUR,MIN)
        self.assertEqual(tod.hour, HOUR)
        self.assertEqual(tod.minute, MIN)
        
    def test_constructor_excepts_on_invalid_hour(self):
        with self.assertRaises(ValueError):
            TimeOfDay(INVALID_HOUR, MIN)
    
    def test_constructor_excepts_on_invalid_minute(self):
        with self.assertRaises(ValueError):
            TimeOfDay(HOUR, INVALID_MIN)
        
    def test_constructor_excepts_on_invalid_time(self):
        with self.assertRaises(ValueError):
            TimeOfDay(INVALID_HOUR, INVALID_MIN)

    def test_from_24_hour_clock_time_no_colon(self):
        tod = TimeOfDay.from_24_hour_time(AFTERNOON_24_TIME_STR_NO_COLON)
        self.assertIsInstance(tod, TimeOfDay)
        self.assertEqual(tod.hour, AFTERNOON_24_TIME_HOUR)
        self.assertEqual(tod.minute, AFTERNOON_24_TIME_MIN)

    def test_from_24_hour_clock_time_with_colon(self):
        tod = TimeOfDay.from_24_hour_time(AFTERNOON_24_TIME_STR_WITH_COLON)
        self.assertIsInstance(tod, TimeOfDay)
        self.assertEqual(tod.hour, AFTERNOON_24_TIME_HOUR)
        self.assertEqual(tod.minute, AFTERNOON_24_TIME_MIN)

    def test_is_valid_time_lower_border(self):
        self.assertTrue(TimeOfDay.is_valid_time(0,0))
        
    def test_is_valid_time_upper_border(self):
        self.assertTrue(TimeOfDay.is_valid_time(24,0))
    
    def test_is_valid_time_minute_under_border(self):
        self.assertFalse(TimeOfDay.is_valid_time(0,-1))
    
    def test_is_valid_time_minute_over_border(self):
        self.assertFalse(TimeOfDay.is_valid_time(24,1))
        
    def test_is_valid_time_hour_under_border(self):
        self.assertFalse(TimeOfDay.is_valid_time(-1,0))
    
    def test_is_valid_time_hour_over_border(self):
        self.assertFalse(TimeOfDay.is_valid_time(25,0))
        
    def test__get_hour_and_min_from_24_hour_time_str_with_colon(self):
        hour, min = TimeOfDay._get_hour_and_min_from_24_hour_time_str(AFTERNOON_24_TIME_STR_WITH_COLON)
        self.assertEqual(AFTERNOON_24_TIME_HOUR, hour)
        self.assertEqual(AFTERNOON_24_TIME_MIN, min)
        
    def test__get_hour_and_min_from_24_hour_time_str_without_colon(self):
        hour, min = TimeOfDay._get_hour_and_min_from_24_hour_time_str(AFTERNOON_24_TIME_STR_NO_COLON)
        self.assertEqual(AFTERNOON_24_TIME_HOUR, hour)
        self.assertEqual(AFTERNOON_24_TIME_MIN, min)
        
    # TODO _get_hour_and_min_from_24_hour_time_str Handling 3 digit long strings, and handle index exceptions .
        
class HoursTestCase(unittest.TestCase):
  #def test_time_between_24hr_clock()
  pass
  