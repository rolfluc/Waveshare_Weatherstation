#import debugpy
#debugpy.listen(5678)
from WeatherInterface import *
from datetime import datetime

weather = Weather()
weather.GetNewTime()
#weather.GetNextHourly()
#weather.GetTomorrow()
