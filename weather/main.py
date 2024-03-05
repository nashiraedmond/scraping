from requests_html import HTMLSession
from  dataclasses import dataclass

@dataclass
class Weather_data:
    temperature: str
    units: str
    precipate: str
    humidity: str
    day_time: str
    wind: str
    day_clouds: str

s=  HTMLSession()
query = 'denmark'
url = f'https://www.google.com/search?q=weather+{query}'

header = {"user-agent": 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}
r = s.get(url, headers=header)

temp = r.html.find('span#wob_tm', first=True).text
units = r.html.find('div.vk_bk.wob-unit span.wob_t', first=True).text
precipate = r.html.find('div.wtsRwe span#wob_pp', first=True).text
humidity = r.html.find('div.wtsRwe span#wob_hm', first=True).text
wind = r.html.find('div.wtsRwe span#wob_ws', first=True).text
day_time = r.html.find('div.VQF4g', first=True).find('div#wob_dts', first=True).text
day_clouds = r.html.find('div.VQF4g', first=True).find('span#wob_dc', first=True).text

print(temp, units, precipate, humidity, wind, day_time, day_clouds)
