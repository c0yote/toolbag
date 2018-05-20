from unittest import TestCase, skip
from unittest.mock import MagicMock, mock_open, patch

from toolbag.timeofday import TimeOfDay, InvalidTime

class TimeOfDayTestCase(TestCase):
    def test_contructor_saves_values(self):
        tod = TimeOfDay(VALID_HOUR, VALID_MIN)
        self.assertEqual(tod.hour, VALID_HOUR)
        self.assertEqual(tod.minute, VALID_MIN)
        
    def test_constructor_excepts_on_invalid_hour(self):
        with self.assertRaises(InvalidTime):
            TimeOfDay(INVALID_HOUR, VALID_MIN)
    
    def test_constructor_excepts_on_invalid_minute(self):
        with self.assertRaises(InvalidTime):
            TimeOfDay(VALID_HOUR, INVALID_MIN)
        
    def test_constructor_excepts_on_invalid_time(self):
        with self.assertRaises(InvalidTime):
            TimeOfDay(INVALID_HOUR, INVALID_MIN)
    
    @patch('toolbag.timeofday.TimeOfDay._raise_if_not_valid_time')
    def test_constructor_calls_to_confirm_valid_time(self, valid_time_func_mock):
        tod = TimeOfDay(VALID_HOUR, VALID_MIN)
        valid_time_func_mock.assert_called_with(VALID_HOUR, VALID_MIN)

    def test_parse_24hr_time_str_to_hour_min_works_for_valid_times(self):
        for time_str, hr24, min in _all_valid_24_hr_clk_times():
            h, m = TimeOfDay.parse_24hr_time_str_to_hour_min(time_str)
            self.assertEqual(hr24, h)
            self.assertEqual(min, m)
            
    def test_parse_24hr_time_str_to_hour_min_excepts_on_invalid_times(self):
        for time_str, hr24, min in _some_invalid_24_hr_clk_times():
            with self.assertRaises(InvalidTime, msg=time_str) as e:
                TimeOfDay.parse_24hr_time_str_to_hour_min(time_str)
        
    def test_parse_12hr_time_str_to_hour_min_works_for_valid_times(self):
        for time_str, hr24, min in _all_valid_12_hr_clk_times():
            h, m = TimeOfDay.parse_12hr_time_str_to_hour_min(time_str)
            self.assertEqual(hr24, h)
            self.assertEqual(min, m)
        
    def test_from_12_hour_time_excepts_on_invalid_times(self):
        for time_str, hr24, min in _some_invalid_12_hr_clk_times():
            with self.assertRaises(InvalidTime, msg=time_str) as e:
                TimeOfDay.parse_12hr_time_str_to_hour_min(time_str)

    def test_from_24_hour_time_works_for_valid_times(self):
        tod = TimeOfDay.from_24_hour_time(VALID_24_CLK_TIME_STR)
        self.assertIsInstance(tod, TimeOfDay)
        self.assertEqual(tod.hour, VALID_24_CLK_TIME_HR)
        self.assertEqual(tod.minute, VALID_24_CLK_TIME_MIN)
        
    def test_from_24_hour_time_excepts_on_invalid_times(self):
        with self.assertRaises(InvalidTime) as e:
            TimeOfDay.from_24_hour_time(INVALID_24_CLK_TIME)

    def test_from_12_hour_time_works_for_valid_times(self):
        tod = TimeOfDay.from_12_hour_time(VALID_12_CLK_TIME_STR)
        self.assertIsInstance(tod, TimeOfDay)
        self.assertEqual(tod.hour, VALID_12_CLK_TIME_HR)
        self.assertEqual(tod.minute, VALID_12_CLK_TIME_MIN)

    def test_from_12_hour_time_excepts_on_invalid_times(self):
        with self.assertRaises(InvalidTime) as e:
            TimeOfDay.from_12_hour_time(INVALID_12_CLK_TIME)

    def test__str__returns_expected_string(self):
        tod = TimeOfDay.from_24_hour_time(VALID_24_CLK_TIME_STR)
        self.assertEqual(str(tod), VALID_24_CLK_TIME_STR)

