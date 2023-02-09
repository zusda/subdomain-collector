from urllib.parse import quote
import re
import urllib.parse as urlparse
import requests



class EnumGoogle():
    def __init__(self,domain):
        self.domain=domain


    def generate_query(self,domain):
        query = "site:{domain} -www.{domain}".format(domain=domain)
        return query

    def extract_domains(self,resp):

        subdomain = []
        link_regx = re.compile('<cite.*?>(.*?)<\/cite>')

        links_list = link_regx.findall(resp)
        for link in links_list:
            # print(link)
            link = re.sub('<span.*>', '', link)

            if not link.startswith('http'):
                link = "http://" + link
            subdomain.append(urlparse.urlparse(link).netloc)

        return subdomain

    def run(self,page_no=1):
        base_url = "https://www.google.com/search?q={query}&start={page_no}"
        query = self.generate_query(self.domain)
        url = base_url.format(query=quote(query), page_no=page_no)

        print(url)

        proxies = {
            'http': 'http://127.0.0.1:7890',
            'https': 'http://127.0.0.1:7890',
        }


        session = requests.Session()
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.8',
            'Accept-Encoding': 'gzip',
        }
        timeout = 25

        resp = session.get(url, headers=headers, timeout=timeout, proxies=proxies)
        subdomain = self.extract_domains(resp.text)

        # for i in subdomain:
        #     print(i)
        return subdomain




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


    subdomains=[]

    t=EnumGoogle(domain)
    for i in range(10):
        temp = t.run(page_no=i)
        subdomains.extend(temp)

    # print(subdomains)
    # print(len(subdomains))

    def Deduplication(lst1):
        lst2 = sorted(set(lst1), key=lst1.index)
        return lst2


    Deduplication_subdomains = Deduplication(subdomains)
    # print(Deduplication_subdomains)

    fo = open("google_subdomains.txt", "w")
    for i in Deduplication_subdomains:
        fo.write(i+"\n")



    fo.close()

