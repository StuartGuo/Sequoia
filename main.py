# -*- encoding: UTF-8 -*-

import process
import strategy.enter as enter
import strategy.low_atr as low_atr
import utils
import logging
import schedule
import time
import tushare as ts
import pandas as pd
import datetime


logging.basicConfig(format='%(asctime)s %(message)s', filename='sequoia.log', level=logging.DEBUG)
UPDATE_TIME="16:00"
EXEC_TIME="19:00"
ALL_PATH='config/Astock.xlsx'

    
def strategy(end_date=None):
    def end_date_filter(code_name):
        stock = code_name[0]
        name = code_name[1]
        data = utils.read_data(stock, name)
        if data is None:
            return False
        return enter.check_volume(code_name, data, end_date=end_date)
    # low_atr.check_low_increase(stock, data)
    return end_date_filter


def dailyjob():
    print("***I am going to calculate the best stocks***")
    if utils.is_weekday():
        logging.info("*********************************************************************")
        process.run()

        stocks = utils.get_stocks()

        m_filter = strategy(end_date=None)

        results = list(filter(m_filter, stocks))
        logging.info('选股结果：{0}'.format(results))
        logging.info("*********************************************************************")
    print("<<<<I have finished my dailyjob,and am going to sleep Zzz~>>>>")

def dailyjob2updateall():
    print("***I am going to update the whole stocks info***")
    ts.set_token('03ce2b42ef7900ecbbbf4b78fae53b675a9477bc98ff937215b17df1')
    pro=ts.pro_api()
    data = pro.query('stock_basic',exchange='',list_status='L',fields='ts_code,symbol,name,area,industry,list_date')
    data['trade_date']= datetime.datetime.now().strftime('%Y%m%d')
    data['close']=0
    data['turnover_rate']=0
    data['turnover_rate_f']=0
    data['volume_ratio']=0
    data['pe']=0
    data['pe_ttm']=0
    data['pb']=0
    data['ps']=0
    data['ps_ttm']=0
    data['total_share']=0
    data['float_share']=0
    data['free_share']=0
    data['total_mv']=0
    data['circ_mv']=0
                    
    db=pro.query('daily_basic', ts_code='', trade_date=datetime.datetime.now().strftime('%Y%m%d'))
    
    for index,row in data.iterrows():
        ts_code=row['ts_code']
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
        for indexi,rowi in db.iterrows():
            ts_codei=rowi['ts_code']
            if ts_codei==ts_code:
                print("%s updated" % ts_codei)
                close=rowi['close']
                turnover_rate=rowi['turnover_rate']
                turnover_rate_f=rowi['turnover_rate_f']
                volume_ratio=rowi['volume_ratio']
                pe=rowi['pe']
                pe_ttm=rowi['pe_ttm']
                pb=rowi['pb']
                ps=rowi['ps']
                ps_ttm=rowi['ps_ttm']
                total_share=rowi['total_share']
                float_share=rowi['float_share']
                free_share=rowi['free_share']
                total_mv=rowi['total_mv']
                circ_mv=rowi['circ_mv']
                
                data.loc[index,'close']=close
                data.loc[index,'turnover_rate']=turnover_rate
                data.loc[index,'turnover_rate_f']=turnover_rate_f
                data.loc[index,'volume_ratio']=volume_ratio
                data.loc[index,'pe']=pe
                data.loc[index,'pe_ttm']=pe_ttm
                data.loc[index,'pb']=pb
                data.loc[index,'ps']=ps
                data.loc[index,'ps_ttm']=ps_ttm
                data.loc[index,'total_share']=total_share
                data.loc[index,'float_share']=float_share
                data.loc[index,'free_share']=free_share
                data.loc[index,'total_mv']=total_mv
                data.loc[index,'circ_mv']=circ_mv		
        
    data.to_excel('config/Astock.xlsx', encoding='utf-8', index=False, header=True)

    print("Successfully get stock info!Enter sleep!")

#schedule.every().saturday.at("09:15").do(weeklyjob)
schedule.every().day.at(UPDATE_TIME).do(dailyjob2updateall)
schedule.every().day.at(EXEC_TIME).do(dailyjob)

while True:
    schedule.run_pending()
    time.sleep(1)