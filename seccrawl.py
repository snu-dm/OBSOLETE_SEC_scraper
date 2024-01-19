from SEC_scraper.crawler import SecCrawler
import pandas as pd


seccrawler = SecCrawler()
# seccrawler.filing_10K('MSFT','0000789019','20210719','2000000')

df = pd.read_csv("sp500.csv")

# print(df.head())

print(df.iloc[1,1])

for i in range(len(df.index)):
    cik = str('{num:010d}'.format(num=df.iloc[i,1]))
    # CIK number is a unique ten digit number we assign to companies that file with the SEC.
    ticker = str(df.iloc[i,0])
    seccrawler.filing_10K(ticker, cik,'20210719','2000000')

#MCHP