# TEST CONSTANTS AND GENERATORS
VALID_HOUR = 4
VALID_MIN = 30
INVALID_HOUR = 25
INVALID_MIN = 60
VALID_12_CLK_TIME_STR = '10:09 PM'
VALID_12_CLK_TIME_HR = 22
VALID_12_CLK_TIME_MIN = 9
VALID_24_CLK_TIME_STR = '22:10'
VALID_24_CLK_TIME_HR = 22
VALID_24_CLK_TIME_MIN = 10
INVALID_12_CLK_TIME = '21:67 CE'
INVALID_24_CLK_TIME = '30:70'
VALID_12_HR_CLK_HRS = range(1,13)
VALID_AM_PERIODS = ('am','a.m.','AM','A.M.','a','A')
VALID_PM_PERIODS = ('pm','p.m.','PM','P.M.','p','P')
VALID_12_HR_PERIODS = VALID_AM_PERIODS + VALID_PM_PERIODS
VALID_12_HR_CLK_SPACE_OPTION = ('',' ')
VALID_24_HR_CLK_HRS = [str(i).zfill(2) for i in range(0,24)]
VALID_24_HR_COLON_OPTION = ('',':')
VALID_CLK_MINS = [str(i).zfill(2) for i in range(0,60)]
INVALID_12_HR_CLK_HRS = (0,) + tuple(range(13,110))
INVALID_12_HR_PERIODS = ('', 'bs','c.f.','DJ','E.M.','f','G')
INVALID_24_HR_CLK_HRS = range(24,125)
INVALID_CLK_MINS = [str(i).zfill(2) for i in range(60,160)]

def _generate_12hr_times(hrs, minutes, periods):
    for hr12 in hrs:
        for min in minutes:
            for space in VALID_12_HR_CLK_SPACE_OPTION:
                for period in periods:
                    time_str = f'{hr12}:{min}{space}{period}'

                    # Convert hour from 12-hour to 24-hour clock.
                    hr24 = ((int(hr12) + 12) % 24) if period in VALID_PM_PERIODS else int(hr12)
                    
                    
                    yield time_str, int(hr24), int(min)

def _all_valid_12_hr_clk_times():
    for time_str, hr24, min in _generate_12hr_times(VALID_12_HR_CLK_HRS, VALID_CLK_MINS, VALID_12_HR_PERIODS):
        yield time_str, hr24, min

def _some_invalid_12_hr_clk_times():
    # Invalid Hours
    for time_str, hr24, min in _generate_12hr_times(INVALID_12_HR_CLK_HRS, VALID_CLK_MINS, VALID_12_HR_PERIODS):
        yield time_str, int(hr24), int(min)
                
    # Invalid Mins
    for time_str, hr24, min in _generate_12hr_times(VALID_24_HR_CLK_HRS, INVALID_CLK_MINS, VALID_12_HR_PERIODS):
        yield time_str, int(hr24), int(min)
        
    # Invalid Period
    for time_str, hr24, min in _generate_12hr_times(VALID_24_HR_CLK_HRS, VALID_CLK_MINS, INVALID_12_HR_PERIODS):
        yield time_str, int(hr24), int(min)

def _generate_24hr_times(hrs, minutes):
    for hr24 in hrs:
        for min in minutes:
            for colon in VALID_24_HR_COLON_OPTION:
                time_str = f'{hr24}{colon}{min}'
                
                yield time_str, int(hr24), int(min)

def _all_valid_24_hr_clk_times():
    for time_str, hr24, min in _generate_24hr_times(VALID_24_HR_CLK_HRS, VALID_CLK_MINS):
        yield time_str, hr24, min

def _some_invalid_24_hr_clk_times():
    # Invalid Hours
    for time_str, hr24, min in _generate_24hr_times(INVALID_24_HR_CLK_HRS, VALID_CLK_MINS):
        yield time_str, int(hr24), int(min)
                
    # Invalid Mins
    for time_str, hr24, min in _generate_24hr_times(VALID_24_HR_CLK_HRS, INVALID_CLK_MINS):
        yield time_str, int(hr24), int(min)
    
    # Non-digit strings.
    non_digits = ['a105', '2b06', '20c7', '83z', 'y06']
    for s in non_digits:
        yield s, 0, 0
