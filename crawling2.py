import requests, re, sys

page = 6
def crawling(url,f_path):
    global page
    headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}
    response = requests.get(url,headers=headers)
    response.encoding = response.apparent_encoding
    filename = f_path + ".html"
    with open(filename,'w',encoding="utf-8") as f:
        f.write(response.text)
    page += 1
    if page > 131:
        sys.exit
    nexturl = url[:len(str(page-1))]
    nexturl += str(page)
    f_path = f_path[:len(str(page-1))]
    f_path += "_"+str(page)
    crawling(nexturl,f_path)

if __name__ == "__main__":
    url = "https://anshun.esa.io/posts/6"
    filename = sys.argv[0]

    crawling(url,filename)