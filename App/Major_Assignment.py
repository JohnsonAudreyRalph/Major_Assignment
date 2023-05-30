import os
import pickle
from keras.models import load_model
import numpy as np
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMessageBox
import time
from datetime import datetime
import urllib.request
import pandas as pd
import socket
import warnings
warnings.filterwarnings("ignore", category=UserWarning)


def DATETIME_STAMP(dates):
    time_1 = dates.timetuple()
    time_2 = round(time.mktime(time_1))
    return time_2


def Predict_model_Close(open_value, high_value, low_value, volume_value):
    loaded_model_Close = load_model('Model/Model_Close.h5')
    features_Close_S = ["Open", "High", "Low", "Volume"]
    with open('Model/scaler_Close.pkl', 'rb') as file:
        scaler_Close_S = pickle.load(file)
    new_features_Close = scaler_Close_S.transform([[open_value, high_value, low_value, volume_value]])
    new_features_Close = pd.DataFrame(columns=features_Close_S, data=new_features_Close)
    new_data_Close = np.array(new_features_Close)
    new_data_Close = new_data_Close.reshape(new_data_Close.shape[0], 1, new_data_Close.shape[1])
    predicted_adj_close = loaded_model_Close.predict(new_data_Close)
    predicted_adj_close = predicted_adj_close[0][0]
    # print("Kết quả giá đóng cửa (Dự đoán) cho ngày mai:", predicted_adj_close)
    return predicted_adj_close


def Predict_model_Low(open_value, high_value, close_value, volume_value):
    features_Low_S = ["Open", "High", "Close", "Volume"]
    loaded_model_Low = load_model('Model/Model_Low.h5')
    with open('Model/scaler_Low.pkl', 'rb') as file:
        scaler_Low_S = pickle.load(file)
    new_features_Low = scaler_Low_S.transform([[open_value, high_value, close_value, volume_value]])
    new_features_Low = pd.DataFrame(columns=features_Low_S, data=new_features_Low)
    new_data_Low = np.array(new_features_Low)
    new_data_Low = new_data_Low.reshape(new_data_Low.shape[0], 1, new_data_Low.shape[1])
    predicted_adj_Low = loaded_model_Low.predict(new_data_Low)
    predicted_adj_Low = predicted_adj_Low[0][0]
    # print("Kết quả giá thấp nhất (Dự đoán) cho ngày mai:", predicted_adj_Low)
    return predicted_adj_Low


def Predict_model_High(open_value, low_value, close_value, volume_value):
    features_High_S = ["Open", "Low", "Close", "Volume"]
    loaded_model_High = load_model('Model/Model_High.h5')
    with open('Model/scaler_High.pkl', 'rb') as file:
        scaler_High_S = pickle.load(file)
    new_features_High = scaler_High_S.transform([[open_value, low_value, close_value, volume_value]])
    new_features_High = pd.DataFrame(columns=features_High_S, data=new_features_High)
    new_data_High = np.array(new_features_High)
    new_data_High = new_data_High.reshape(new_data_High.shape[0], 1, new_data_High.shape[1])
    predicted_adj_High = loaded_model_High.predict(new_data_High)
    predicted_adj_High = predicted_adj_High[0][0]
    # print("Kết quả (dự đoán) giá cao nhất: ", predicted_adj_High)
    return predicted_adj_High


def Predict_model_Open(high_value, low_value, close_value, volume_value):
    features_Open_S = ["High", "Low", "Close", "Volume"]
    loaded_model_Open = load_model('Model/Model_Open.h5')
    with open('Model/scaler_Open.pkl', 'rb') as file:
        scaler_Open_S = pickle.load(file)
    new_features_Open = scaler_Open_S.transform([[high_value, low_value, close_value, volume_value]])
    new_features_Open = pd.DataFrame(columns=features_Open_S, data=new_features_Open)
    new_data_Open = np.array(new_features_Open)
    new_data_Open = new_data_Open.reshape(new_data_Open.shape[0], 1, new_data_Open.shape[1])
    predicted_adj_Open = loaded_model_Open.predict(new_data_Open)
    predicted_adj_Open = predicted_adj_Open[0][0]
    # print("Kết quả (dự đoán) giá mở cửa: ", predicted_adj_Open)
    return predicted_adj_Open


