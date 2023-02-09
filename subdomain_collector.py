


'''

python3 subdomain_collector.py -d iculture.cc -o result.txt
'''


import time
import re
import datetime
import os
import requests

def esd_deali():
    kfile=open('esd_subdomain.txt','r+')
    ofile = open('esd_subdomain_tmp.txt','w')
    for line in kfile:
        subdomain_tmp=line.split(' ')[0]
        if subdomain_tmp:
            ofile.write(subdomain_tmp+'\n')

    kfile.close()
    ofile.close()
    os.system("mv esd_subdomain_tmp.txt esd_subdomain.txt")
def Deduplication(fileName):
    subdomains=[]
    file_subdomains=open(fileName,'r')
    for line in file_subdomains:
        subdomains.append(line)
    print(len(subdomains))
    file_subdomains.close()
    lst2 = sorted(set(subdomains), key=subdomains.index)
    return lst2
def subdomain_aliveTest(in_subdomains):
    subdomains=[]
    for subdomain in in_subdomains:

        burp0_url = "http://{}/".format(subdomain.replace('\n', ''))
        burp0_headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/109.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
            "Accept-Encoding": "gzip, deflate", "Connection": "close", "Upgrade-Insecure-Requests": "1"}

        try:
            resp = requests.get(burp0_url, headers=burp0_headers, allow_redirects=False)
        except:
            continue

        if resp.status_code in [410, 400, 500, 501, 502, 503, 504]:
            continue
        if resp.status_code == 301:

            newUrl = resp.headers['location']
            if 'https' in newUrl:
                matchObj = re.match(r'https://(.*?)/', newUrl)
            else:
                matchObj = re.match(r'http://(.*?)/', newUrl)
            s = matchObj.group(1)
            # if s is None:
            # print(burp0_url)
            subdomains.append(s.replace('\n', ''))
            continue
        subdomains.append(subdomain.replace('\n', ''))
    return subdomains
def exec_kali(command):

    tmp = "gnome-terminal -- bash -c \"echo \\\"\nexecuting command: {cmd}\n\\\";{cmd};exec bash;\"".format(cmd=command)
    os.system(tmp)
def dealing(infile):
    time.sleep(2)
    os.system("cat {infile} >>{out}".format(infile=infile,out=OutputfileName))
    time.sleep(1)
    os.system("mv {infile} {infile}_".format(infile=infile))

    print('\r',end='')
    print("--------{} finished".format(infile.split('.')[0]))
def ksubdomain_deali():
    kfile=open('ksubdomain.txt','r+')
    ofile = open('ksubdomain_tmp.txt','w')
    for line in kfile:
        matchObj = re.match(r'(.*?) => (.*)', line)
        if matchObj:
            ofile.write(matchObj.group(1)+'\n')

    kfile.close()
    ofile.close()
    os.system("mv ksubdomain_tmp.txt ksubdomain.txt")

from optparse import OptionParser
if __name__ == '__main__':

    usage = "show something usefull"
    parser = OptionParser(usage)  # 带参的话会把参数变量的内容作为帮助信息输出
    parser.add_option("-d", "--domain", dest="domian", help="a domain")
    parser.add_option("-o", "--output", dest="outfile", help="save result to the file, default result.txt ",
                      default="result.txt")
    (options, args) = parser.parse_args()

    if options.domian is None:
        print('need a domain')
        exit()
    print('\n resualt save in {}\n'.format(os.getcwd()+'/'+options.outfile))

    domain=options.domian
    OutputfileName = options.outfile

    commands=[
        'esd -d {domain};mv /tmp/esd/.{domain}.esd ./esd_subdomain.txt',
        'ksubdomain e  -d {domain}  | tee ksubdomain.txt',
        'amass enum -v -d {domain} -o amass.txt -passive;mv amass.txt amass_subdomains.txt',
        'python3 EnumGoogle.py -d {domain}',
        'python3 subdomain_fofa.py -d {domain}'
    ]
    ofileName=[
        'amass_subdomains.txt_',
        'ksubdomain.txt_',
        'google_subdomains.txt_',
        'fofa_subdomains.txt_',
        'esd.txt_'
    ]

    os.system("rm amass_subdomains.txt ksubdomain.txt google_subdomains.txt fofa_subdomains.txt esd.txt 2>/dev/null")
    # execute all commands
    for i in commands:
        tmp_command = i.format(domain=domain)
        print(tmp_command)
        exec_kali(tmp_command)
    print("\n\n")

    # -----------------------------------------



    timeStick = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
    # OutputfileName="subdomains_{}.txt".format(timeStick)
    fo = open(OutputfileName, "w")

    finish=0
    runningtime=0


    print("start check result files")
    print("time: {}".format(datetime.datetime.now()))
    while True:

        if os.path.exists('amass_subdomains.txt'):
            dealing("amass_subdomains.txt")
            finish=finish+1

        if os.path.exists('ksubdomain.txt'):
            ksubdomain_deali()
            dealing("ksubdomain.txt")
            finish=finish+1

        if os.path.exists('google_subdomains.txt'):
            dealing("google_subdomains.txt")
            finish=finish+1

        if os.path.exists('fofa_subdomains.txt'):
            dealing("fofa_subdomains.txt")
            finish=finish+1

        if os.path.exists('esd_subdomain.txt'):
            esd_deali()
            dealing("esd_subdomain.txt")
            finish=finish+1

        print("\r Have been running for {}s\n".format(runningtime), end="")
        if finish==len(commands):

            print("all scripts finished")
            print("time: {}".format(datetime.datetime.now()))

            subdomains_deduplication=Deduplication(OutputfileName)
            subdomains=subdomain_aliveTest(subdomains_deduplication)
            print(len(subdomains))


            os.system('rm {}'.format(OutputfileName))


            ofile=open(OutputfileName,'a')


            for i in subdomains:
                ofile.write(i+'\n')
            ofile.close()


            os.system('rm *.txt_;rm ksubdomain.yaml')
            exit()




        runningtime=runningtime+30
        time.sleep(30)














