# -*- coding: utf-8 -*-
"""
Created on Mon May 16 19:54:44 2022

@author: Omotade
"""
import requests
from datetime import datetime
from bs4 import BeautifulSoup
import csv
import os


def scrape():
    data = requests.get('https://www.coingecko.com/')
    soup = BeautifulSoup(data.content, 'html.parser')
    
    return soup

def get_coins(info={}):
    
    global cryptosoup
    
    cryptosoup = scrape()
    coinnames = cryptosoup.select('a.d-lg-none.font-bold.tw-w-12')
    coin_info = []
    for coin in coinnames:
        name = coin.text
        href = coin.get('href')
        
        if href is not None:
            href = href.strip().split('/')
            Name = href[-1].title()
            info = {'CoinName':Name}
            
        if name is not None:
            name = name.strip()
            info.update({'Coin':name})
            
       
        coin_info.append(info)

    return coin_info

def extract_coindata(coin_info=get_coins()):
    """Extracts the current price, 24thVolume and MarketCap
    returns a list of dictionaries where each dictionary is for each coin"""
    
    now = datetime.now()
    coinprices = cryptosoup.select('span.no-wrap')

    prices = []
    for price in coinprices:
        coinprice = price.text
        if coinprice is not None:
            coinprice = coinprice.strip()

            prices.append(coinprice)
    start = 0
    for i in range(len(prices)//3):
        stop = (i+1) * 3

        # Getting prices in groups of threes: This contain the current price, 24thvolume and Market cap
        coin_prices = prices[start:stop]

        # get each categoy of prices on the page for each coin
        current = coin_prices[0]
        

        # make sure the next start point picks up at the previous stop point
        start = stop
        
        
        time = now.strftime('%Y/%m/%d/%H:%M')
        time = datetime.strptime(time, '%Y/%m/%d/%H:%M')
        info = {'Time':time,'Price':current,'Website':'https://www.coingecko.com/'}
        
        coin_info[i].update(info)
        
    return coin_info

def to_csv(columns, coindata):

    n = datetime.now()
    n = n.strftime('%H-%M')
    try:
        os.mkdir('{}'.format(n))
    except FileExistsError:
        pass
    
    path = './'+ n + '/crypto.csv'
    with open(path, 'w', newline='') as fp:
        dict_writer = csv.DictWriter(fp, columns)
        dict_writer.writeheader()
        dict_writer.writerows(coindata)