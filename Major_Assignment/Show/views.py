from django.shortcuts import render
import time
from datetime import datetime
import urllib.request
import os
import pandas as pd
from keras.models import load_model
import numpy as np
from sklearn.preprocessing import MinMaxScaler


# Create your views here.
def DATETIME_STAMP(dates):
    time_1 = dates.timetuple()
    time_2 = round(time.mktime(time_1))
    return time_2


def dowload_file():
    # Kiểm tra xem tệp data đã tồn tại hay chưa, nếu đã tồn tại rồi => Xóa, chưa tồn tại thì thực hiện tải xuống
    filename = 'static/Data/Data.csv'
    if os.path.exists(filename):
        os.remove(filename)
        print("Đã xóa")
    print("Tệp chưa tồn tại! Thực hiện tải xuống")
    star_Time = DATETIME_STAMP(datetime(2004, 1, 1))
    end_Time = DATETIME_STAMP(datetime(2019, 1, 1))
    url = 'https://query1.finance.yahoo.com/v7/finance/download/NFLX?period1=' + str(star_Time) + '&period2=' + str(
        end_Time) + '&interval=1d&events=history&includeAdjustedClose=true'
    urllib.request.urlretrieve(url, 'Data.csv')
    try:
        urllib.request.urlretrieve(url, filename)
        print("Tệp đã được tải xuống thành công.")
    except urllib.error.URLError as e:
        print("Lỗi khi tải xuống tệp:", e)


def Predict_model_Open(high_value, low_value, close_value, volume_value):
    model = load_model('Model/Model_Open.h5')
    features = ["Open", "High", "Low", "Volume"]
    scaler = MinMaxScaler(feature_range=(0, 1))

    # Chuẩn hóa đặc trưng mới
    new_features = scaler.transform([[high_value, low_value, close_value, volume_value]])
    new_features = pd.DataFrame(columns=features, data=new_features)

    # Chuyển đổi dữ liệu mới thành dạng phù hợp cho LSTM
    new_data = np.array(new_features)
    new_data = new_data.reshape(new_data.shape[0], 1, new_data.shape[1])
    predicted_adj_close = model.predict(new_data)
    # In kết quả dự đoán
    print("Kết quả giá mở cửa (Dự đoán) cho ngày mai:", predicted_adj_close)


def index(req):
    dowload_file()
    data = pd.read_csv('Data.csv')
    data.drop(["Adj Close"], axis=1, inplace=True)
    print(data)
    print("\n==========================================================================")
    data_30_Row = data.tail(30)
    print(data_30_Row)
    # Thiết lập cột Date làm chỉ mục (index) của DataFrame
    data_30_Row.set_index('Date', inplace=True)
    # Khởi tạo các mảng để lưu giá trị
    Day = []
    Open = []
    High = []
    Low = []
    Close = []
    Volume = []
    # Lấy giá trị của từng cột theo ngày và lưu vào các mảng tương ứng
    for date, row in data_30_Row.iterrows():
        Day.append(date)
        Open.append(row['Open'])
        High.append(row['High'])
        Low.append(row['Low'])
        Close.append(row['Close'])
        Volume.append(row['Volume'])
    # In ra kết quả
    for i in range(len(Day)):
        print("Date:", Day[i])
        print("Open:", Open[i])
        print("High:", High[i])
        print("Low:", Low[i])
        print("Close:", Close[i])
        print("Volume:", Volume[i])
        conten = {
            'Day': Day,
            'Open': Open,
            'High': High,
            'Low': Low,
            'Close': Close,
            'Volume': Volume
        }
    return render(req, 'index.html')
