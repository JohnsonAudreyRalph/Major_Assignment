# import yfinance as yf
#
# start_date = "2001-01-11"
# end_date = "2023-05-17"
#
# FPT_data = yf.download("FPT", start=start_date, end=end_date, interval="1d")
# print(FPT_data)

# from datetime import datetime
#
# # Nhập khoảng thời gian bất kỳ
# start_date = datetime(2004, 1, 1)  # Ngày bắt đầu
# end_date = datetime(2023, 5, 18)  # Ngày kết thúc
#
# # Chuyển đổi thành thời điểm Unix Epoch
# start_timestamp = int(start_date.timestamp())
# end_timestamp = int(end_date.timestamp())
#
# print("Thời điểm Unix Epoch của ngày bắt đầu:", start_timestamp)
# print("Thời điểm Unix Epoch của ngày kết thúc:", end_timestamp)


# import time
# from datetime import datetime
#
#
# def START_TIME(dates):
#     time_1 = dates.timetuple()
#     time_2 = round(time.mktime(time_1))
#     return time_2
#
#
# date = datetime.now()
# print(START_TIME(date))


import requests, time
import pandas as pd
from datetime import datetime

def DATETIME_STAMP(dates):
    time_1 = dates.timetuple()
    time_2 = round(time.mktime(time_1))
    return time_2

star_Time = DATETIME_STAMP(datetime(2004, 1, 1))
end_Time = DATETIME_STAMP(datetime(2019,1,1))
# url = 'https://query1.finance.yahoo.com/v7/finance/chart/NFLX?period1='+str(star_Time)+'&period2='+str(end_Time)+'&interval=1d&events=history&includeAdjustedClose=true'
url = 'http://query1.finance.yahoo.com/v7/finance/chart/NFLX?period1='+str(star_Time)+'&period2='+str(end_Time)+'&interval=1d'
print(url)

response = requests.get(url)
print(response.text)
try:
    req = requests.get(url)
    req.raise_for_status()
    data = req.json()
    print(data)
except requests.exceptions.RequestException as e:
    print("Error occurred:", e)
except ValueError as e:
    print("Error decoding JSON:", e)

# req = requests.get(url).json()
# req = requests.get(url)
# print(req)
# import urllib.request
#
# filename = 'data.csv'  # Tên tệp để lưu trữ dữ liệu tải xuống
#
# try:
#     urllib.request.urlretrieve(url, filename)
#     print("Tệp đã được tải xuống thành công.")
# except urllib.error.URLError as e:
#     print("Lỗi khi tải xuống tệp:", e)


# import requests
#
# url = "https://query1.finance.yahoo.com/v7/finance/chart/NFLX?period1=1072890000&period2=1546275600&interval=1d"
#
# response = requests.get(url)
# print(response.text)


