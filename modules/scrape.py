import requests
import re
import csv
from bs4 import BeautifulSoup
import time
import sys


def scrape(proxy):
    
    proxy = 'https://' + proxy

    # Read the CSV file in (skipping first row).
    csvList = open('./csv/productLinks.csv')
    productList = csv.reader(csvList, delimiter='|')

    headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'}

    proxies = {
        'http': 'http://93.188.161.129:8080',
    }

    # If an https proxy is provided, use it    
    if proxy != 'https://Please enter a proxy':
        proxies['https'] = proxy
    else:
        sys.exit('GSA may blacklist your IP address without providing an https proxy: program will now exit.')        

    # Setup to write to a new csv file
    outputfile = open('./csv/final.csv', 'a', newline='')
    outputwriter = csv.writer(outputfile, delimiter=';')

    # Loops through each product row in the csv
    for product in productList:
        print(product)
        prodname = product[0]
        prodUrls = product[1].split('`')

        print(prodname)

        # Loops through each link... while keeping the same prodname.
        if 'No results found' not in prodUrls[0]:
            for link in prodUrls:
                print(link)
                res = requests.get(link, proxies=proxies, headers=headers, timeout=None)
                soup = BeautifulSoup(res.text, 'html.parser')

                pricingTable = soup.findAll(attrs={
                    'width': "100%",
                    'border': "0",
                    'cellpadding': "0",
                    'cellspacing': "0",
                    'class': 'greybox'
                })[0]

                nameTable = soup.findAll(attrs={
                    'width': "100%",
                    'border': "0",
                    'cellspacing': "0",
                    'cellpadding': "0",
                    'class': "black8pt"
                })

                moreSpecs = soup.findAll(attrs={
                    'width': "100%",
                    'border': "0",
                    'cellspacing': "0",
                    'cellpadding': "1",
                    'class': "black8pt"
                })

                # Spects/Description tabs
                specsTab = ''
                additionalDesc = ''

                descTable = soup.findAll(id='TabbedPanels1')
                tabPanelLabels = descTable[0].ul.findAll('li')

                if len(descTable) > 0:
                    if len(descTable[0].select('.comment')) > 0:
                        additionalDesc = descTable[0].select('.comment')
                    tabPanelContent = descTable[0].select(
                        ".TabbedPanelsContent table")

                # # if spec box exists
                if len(tabPanelContent) > 1:
                    speclist = tabPanelContent[1].findAll('tr')
                else:
                    speclist = []

                if len(speclist) > 0:
                    for spec in speclist:
                        specs = spec.findAll('td')
                        if len(specs) > 1:
                            for i, v in enumerate(specs):
                                if i == 1:
                                    specsTab += v.get_text() + '. '
                                else:
                                    specsTab += v.get_text() + ': '

                # # Product Attributes
                productName = nameTable[1].strong.string.replace(';', ' ')

                trs = pricingTable.findAll('tr')

                if type(additionalDesc) == list:
                    if type(additionalDesc[0]) != str:
                        outputwriter.writerow([
                            'prodNum', 'productName', 'prodUrl', 'specsTab', 'additionalDesc'
                        ])
                        outputwriter.writerow([
                            prodname, productName, link, specsTab, additionalDesc[0].get_text(
                            ).strip()
                        ])
                else:
                    outputwriter.writerow([
                        'prodNum', 'productName', 'prodUrl', 'specsTab'
                    ])
                    outputwriter.writerow([
                        prodname, productName, link, specsTab
                    ])

                for i, row in enumerate(trs):

                    # pricing table rows
                    test = row.select('td')
                    test2 = row.select('th')

                    ourList = []
                    our2List = []

                    vendorList = []
                    vendorIndex = []
                    count = 0

                    for e, v in enumerate(test):
                        if i == 0:
                            if len(ourList) > 0 and e > 1:
                                if v.get_text().strip() == ourList[-1]:
                                    break
                            if v.get_text().strip() == 'Price/Unit':
                                ourList.append('Price')
                                ourList.append('')
                                ourList.append('Unit')
                            elif v.get_text().strip() == 'Features':
                                ourList.append('Features')
                                ourList.append('')
                                break
                            else:
                                ourList.append(v.get_text().strip())

                        elif v.img != None:
                            if v.img['alt'].strip() != '':
                                ourList.append(v.img['alt'].strip())
                        else:
                            if '&nbsp;' not in v.get_text().strip():
                                ourList.append(v.get_text().strip())

                            # if we find links in this tr and it contains catalog (vendor link)
                            if len(v.select('font[size="2"] a')) > 0:
                                if 'catalog' in v.select('font[size="2"] a')[0].get('href'):
                                    newlink = 'https://www.gsaadvantage.gov' + v.select('font[size="2"] a')[
                                        0].get('href')

                                    if newlink != None:
                                        
                                        res2 = requests.get(
                                            newlink, proxies=proxies, headers=headers, timeout=None)
                                        soup2 = BeautifulSoup(res2.text, 'html.parser')

                                        nameTable2 = soup2.findAll(attrs={
                                            'width': "100%",
                                            'border': "0",
                                            'cellspacing': "0",
                                            'cellpadding': "0",
                                            'class': "black8pt"
                                        })

                                        moreSpecs2 = soup2.findAll(attrs={
                                            'width': "100%",
                                            'border': "0",
                                            'cellspacing': "0",
                                            'cellpadding': "1",
                                            'class': "black8pt"
                                        })

                                        # Spects/Description tabs
                                        specsTab2 = ''
                                        additionalDesc2 = ''

                                        descTable2 = soup2.findAll(
                                            id='TabbedPanels1')

                                        if len(descTable2) > 0:
                                            tabPanelLabels2 = descTable2[0].ul.findAll(
                                                'li')
                                            if len(descTable2[0].select('.comment')) > 0:
                                                additionalDesc2 = descTable2[0].select(
                                                    '.comment')
                                            tabPanelContent2 = descTable2[0].select(
                                                ".TabbedPanelsContent table")
                                            tabPanelContent3 = descTable2[0].select(
                                                ".TabbedPanelsContentGroup td div")
                                            our2List.append(newlink)
                                            for div in tabPanelContent3:
                                                our2List.append(
                                                    div.get_text().strip())
                                            if len(additionalDesc2) > 0:
                                                our2List.append(
                                                    additionalDesc2[0].get_text().strip())

                                        # # if spec box exists
                                        if tabPanelContent2:
                                            if len(tabPanelContent2) > 1:
                                                speclist2 = tabPanelContent2[1].findAll(
                                                'tr')
                                            else:
                                                speclist2 = []

                                        if len(speclist2) > 0:
                                            for spec in speclist2:
                                                specs = spec.findAll('td')
                                                if len(specs) > 1:
                                                    for i, v in enumerate(specs):
                                                        if i == 1:
                                                            specsTab2 += str(v.string) + \
                                                                '. '
                                                        else:
                                                            specsTab2 += str(v.string) + \
                                                                ': '
                                            our2List.append(
                                                specsTab2)

                    for e, v in enumerate(test2):
                        if i == 0:
                            if v.get_text().strip() == 'Contractor':
                                count = e
                            our2List.append(v.get_text().strip())
                            our2List.append('')

                    ourList[0] = prodname
                    
                    if len(ourList) > 0:
                        outputwriter.writerow(ourList + our2List)
                    else:
                        continue

        else:
            outputwriter.writerow([prodname, 'No results found.'])

    outputfile.close()
    sys.exit('Complete')