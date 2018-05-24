from toolbag.bookend import Bookend

with Bookend('Do some stuff... ', 'Done!') as be:
    be.change_outro('Failed!')