#import debugpy
#debugpy.listen(5678)
from WeatherInterface import *
from datetime import datetime
from WeatherView import *

Viewer = WeatherViewer()

weather = Weather()
weather.GetNewTime()
Viewer.DisplayHours(weather.GetNextHourly())
Viewer.DisplayTomorrow(weather.GetTomorrow())
Viewer.DisplayNextDay(weather.GetNextDay())
Viewer.DoSleep()
