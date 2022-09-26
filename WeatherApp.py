#import debugpy
#debugpy.listen(5678)
from WeatherInterface import *
from datetime import datetime
from WeatherView import *

Viewer = WeatherViewer()

weather = Weather()
weather.GetNewTime()
#weather.TestViaFile(os.getcwd() + "\\" + "sample_partly_cloudy.json")
Viewer.DisplayHours(weather.GetNextHourly())
Viewer.DisplayTomorrow(weather.GetTomorrow())
Viewer.DisplayNextDay(weather.GetNextDay())

