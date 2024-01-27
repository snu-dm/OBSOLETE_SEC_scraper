from sec_utils import *
import pandas as pd
import argparse

def main(args):
    seccrawler = SecCrawler()
    # seccrawler.filing_10K('MSFT','0000789019','20210719','2000000')
    dataList = seccrawler.filing_10K(args.ticker, args.cik,'20240127', 10)

    print(f"num: {len(dataList)}")
    print(dataList[0][:1500])

    return dataList

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('ticker', type=str)
    parser.add_argument('cik', type=str)
    args = parser.parse_args()

    main(args)