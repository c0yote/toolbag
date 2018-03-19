import sys

class ProgressBar():
  PERCENTAGE_STR_LENGTH = 8
  BAR_LEFT_BORDER = '['
  BAR_RIGHT_BORDER = ']'
  
  def __init__(self, width=60):
    self.width = width
    
  def render(self, progress):
    text = self._build_progress_bar_string(progress)
    sys.stdout.write(text)
    sys.stdout.flush()
    
  def _get_bar_field_width(self):
    return (self.width - 
            ProgressBar.PERCENTAGE_STR_LENGTH -
            len(ProgressBar.BAR_LEFT_BORDER) -
            len(ProgressBar.BAR_RIGHT_BORDER))
      
    
  def _build_progress_bar_string(self, progress):
    return ('\r' +
           self._build_bar_string(progress) +
           self._build_percent_string(progress))
    
  def _build_bar_string(self, progress):
    fill_char_count = int(self._get_bar_field_width() * progress)
    empty_char_count = self._get_bar_field_width() - fill_char_count
    
    filled_field_str = ''.join(['#' for i in range(fill_char_count)])
    empty_field_str = ''.join([' ' for i in range(empty_char_count)])
    
    return (ProgressBar.BAR_LEFT_BORDER +
            filled_field_str + 
            empty_field_str +
            ProgressBar.BAR_RIGHT_BORDER)
    
  def _build_percent_string(self, progress):
    percent = round(progress * 100, 1)
    return f'{percent:>{ProgressBar.PERCENTAGE_STR_LENGTH}} %'
  
if __name__ == '__main__':
  import time
  
  # Demo
  pb = ProgressBar(80)
  
  progress = 0.0
  while progress <= 1.0:
    progress += 0.05
    time.sleep(.1)
    pb.render(progress)
    