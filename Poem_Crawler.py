#coding=gbk
import requests
from bs4 import BeautifulSoup

cnt = 0
for i in range(1, 14):
    url = "https://www.shicimingju.com/shicimark/tangshisanbaishou_"+str(i)+"_0__1.html"
    r = requests.get(url)
    demo = r.text
    soup = BeautifulSoup(demo, "html.parser")
    html1 = soup.find_all(class_='shici_list_main')

    for text in html1:
        index = 0
        text = text.get_text().replace('\n', '').replace(' ', '').replace("收起", '').replace("展开全文", '').replace('/', '-')
        text = text.encode("GBK", "ignore")
        text = text.decode("GBK")
        cnt += 1
        # print(cnt, text)

        with open("dataset/" + str(cnt)+".txt", "w") as f:
             f.write(text)


