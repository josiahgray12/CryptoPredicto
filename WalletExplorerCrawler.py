from bs4 import BeautifulSoup
import requests
import urllib
import urllib2
import urllib3
import pprint

for i in range(1965, 117509):
    url = 'https://www.walletexplorer.com/wallet/00000014ea8b260f/addresses'
    if i > 0:
        url = url + "?page=" + str(i + 1)
    r = requests.get(url)
    r_HTML = r.text
    soup = BeautifulSoup(r_HTML, "html.parser")

    rawList = []

    for string in soup.strings:
        if len(string) > 29 and len(string) < 39:
            rawList.append(string)
    del rawList[0]
    del rawList[len(rawList) - 1]

    

    file = open("GDAXaddressPage" + str(i+1) + ".txt" , "w")
    file.write("Page " + str(i+1) + " of GDAX addresses:\n\n")
    for item in rawList:
        file.write(item + "\n")
    file.close()


