import requests, re, sys
from bs4 import BeautifulSoup

page = 1
def crawling(url,f_path):
    global page
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url,headers=headers)
    response.encoding = response.apparent_encoding
    filename = f_path + ".html"
    with open(filename,'w',encoding="utf-8") as f:
        f.write(response.text)
    html = open(filename,'r')
    soup = BeautifulSoup(html, "html.parser")
    for res in soup.find_all(class_="wpcr_inactive"):
        res_p = res.string
        if page < int(res_p):
                page += 1
                nexturl = url[:-1]
                nexturl += res_p
                f_path = f_path[:-2]
                f_path += "_"+res_p
                crawling(nexturl,f_path)

if __name__ == "__main__":
    url_positive = "http://meigen.keiziban-jp.com/ポジティブ?wpcrp=1"
    url_negative = "http://meigen.keiziban-jp.com/ネガティブ?wpcrp=1"
    filename = sys.argv[0]

    #crawling(url_positive,filename)
    crawling(url_negative,filename)