# from tvDatafeed import TvDatafeed, Interval
#
# tv = TvDatafeed()
#
# nifty_index_data = tv.get_hist(symbol="NIFTY", exchange="NSE", interval=Interval.in_1_hour, n_bars=1000, fut_contract=1)
#
# print(nifty_index_data)


# from tradingview_ta import TA_Handler, Interval, Exchange
#
# data = TA_Handler(
#     symbol="HNG",
#     screener="vietnam",
#     exchange="HOSE",
#     interval=Interval.INTERVAL_1_MONTH
# )
#
# print(data.get_analysis().indicators)

# from tradingview_ta import TA_Handler, Interval, Exchange
#
# data = TA_Handler(
#     symbol="HNG",
#     screener="vietnam",
#     exchange="HOSE",
#     interval=Interval.INTERVAL_1_MONTH
# )
#
# analysis = data.get_analysis().indicators
#
# print(analysis)
# x = data.get_analysis().time
# print(x)

# # Duyệt qua từng chỉ số và xuất dữ liệu
# for indicator in indicators:
#     print(f"Chỉ số: {indicator}")
#     for date in analysis.indicators[indicator]:
#         value = analysis.indicators[indicator][date]
#         print(f"Ngày: {date}")
#         print(f"Giá trị: {value}")
#         print()

# from tradingview_ta import TA_Handler, Interval, Exchange
#
# data = TA_Handler(
#     symbol="HNG",
#     screener="vietnam",
#     exchange="HOSE",
#     interval=Interval.INTERVAL_1_DAY
# )
#
# candles = data.get_analysis().indicators
# # print(candles)
# open_price = candles['open']
# print(open_price)

#
# # Duyệt qua từng ngày và xuất dữ liệu
# for candle in candles:
#     # date = candle['datetime']
#     open_price = candle['open']
#     high_price = candle['high']
#     low_price = candle['low']
#     close_price = candle['close']
#     volume = candle['volume']
#
#     # print(f"Ngày: {date}")
#     print(f"Mở cửa: {open_price}")
#     print(f"Cao nhất: {high_price}")
#     print(f"Thấp nhất: {low_price}")
#     print(f"Đóng cửa: {close_price}")
#     print(f"Khối lượng: {volume}")
#     print()

# from tradingview_ta import TA_Handler, Interval, Exchange
#
# data = TA_Handler(
#     symbol="HNG",
#     screener="vietnam",
#     exchange="HOSE",
#     interval=Interval.INTERVAL_1_MONTH
# )
#
# analysis = data.get_analysis()
# indicators = analysis.indicators
# print(indicators)
#
# time_info = analysis.time
# print(time_info)

import yfinance as yf

nifty_index_data = yf.download("FPT", period="11y", interval="1d")
# nifty_index_data = yf.download("FPT", period="2y", interval="1h")
# [1m, 2m, 5m, 15m, 30m, 60m, 90m, 1h, 1d, 5d, 1wk, 1mo, 3mo]

# Lưu dữ liệu vào file CSV
# nifty_index_data.to_csv("Data.csv")

# Hiển thị thông tin về dữ liệu
print(nifty_index_data)
