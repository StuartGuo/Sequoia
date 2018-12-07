# -*- encoding: UTF-8 -*-

import talib as tl
import pandas as pd
import notify
import logging
import datetime


# TODO 真实波动幅度（ATR）放大
# 最后一个交易日收市价为指定区间内最高价
def check_max_price(stock, data, end_date=None, threshold=60):
    print("%s check max price" %stock)
    max_price = 0
    data = data.loc[:end_date]
    data = data.tail(n=threshold)
    if data.size < threshold:
        logging.info("{0}:样本小于{1}天...\n".format(stock, threshold))
        return False
    for index, row in data.iterrows():
        if row['close'] > max_price:
            max_price = float(row['close'])

    last_close = data.iloc[-1]['close']

    if last_close >= max_price:
        return True

    return False


# 最后一个交易日收市价突破指定区间内最高价
def check_breakthrough(stock, data, end_date=None, threshold=60):
    max_price = 0
    data = data.loc[:end_date]
    data = data.tail(n=threshold+1)
    if data.size < threshold + 1:
        logging.info("{0}:样本小于{1}天...\n".format(stock, threshold))
        return False

    # 最后一天收市价
    last_close = data.iloc[-1]['close']

    data = data.head(n=threshold)
    for index, row in data.iterrows():
        if row['close'] > max_price:
            max_price = float(row['close'])

    if last_close > max_price > data.iloc[-1]['close']:
        return True
    else:
        return False


# 均线突破
def check_ma(stock, data, end_date=None, ma_days=250):
    print("%s check ma" %stock)
    if len(data.index) < ma_days:
        logging.info("{0}:样本小于{1}天...\n".format(stock, ma_days))
        return False
    print("dat size %d" %data.size)
    data['ma'] = pd.Series(tl.MA(data['close'].values, ma_days), index=data.index.values)

    begin_date = data.iloc[0].name
    if end_date is not None:
        if end_date < begin_date:  # 该股票在end_date时还未上市
            logging.info("{}在{}时还未上市".format(stock, end_date))
            return False
    data = data.loc[:end_date]

    last_close = data.iloc[-1]['close']
    last_ma = data.iloc[-1]['ma']
    if last_close > last_ma:
        return True
    else:
        return False


def check_volume(code_name, data, end_date=None, threshold=40):
    stock = code_name[0]
    name = code_name[1]
    total_vol = 0
    
    if len(data.index) < threshold + 1:
        logging.info("{0}:样本小于{1}天...\n".format(stock, threshold))
        return False

    last_close = data.iloc[-1]['close']
    last_open = data.iloc[-1]['open']
    last_high = data.iloc[-1]['high']
 #（收盘价-开盘价）/（最高价-收盘价）>2   
    wr=(last_close-last_open)/(last_high-last_close)
    if(wr<2):
        return False

    last_vol = data.iloc[-1]['vol']
    last_change = data.iloc[-1]['change']
#当天上涨    
    if(last_change < 0):
        return False

    for index, row in data.iterrows():
        total_vol += float(row['vol'])
#成交量为60日最高
        if(row['vol'] > last_vol):
            return False
#最高价为60日最高
        if(row['high'] > last_high):
            return False

    mean_vol = total_vol / len(data.index)
    vol_ratio = last_vol / mean_vol
#成交量为60日平均成交量3倍以上
    if vol_ratio >= 3:
        msg = "*{0}({1})".format(name, stock)
        logging.info(msg)
        today = datetime.date.today().strftime('%Y%m%d')
        notify.notify(today+"-stock result",msg)
        return True
    else:
        return False
