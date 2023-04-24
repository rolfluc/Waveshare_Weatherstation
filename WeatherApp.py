from WeatherInterface import *
from datetime import datetime
from WeatherView import *

Viewer = WeatherViewer()

weather = Weather()
weather.GetNewTime()
weather.TestViaFile("sample_snow.json")
Viewer.DisplayToday(weather.GetToday())
Viewer.DisplayTomorrow(weather.GetTomorrow())
Viewer.DisplayNextDay(weather.GetNextDay())
Viewer.SendToScreen()
Viewer.DoSleep()
