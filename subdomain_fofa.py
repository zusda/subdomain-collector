



import requests


import base64
import json

email = ""
key = ""
size = 1000
page = 1
headers = {'user-agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}

def subdomain_fofa(query_str):
    fofa_web_host_port = []  
    fofa_service_host_port = []     #

    qbase64 = str(base64.b64encode(query_str.encode(encoding='utf-8')), 'utf-8')
    if email=='' or key=='':
    	print('config your fofa email or key in subdomain_fofa.py')
    	return
    url = r'https://fofa.info/api/v1/search/all?email={}&key={}&qbase64={}&size={}&page={}&fields=host,title,ip,domain,port,server,protocol,city'.format(email, key, qbase64, size, page)

    # print(url)
    ret = json.loads(requests.get(url=url, headers=headers, timeout=10, verify=False).text)
    fofa_Results = ret['results']


    print("---------------------------------------------------------------------------------")

    hosts=[]
    for result in fofa_Results:
        host, title, ip, domain, port, server, protocol, address = result
        if domain != '':

            hosts.append(host)
    # print(hosts)

    subdomains=subdomain_clean(hosts)

    return subdomains
    # print(subdomains)




def subdomain_clean(hosts):
    subdomains=[]
    for i in hosts:
        if "http" in i:
            a=i.split('//')[1]
            subdomains.append(a)
        else:
            subdomains.append(i)
    return subdomains

if __name__ == '__main__':

    from optparse import OptionParser
    parser = OptionParser()
    parser.add_option("-d","--domain",dest="domain",help="need domain")
    (options,args)=parser.parse_args()
    if options.domain == None:
        print("need domain")
        exit()
    else:
        domain =options.domain

    subdomains = subdomain_fofa('domain="{}"'.format(domain))
    # print(subdomains)

    def Deduplication(lst1):
        lst2 = sorted(set(lst1), key=lst1.index)
        return lst2

    Deduplication_subdomains = Deduplication(subdomains)



    fo = open("fofa_subdomains.txt", "w")
    for i in Deduplication_subdomains:
        fo.write(i+"\n")


    fo.close()



