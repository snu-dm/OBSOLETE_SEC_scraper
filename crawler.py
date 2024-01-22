# This script will download all the 10-K, 10-Q and 8-K
# provided that of company symbol and its cik code.

from bs4 import BeautifulSoup
import random
import requests
import os
import time

class SecCrawler():

	def __init__(self):
		self.hello = "Welcome to SEC Cralwer!"

	def make_directory(self, companyCode, cik, filing_type, folder_name):
		# Making the directory to save comapny filings
		if not os.path.exists(f"{folder_name}"):
			os.makedirs(f"{folder_name}")
		if not os.path.exists(f"{folder_name}/{companyCode}/"):
			os.makedirs(f"{folder_name}/{companyCode}/")
		if not os.path.exists(f"{folder_name}/{companyCode}/{cik}/"):
			os.makedirs(f"{folder_name}/{companyCode}/{cik}/")
		if not os.path.exists(f"{folder_name}/{companyCode}/{cik}/{filing_type}/"):
			os.makedirs(f"{folder_name}/{companyCode}/{cik}/{filing_type}/")

	def save_in_directory(self, companyCode, cik, docList, docNameList, filing_type, folder_name):
		# Save every text document into its respective folder
		for j in range(len(docList)):
			base_url = docList[j]
			print(base_url)
			headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
			r = requests.get(base_url, headers = headers)
			data = r.text

			path = f"{folder_name}/{companyCode}/{cik}/{filing_type}/{str(docNameList[j])}"
			print(f"saving to {path}")
			filename = open(path,"wb")
			filename.write(data.encode('ascii', 'ignore'))
			time.sleep(random.uniform(1, 3))

	def filing_10K(self, companyCode, cik, priorto, count, folder_name):
		try:
			self.make_directory(companyCode, cik, '10-K', folder_name)
		except:
			print("Not able to create directory")

		#generate the url to crawl
		base_url = f"http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK={cik}&type=10-K&dateb={priorto}&owner=exclude&output=xml&count={count}"
		print(f"started 10-K for code: {companyCode}")
		headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:88.0) Gecko/20100101 Firefox/88.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8"}
		headers = {"User-Agent": "5yoondori@snu.ac.kr"}

		r = requests.get(base_url, headers = headers)
		data = r.text

		time.sleep(random.uniform(1, 3))

		soup = BeautifulSoup(data, features = "lxml") # Initializing to crawl again
		linkList=[] # List of all links from the CIK page
		# If the link is .htm convert it to .html
		for filing in soup.find_all('filing'):
			type_tag = filing.find('type')
			link_tag = filing.find('filinghref')

			# only search for 10-K, not for 10-K/A
			if type_tag.string == "10-K":
				URL = link_tag.string
				if link_tag.string.split(".")[len(link_tag.string.split("."))-1] == "htm":
					URL += "l"
				linkList.append(URL)

		print(f"Number of files to download : {len(linkList)}")
		print("Start downloading....")

		docList = [] # List of URL to the text documents
		docNameList = [] # List of document names

		for k in range(len(linkList)):
			requiredURL = str(linkList[k])[0:len(linkList[k])-11]
			txtdoc = requiredURL+".txt"
			docname = txtdoc.split("/")[len(txtdoc.split("/"))-1]
			docList.append(txtdoc)
			docNameList.append(docname)

		print(docNameList)
		try:
			self.save_in_directory(companyCode, cik, docList, docNameList, '10-K', folder_name)
		except:
			print("Not able to save the file :( ")

		print(f"Successfully downloaded all {len(linkList)} files")