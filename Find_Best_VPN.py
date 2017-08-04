#!/usr/bin/python3
from urllib.request import urlopen
from bs4 import BeautifulSoup

import shlex
import subprocess
import sys

def ping_ip(ip):

    # Tokenize the shell command
    cmd = shlex.split("ping -c1 -w1 " + str(ip))
    try:
        output = subprocess.check_output(cmd)
    except subprocess.CalledProcessError as e:
        # print("The IP {0} is NotReacahble".format(cmd[-1]))
        return 1,0;
    else:
        returns = str(output)
        indexBegin = returns.find("time=")
        indexEnd = returns.find("ms")

        time = float(returns[indexBegin+5:indexEnd-1])
        # print(output)
        return (0,time);
        # print("The IP  is Reachable",ip)


def main():
    argc = sys.argv.__len__()
    if argc < 2:
        print("Usage : python3 getip.py [url]")
        return

    url = sys.argv[1]
    html = urlopen(str(url))
    # html = urlopen("http://www.pythonscraping.com/pages/warandpeace.html")
    # html = urlopen("http://www.baidu.com")
    # html = urlopen("http://p79027972.chibnt01.ap.so-net.ne.jp:48346/en/")
    bsObj = BeautifulSoup(html, "lxml");
    # print(bsObj.title)
    # nameList = bsObj.findAll("span",{"class":"green"});
    nameList = bsObj.findAll("span",{"style":"font-size: 12pt;"});
    print("Find ",nameList.__len__(),"ip in ",sys.argv[1])

    ip_usable = 0;
    ip_best = ""
    time_best = 500
    index = 1
    for name in nameList:
        print("try index : ",index)
        index = index + 1
        ip_usable,time = ping_ip(name.get_text())
        if ip_usable == 0:
            if time<time_best:
                time_best = time
                ip_best = name.get_text()

    if ip_best != "":
        print("find best usable ip : ", ip_best)
        print("time : ", time_best)
    else:
        print("Program fishinged, there are no ip useable.")

if __name__ == '__main__':
    main()
