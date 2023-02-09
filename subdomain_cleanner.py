


import requests

infileName='subdomains_2023_01_27_04_23_32.txt'
# infileName='t.txt'
infile=open(infileName,'r')


subdomains=[]

import re


for subdomain in infile:

    burp0_url = "http://{}/".format(subdomain.replace('\n',''))
    burp0_headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8", "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2", "Accept-Encoding": "gzip, deflate", "Connection": "close", "Upgrade-Insecure-Requests": "1"}


    try:
        resp=requests.get(burp0_url, headers=burp0_headers,allow_redirects=False)
    except:
        continue

    if resp.status_code in [410,400,500,501,502,503,504]:
        continue
    if resp.status_code == 301:

        newUrl = resp.headers['location']
        if 'https' in newUrl:
            matchObj = re.match(r'https://(.*?)/', newUrl)
        else:
            matchObj = re.match(r'http://(.*?)/', newUrl)
        s=matchObj.group(1)
        # if s is None:
            # print(burp0_url)
        subdomains.append(s.replace('\n',''))
        continue
    subdomains.append(subdomain.replace('\n',''))


infile.close()

import datetime
timeStick = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
# OutputfileName="subdomains_cleaned_{}.txt".format(timeStick)
OutputfileName="t2.txt"
ofile=open(OutputfileName,'w')

# deduplication
def Deduplication(lst1):
    lst2 = sorted(set(lst1), key=lst1.index)
    return lst2
subdomains_new=Deduplication(subdomains)


# print(subdomains_new)
for i in subdomains_new:
    ofile.write(i+'\n')
ofile.close()


