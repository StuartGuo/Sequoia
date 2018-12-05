# -*- coding: UTF-8 -*-

import tushare as ts
import datetime
import logging
from pandas.tseries.offsets import Day
import utils

DATA_DIR = 'data'

CONFIG_ALL='config/Astock.xlsx'


def append(code_name):
    stock = code_name[0]
    name = code_name[1]
    old_data = utils.read_data(stock, name)

    if old_data is None:
        today = datetime.date.today().strftime('%Y%m%d')
        preday = (datetime.date.today()-60*Day()).strftime('%Y%m%d')
        api = ts.pro_api()
        data = ts.pro_bar(pro_api=api, ts_code=stock, adj='qfq', start_date=preday, end_date=today)
        if data is None or data.empty:
            logging.info("股票："+stock+" 数据下载失败，重试...")
            return
        if len(data) < 30:
            logging.info("股票："+stock+" 上市时间小于30日，略过...")
            return
        data = data.sort_index()
        file_name = stock + '-' + name + '.csv'
        file_path = DATA_DIR + "/" + file_name
        print("create-"+file_path) 
        data.to_csv(file_path)
    else:
        start_date = old_data.iloc[-1]['trade_date']
        today = datetime.date.today().strftime('%Y%m%d')
        if start_date == today:
            return
        api = ts.pro_api()
        appender = ts.pro_bar(pro_api=api, ts_code=stock, adj='qfq', start_date=today, end_date=today)
        print(appender)
        if appender is None:
            logging.info("股票：{} 没有新的数据，略过。。。".format(stock))
        else:
            file_name = stock + '-' + name + '.csv'
            file_path = DATA_DIR + "/" + file_name
            print("append-"+file_path) 
            appender.to_csv(file_path, mode='a', header=False)

def fetch(code_name):
    stock = code_name[0]
    name = code_name[1]
    today = datetime.date.today().strftime('%Y%m%d')
    preday = (datetime.date.today()-60*Day()).strftime('%Y%m%d')
    api = ts.pro_api()
    data = ts.pro_bar(pro_api=api, ts_code=stock, adj='qfq', start_date=preday, end_date=today)
    if data is None or data.empty:
        logging.info("股票："+stock+" 数据下载失败，重试...")
        return
    if len(data) < 30:
        logging.info("股票："+stock+" 上市时间小于30日，略过...")
        return
    data = data.sort_index()
    file_name = stock + '-' + name + '.csv'
    file_path = DATA_DIR + "/" + file_name
    print("create-"+file_path) 
    data.to_csv(file_path)


def run():
    code_names = utils.get_stocks(CONFIG_ALL)
    if code_names:
        # stocks = list(zip(*code_names))
        [append(ss) for ss in code_names]
        # pool = threadpool.ThreadPool(10)
        # requests = threadpool.makeRequests(append, stocks)
        # [pool.putRequest(req) for req in requests]
        # pool.wait()

