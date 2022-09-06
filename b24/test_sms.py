import requests
from smsc_api import *

smsc = SMSC()
r = smsc.send_sms("79823105691", "Тестовое сообщение", sender="sms")

print(r)

# r = requests.post("https://sms.ru/sms/send?api_id=B53FA6D1-EF23-B17F-BBD6-9D5BD11C4729&to=" + "79823105691" +
#                   "&msg=" + "hello+world" + "&json=1")
