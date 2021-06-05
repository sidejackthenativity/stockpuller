import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
import time


def get_info(tickerSymbol):


    URL = 'https://finance.yahoo.com/quote/%s?p=%s' % (tickerSymbol, tickerSymbol)
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')
    print(tickerSymbol)
    closing = soup.find_all(class_="Trsdu(0.3s) Fw(b) Fz(36px) Mb(-4px) D(ib)")[0].get_text()
    attributes = soup.find_all(class_="Ta(end) Fw(600) Lh(14px)")
    previous_closing = attributes[0].get_text()
    pe_ratio = attributes[10].get_text()

    return closing, attributes, previous_closing, pe_ratio


def main():
    #Grab lines from the file, hard-coded for now
    filepath = 'tickerlist.txt'

    #column_names = ["ticker","date","previous close","closing","pe ratio"]

    df_ = pd.DataFrame(columns=["ticker","date","previous close","closing","pe ratio"])
    #df_ = df_.fillna(0) # with 0s rather than NaNs
    file = open(filepath,'r')

    for line in file:
        symbol = line.rstrip()
        closing, attributes, previous_closing, pe_ratio = get_info(symbol)
        date = datetime.datetime.now()

        df_ = df_.append({'ticker' : symbol, 'date' : date, 'previous close' : previous_closing, 'closing':closing, 'pe ratio' : pe_ratio},
                ignore_index = True)
        df_
        print(df_)
        time.sleep(1)

    file.close()

    df_.to_csv('stockData.csv')

main()
