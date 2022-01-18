import re
import requests
import pandas as pd
head=("股票名字","今日开盘价","昨日收盘价","当前价格","今日最高价",
        "今日最低价","竞买价","竞卖价","成交的股票数","成交金额",
        "买一","买一报价","买二","买二报价","买三",
        "买三报价","买四","买四报价","买五","买五报价",
        "卖一","卖一报价","卖二","卖二报价","卖三","卖三报价",
        "卖四","卖四报价","卖五","卖五报价")
def getempframe():
    return pd.DataFrame(columns=head)
def getdata(code):
    page=requests.get("http://hq.sinajs.cn/list="+code)
    stock_info=re.split(',|"|=',page.text)[2:34]
    return (pd.to_datetime("{date} {time}".format(date=stock_info[-2],time=stock_info[-1])),
            stock_info[0:-2])
def adddata(data,frame):
    frame.loc[data[0]]=data[1]