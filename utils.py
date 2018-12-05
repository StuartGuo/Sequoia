# -*- coding: UTF-8 -*-
import datetime

import xlrd
import pandas as pd
import os
import time

DATA_DIR = 'data'
ONE_HOUR_SECONDS = 60 * 60

def strategy_pool(config=None):
    stock_list=list()
    data = pd.read_excel(config)
    for index,row in data.iterrows():
        ts_code=str(row['ts_code'])
        name=str(row['name'])
        close=row['close']
        turnover_rate=row['turnover_rate']
        turnover_rate_f=row['turnover_rate_f']
        volume_ratio=row['volume_ratio']
        pe=row['pe']
        pe_ttm=row['pe_ttm']
        pb=row['pb']
        ps=row['ps'] 
        ps_ttm=row['ps_ttm']
        total_share=row['total_share']
        float_share=row['float_share']
        free_share=row['free_share']
        total_mv=row['total_mv']
        circ_mv=row['circ_mv']
#ts_code 非ST
#pe_ttm 不大于100
#ps_ttm 不大于10
#circ_mv 小于1000000/100000
        if(name.find("ST")>=0):
            continue
        if((pe_ttm==0) or (ps_ttm==0) or (circ_mv==0)):
            continue
        if((pe_ttm<=100) and (ps_ttm<=10) and (circ_mv<300000)):
            stock=list()
            stock.append(ts_code)
            stock.append(name)
            stock_list.append(stock)
    return stock_list

# 获取股票代码列表
def get_stocks(config=None):
    if config:
        return strategy_pool(config)
    else:
        data_files = os.listdir(DATA_DIR)
        stocks = []
        for file in data_files:
            code_name = file.split(".c")[0]
            code = code_name.split("-")[0]
            name = code_name.split("-")[1]
            appender = (code, name)
            stocks.append(appender)
        return stocks


# 读取本地数据文件
def read_data(stock, name):
    file_name = stock + '-' + name + '.csv'
    try:
        f = open(DATA_DIR + "/" + file_name)
        df = pd.read_csv(f)
        f.close()
        return df
    except FileNotFoundError:
        return None


# 是否需要更新数据
def need_update_data():
    try:
        filename = "data/000001.SH-平安银行.csv"
        last_modified = os.stat(filename).st_mtime
        now = time.time()
        time_diff = now - last_modified
        return time_diff > ONE_HOUR_SECONDS
    except FileNotFoundError:
        return True


# 是否是工作日
def is_weekday():
    return datetime.datetime.today().weekday() < 5
