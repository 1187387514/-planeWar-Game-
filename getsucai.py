import requests
from bs4 import BeautifulSoup as bs
import traceback
import urllib

def gethtml(url):
    try:
        header = {'user-agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.90 Safari/537.36'}
        r = requests.get(url,headers = header)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        html = r.text
        return html
    except:
        print('gethtml fail ')
        traceback.print_exc()

def geturl(html):
    try:
        soup = bs(html,"html.parser")
        urls = soup.find_all(attrs = {'class':"image-view"})
        titles = soup.find_all(class_='image-caption')
        turls = zip(titles,urls)
        print(turls)
        photoUrls = []
        for url in turls:
            photoUrls.append((url[0].string,url[1].img.attrs['data-original-src']))
        return photoUrls

    except:
        print('获取url失败')
        traceback.print_exc()

def download(urls):
    for url in urls:
        print('https:'+url[1])
        urllib.request.urlretrieve('https:'+url[1],filename="D:\python\飞机大战\data\{title}".format(title=url[0]),reporthook=loading)

def loading(blocknum,blocksize,totalsize):
    percent=int(100*blocknum*blocksize/totalsize)
    if percent>100:
        percent=100
    print("正在下载>>>{}%".format(percent))
    import time
    time.sleep(0.5)



def main():
    html = gethtml('https://www.jianshu.com/p/0993c99f6000')
    print(html)
    photoUrls = geturl(html)
    print(photoUrls)
    download(photoUrls)

main()
