import pandas as pd
import datetime
import requests
from requests.exceptions import ConnectionError
from bs4 import BeautifulSoup
import os


def web_content_div(web_content, class_path, value):
    web_content_div = web_content.find_all('div', {'class': class_path})
    try:
        if value != 'None':
            spans = web_content_div[0].find_all(value)
            texts = [span.get_text() for span in spans]
        else:
            text = web_content_div[0].get_text("|", strip=True)
            text = text.split("|")
            texts = text[-1]
    except IndexError:
        texts = []
    return texts

def real_time_price(stock_code):
    Error = 0
    url = f"https://finance.yahoo.com/quote/{stock_code}?p={stock_code}&.tsrc=fin-srch"
    try:
        r = requests.get(url)
        web_content = BeautifulSoup(r.text, 'lxml')
        texts = web_content_div(web_content, 'D(ib) Mend(20px)', 'fin-streamer')
        

        if texts != []:
            price, change = texts[0], texts[1] + ' ' + texts[2]
        else:
            Error = 1
            price, change = [],[]

        if stock_code [-2:] == '=F':
            texts = web_content_div(web_content, '"D(ib) W(1/2) Bxz(bb) Pstart(12px) Va(t) ie-7_D(i) ie-7_pos(a)\
                 smartphone_D(b) smartphone_W(100%) smartphone_Pstart(0px) smartphone_Bdb smartphone_Bdc($seperatorColor)",', 'fin-streamer')
        else:
            texts = web_content_div(web_content, '"D(ib) W(1/2) Bxz(bb) Pend(12px) Va(t) ie-7_D(i) smartphone_D(b)\
                 smartphone_W(100%) smartphone_Pstart(0px) smartphone_Bdb smartphone_Bdc($seperatorColor)"', 'fin-streamer')

        if texts != []:
            volume = texts[0]
        else:
            Error = 2
            volume = []

        # 1 year target
        texts = web_content_div(web_content, '"D(ib) W(1/2) Bxz(bb) Pstart(12px) Va(t) ie-7_D(i) ie-7_Pos(a)\
             smartphone_D(b) smartphone_W(100%) smartphone_Pstart(0px) smartphone_BdB smartphone_Bdc($seperatorColor)"', 'None')
        
        if texts != []:
            if stock_code [-2:] == '=F':
                one_year_target = []
            else:
                one_year_target = texts
        else:
            Error = 3
            one_year_target = []

        
    except ConnectionError:
        price, change, volume, latest_pattern, one_year_target = [],[],[],[],[]
        Error = 1
        print('Connection Error')

    latest_pattern = []
    return price, change, volume, latest_pattern, one_year_target, Error

Stock = ['ES=F', 'AAPL']

while True:
    info = []
    time_stamp = datetime.datetime.now() - datetime.timedelta(hours=12)
    time_stamp = time_stamp.strftime("%Y-%m-%d %H:%M:%S")
    for stock_code in Stock:
        stock_price, change, volume, latest_pattern, one_year_target, Error = real_time_price(stock_code)
        info.append(stock_price)
        info.extend([change])
        info.extend([volume])
        info.extend([latest_pattern])
        info.extend([one_year_target])

    if Error != 0:
        print()

    col = [time_stamp]
    col.extend(info)
    df = pd.DataFrame(col)
    df = df.T
    '''path = "/Users/USERNAME/Desktop/Python/Launchpad/"
    path += str(time_stamp[0:11] + 'stock data.csv')
    df.to_csv(path, mode = 'a', header = False)'''
    
    df.to_csv(time_stamp[0:11] + 'stock data.csv', mode = 'a', header = False)
    print(col)