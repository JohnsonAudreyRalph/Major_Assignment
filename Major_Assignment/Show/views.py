from django.shortcuts import render
import time
from datetime import datetime
import urllib.request
import os
import pandas as pd
from keras.models import load_model
import numpy as np
import pickle


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
    features_Open_S = ["High", "Low", "Close", "Volume"]
    loaded_model_Open = load_model('static/Model/Model_Open.h5')
    with open('static/Model/scaler_Open.pkl', 'rb') as file:
        scaler_Open_S = pickle.load(file)
    new_features_Open = scaler_Open_S.transform([[high_value, low_value, close_value, volume_value]])
    new_features_Open = pd.DataFrame(columns=features_Open_S, data=new_features_Open)
    new_data_Open = np.array(new_features_Open)
    new_data_Open = new_data_Open.reshape(new_data_Open.shape[0], 1, new_data_Open.shape[1])
    predicted_adj_Open = loaded_model_Open.predict(new_data_Open)
    predicted_adj_Open = predicted_adj_Open[0][0]
    print("Kết quả (dự đoán) giá mở cửa: ", predicted_adj_Open)
    return predicted_adj_Open


def Predict_model_High(open_value, low_value, close_value, volume_value):
    features_High_S = ["Open", "Low", "Close", "Volume"]
    loaded_model_High = load_model('static/Model/Model_High.h5')
    with open('static/Model/scaler_High.pkl', 'rb') as file:
        scaler_High_S = pickle.load(file)
    new_features_High = scaler_High_S.transform([[open_value, low_value, close_value, volume_value]])
    new_features_High = pd.DataFrame(columns=features_High_S, data=new_features_High)
    new_data_High = np.array(new_features_High)
    new_data_High = new_data_High.reshape(new_data_High.shape[0], 1, new_data_High.shape[1])
    predicted_adj_High = loaded_model_High.predict(new_data_High)
    predicted_adj_High = predicted_adj_High[0][0]
    print("Kết quả (dự đoán) giá cao nhất: ", predicted_adj_High)
    return predicted_adj_High


def Predict_model_Low(open_value, high_value, close_value, volume_value):
    features_Low_S = ["Open", "High", "Close", "Volume"]
    loaded_model_Low = load_model('static/Model/Model_Low.h5')
    with open('static/Model/scaler_Low.pkl', 'rb') as file:
        scaler_Low_S = pickle.load(file)
    new_features_Low = scaler_Low_S.transform([[open_value, high_value, close_value, volume_value]])
    new_features_Low = pd.DataFrame(columns=features_Low_S, data=new_features_Low)
    new_data_Low = np.array(new_features_Low)
    new_data_Low = new_data_Low.reshape(new_data_Low.shape[0], 1, new_data_Low.shape[1])
    predicted_adj_Low = loaded_model_Low.predict(new_data_Low)
    predicted_adj_Low = predicted_adj_Low[0][0]
    print("Kết quả giá thấp nhất (Dự đoán) cho ngày mai:", predicted_adj_Low)
    return predicted_adj_Low


def Predict_model_Close(open_value, high_value, low_value, volume_value):
    loaded_model_Close = load_model('static/Model/Model_Close.h5')
    features_Close_S = ["Open", "High", "Low", "Volume"]
    with open('static/Model/scaler_Close.pkl', 'rb') as file:
        scaler_Close_S = pickle.load(file)
    new_features_Close = scaler_Close_S.transform([[open_value, high_value, low_value, volume_value]])
    new_features_Close = pd.DataFrame(columns=features_Close_S, data=new_features_Close)
    new_data_Close = np.array(new_features_Close)
    new_data_Close = new_data_Close.reshape(new_data_Close.shape[0], 1, new_data_Close.shape[1])
    predicted_adj_close = loaded_model_Close.predict(new_data_Close)
    predicted_adj_close = predicted_adj_close[0][0]
    print("Kết quả giá đóng cửa (Dự đoán) cho ngày mai:", predicted_adj_close)
    return predicted_adj_close


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
    Predict_Open = []
    Predict_High = []
    Predict_Low = []
    Predict_Close = []
    # Lấy giá trị của từng cột theo ngày và lưu vào các mảng tương ứng
    for date, row in data_30_Row.iterrows():
        Day.append(date)
        Open.append(row['Open'])
        High.append(row['High'])
        Low.append(row['Low'])
        Close.append(row['Close'])
        Volume.append(row['Volume'])
        print('High: ', High)
        print('Low: ', Low)
        print('Close: ', Close)
        print('Volume: ', Volume)
        Predict_Open.append(Predict_model_Open(High[-1], Low[-1], Close[-1], Volume[-1]))
        Predict_High.append(Predict_model_High(Open[-1], Low[-1], Close[-1], Volume[-1]))
        Predict_Low.append(Predict_model_Low(Open[-1], High[-1], Close[-1], Volume[-1]))
        Predict_Close.append(Predict_model_Close(Open[-1], High[-1], Low[-1], Volume[-1]))
    # In ra kết quả
    # for i in range(len(Day)):
        # print("Date:", Day[i])
        # print("Open:", Open[i])
        # print("High:", High[i])
        # print("Low:", Low[i])
        # print("Close:", Close[i])
        # print("Volume:", Volume[i])
        # print("Predict Open: ", Predict_Open[i])
        # print("Predict High: ", Predict_High[i])
        # print("Predict Low: ", Predict_Low[i])
        # print("Predict Close: ", Predict_Close[i])
        # print("\n")
    context = {
        'Day': Day,
        'Open': Open,
        'High': High,
        'Low': Low,
        'Close': Close,
        'Volume': Volume,
        'Predict_Open': Predict_Open,
        'Predict_High': Predict_High,
        'Predict_Low': Predict_Low,
        'Predict_Close': Predict_Close
    }
    return render(req, 'index.html', context)
    # return render(req, 'CHAR.html', context)