def check_network_connection():
    try:
        # Tạo một socket mới
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)  # Đặt thời gian chờ kết nối là 2 giây

        # Thử kết nối đến một địa chỉ IP bất kỳ (ở đây chọn google.com)
        result = sock.connect_ex(('google.com', 80))
        if result == 0:
            return True  # Kết nối thành công
        else:
            return False  # Kết nối thất bại
        sock.close()
    except socket.error as e:
        print(str(e))
        return False


class Ui_MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super(Ui_MainWindow, self).__init__()
        self.txt_Predict_Close = None
        self.txt_Predict_Low = None
        self.txt_Predict_High = None
        self.txt_Predict_Open = None
        self.label_13 = None
        self.label_14 = None
        self.label_15 = None
        self.label_16 = None
        self.groupBox_3 = None
        self.btn_Date = None
        self.date_Value = None
        self.groupBox_2 = None
        self.lineEdit_9 = None
        self.label_12 = None
        self.lineEdit_2 = None
        self.lineEdit_3 = None
        self.lineEdit_4 = None
        self.lineEdit = None
        self.label_7 = None
        self.label_5 = None
        self.label_6 = None
        self.label_4 = None
        self.groupBox = None
        self.centralwidget = None
        self.statusbar = None
        self.setupUi()

    def closeEvent(self, event):
        """Override closeEvent to confirm window close."""
        reply = QMessageBox.question(self, "Xác nhận thoát", "Bạn có chắc chắn muốn thoát?",
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
        if reply == QMessageBox.Yes:
            # print("Bạn đã thoát")
            event.accept()
            self.close()  # Close the window
        else:
            event.ignore()

    def setupUi(self):
        self.setObjectName("MainWindow")
        self.resize(667, 669)
        self.setFixedSize(667, 669)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(20)
        font.setBold(True)
        font.setWeight(75)
        self.setFont(font)
        self.setAnimated(False)
        self.setDocumentMode(False)
        self.setDockNestingEnabled(False)
        self.setUnifiedTitleAndToolBarOnMac(False)
        self.centralwidget = QtWidgets.QWidget(parent=self)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 110, 641, 281))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox.setFont(font)
        self.groupBox.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.groupBox.setAutoFillBackground(False)
        self.groupBox.setObjectName("groupBox")
        self.label_4 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_4.setGeometry(QtCore.QRect(80, 230, 231, 41))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_5.setGeometry(QtCore.QRect(80, 130, 231, 41))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_6.setGeometry(QtCore.QRect(80, 80, 231, 41))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_7.setGeometry(QtCore.QRect(80, 30, 231, 41))
        self.label_7.setObjectName("label_7")
        self.lineEdit = QtWidgets.QLineEdit(parent=self.groupBox)
        self.lineEdit.setGeometry(QtCore.QRect(320, 30, 271, 41))
        self.lineEdit.setFrame(False)
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit.setReadOnly(True)
        self.lineEdit_2 = QtWidgets.QLineEdit(parent=self.groupBox)
        self.lineEdit_2.setGeometry(QtCore.QRect(320, 80, 271, 41))
        self.lineEdit_2.setFrame(False)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.lineEdit_2.setReadOnly(True)
        self.lineEdit_3 = QtWidgets.QLineEdit(parent=self.groupBox)
        self.lineEdit_3.setGeometry(QtCore.QRect(320, 130, 271, 41))
        self.lineEdit_3.setFrame(False)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.lineEdit_3.setReadOnly(True)
        self.lineEdit_4 = QtWidgets.QLineEdit(parent=self.groupBox)
        self.lineEdit_4.setGeometry(QtCore.QRect(320, 230, 271, 41))
        self.lineEdit_4.setFrame(False)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_4.setReadOnly(True)
        self.label_12 = QtWidgets.QLabel(parent=self.groupBox)
        self.label_12.setGeometry(QtCore.QRect(80, 180, 231, 41))
        self.label_12.setObjectName("label_12")
        self.lineEdit_9 = QtWidgets.QLineEdit(parent=self.groupBox)
        self.lineEdit_9.setGeometry(QtCore.QRect(320, 180, 271, 41))
        self.lineEdit_9.setFrame(False)
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.lineEdit_9.setReadOnly(True)
        self.groupBox_2 = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(10, 0, 641, 111))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.date_Value = QtWidgets.QDateEdit(parent=self.groupBox_2)
        self.date_Value.setGeometry(QtCore.QRect(150, 40, 161, 41))
        self.date_Value.setObjectName("date_Value")
        self.btn_Date = QtWidgets.QPushButton(parent=self.groupBox_2)
        self.btn_Date.setGeometry(QtCore.QRect(400, 40, 151, 41))
        self.btn_Date.setObjectName("btn_Date")
        self.btn_Date.clicked.connect(self.Click_Button)
        self.groupBox_3 = QtWidgets.QGroupBox(parent=self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 390, 641, 231))
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(14)
        font.setBold(True)
        font.setWeight(75)
        self.groupBox_3.setFont(font)
        self.groupBox_3.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.groupBox_3.setAutoFillBackground(False)
        self.groupBox_3.setObjectName("groupBox_3")
        self.label_13 = QtWidgets.QLabel(parent=self.groupBox_3)
        self.label_13.setGeometry(QtCore.QRect(40, 130, 271, 41))
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(parent=self.groupBox_3)
        self.label_14.setGeometry(QtCore.QRect(40, 80, 271, 41))
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(parent=self.groupBox_3)
        self.label_15.setGeometry(QtCore.QRect(40, 30, 271, 41))
        self.label_15.setObjectName("label_15")
        self.txt_Predict_Open = QtWidgets.QLineEdit(parent=self.groupBox_3)
        self.txt_Predict_Open.setGeometry(QtCore.QRect(320, 30, 271, 41))
        self.txt_Predict_Open.setFrame(False)
        self.txt_Predict_Open.setObjectName("txt_Predict_Open")
        self.txt_Predict_Open.setReadOnly(True)
        self.txt_Predict_High = QtWidgets.QLineEdit(parent=self.groupBox_3)
        self.txt_Predict_High.setGeometry(QtCore.QRect(320, 80, 271, 41))
        self.txt_Predict_High.setFrame(False)
        self.txt_Predict_High.setObjectName("txt_Predict_High")
        self.txt_Predict_High.setReadOnly(True)
        self.txt_Predict_Low = QtWidgets.QLineEdit(parent=self.groupBox_3)
        self.txt_Predict_Low.setGeometry(QtCore.QRect(320, 130, 271, 41))
        self.txt_Predict_Low.setFrame(False)
        self.txt_Predict_Low.setObjectName("txt_Predict_Low")
        self.txt_Predict_Low.setReadOnly(True)
        self.label_16 = QtWidgets.QLabel(parent=self.groupBox_3)
        self.label_16.setGeometry(QtCore.QRect(40, 180, 271, 41))
        self.label_16.setObjectName("label_16")
        self.txt_Predict_Close = QtWidgets.QLineEdit(parent=self.groupBox_3)
        self.txt_Predict_Close.setGeometry(QtCore.QRect(320, 180, 271, 41))
        self.txt_Predict_Close.setFrame(False)
        self.txt_Predict_Close.setObjectName("txt_Predict_Close")
        self.txt_Predict_Close.setReadOnly(True)
        self.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(parent=self)
        self.statusbar.setObjectName("statusbar")
        self.setStatusBar(self.statusbar)

        self.retranslateUi(self)
        QtCore.QMetaObject.connectSlotsByName(self)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Dự đoán giá cổ phiếu thông qua mô hình LSTM"))
        self.groupBox.setTitle(_translate("MainWindow", "Xác nhận thông tin"))
        self.label_4.setText(_translate("MainWindow", "Khối lượng giao dịch: "))
        self.label_5.setText(_translate("MainWindow", "Giá thấp nhất:"))
        self.label_6.setText(_translate("MainWindow", "Giá cao nhất:"))
        self.label_7.setText(_translate("MainWindow", "Giá mở cửa: "))
        self.label_12.setText(_translate("MainWindow", "Giá đóng cửa:"))
        self.groupBox_2.setTitle(_translate("MainWindow", "Chọn thời gian"))
        self.date_Value.setDisplayFormat(_translate("MainWindow", "dd/MM/yyyy"))

        self.btn_Date.setText(_translate("MainWindow", "Xác nhận"))

        self.groupBox_3.setTitle(_translate("MainWindow", "Kết quả dự đoán hôm sau"))
        self.label_13.setText(_translate("MainWindow", "Giá thấp nhất (Dự đoán):"))
        self.label_14.setText(_translate("MainWindow", "Giá cao nhất (Dự đoán):"))
        self.label_15.setText(_translate("MainWindow", "Giá mở cửa (Dự đoán): "))
        self.label_16.setText(_translate("MainWindow", "Giá đóng cửa (Dự đoán):"))

    def Click_Button(self):
        # Kiểm tra kết nối mạng trước khi thực hiện yêu cầu
        if check_network_connection():
            # print("Có kết nối mạng")
            selected_date = self.date_Value.date()
            day = selected_date.day()
            month = selected_date.month()
            year = selected_date.year()
            # print(f"Ngày đã chọn: {day}/{month}/{year}")
            star_Time = DATETIME_STAMP(datetime(year, month, day+1))
            end_Time = DATETIME_STAMP(datetime(year, month, day+1))
            url = 'https://query1.finance.yahoo.com/v7/finance/download/NFLX?period1=' + str(star_Time) + '&period2=' + str(
                end_Time) + '&interval=1d'
            # print(url)
            # Kiểm tra xem tệp data đã tồn tại hay chưa, nếu đã tồn tại rồi => Xóa, chưa tồn tại thì thực hiện tải xuống
            filename = 'Data.csv'
            if os.path.exists(filename):
                os.remove(filename)
                # print("Đã xóa")
            # print("Tệp chưa tồn tại! Thực hiện tải xuống")
            filename = 'Data.csv'  # Tên tệp để lưu trữ dữ liệu tải xuống
            try:
                urllib.request.urlretrieve(url, filename)
                # print("Tệp đã được tải xuống thành công.")
                data = pd.read_csv('Data.csv')
                # print(data)
                # Truy cập vào hàng đầu tiên của DataFrame để lấy giá trị cần điền
                row = data.iloc[0]
                # Điền giá trị vào các lineEdit
                self.lineEdit.setText(str(row['Open']))
                self.lineEdit_2.setText(str(row['High']))
                self.lineEdit_3.setText(str(row['Low']))
                self.lineEdit_9.setText(str(row['Close']))
                self.lineEdit_4.setText(str(row['Volume']))
                Predict_Open = Predict_model_Open(str(row['High']), str(row['Low']), str(row['Close']),
                                                  str(row['Volume']))
                self.txt_Predict_Open.setText(str(Predict_Open))
                Predict_High = Predict_model_High(str(row['Open']), str(row['Low']), str(row['Close']),
                                                  str(row['Volume']))
                self.txt_Predict_High.setText(str(Predict_High))
                Predict_Low = Predict_model_Low(str(row['Open']), str(row['High']), str(row['Close']),
                                                str(row['Volume']))
                self.txt_Predict_Low.setText(str(Predict_Low))
                Predict_Close = Predict_model_Close(str(row['Open']), str(row['High']), str(row['Low']),
                                                    str(row['Volume']))
                self.txt_Predict_Close.setText(str(Predict_Close))
            except urllib.error.URLError as e:
                # print("Lỗi khi tải xuống tệp:", e)
                QMessageBox.information(self, "Lỗi", "Ngày bạn chọn không mở chứng khoán", QMessageBox.Ok)
        else:
            QMessageBox.warning(self, "Không kết nối mạng",
                                "Không thể kết nối với mạng. \nVui lòng kiểm tra kết nối mạng của bạn.")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    ex = Ui_MainWindow()
    ex.show()
    sys.exit(app.exec_())
