import requests
from bs4 import BeautifulSoup
from datetime import datetime


def get_top20_list():
    nv_src = requests.get('https://www.naver.com').text
    result = BeautifulSoup(nv_src, "html.parser").find("ul", class_="ah_l").find_all("li", {"class": "ah_item"})

    return list(map(lambda data: data.find("span", class_="ah_k").text, result))


def search_sections(keyword):
    headers = {"user-agent": "Mozilla/5.0"}
    nv_src = requests.get('https://search.naver.com/search.naver?query=' + keyword, headers=headers).text
    sections = BeautifulSoup(nv_src, "html.parser").find_all("ul", {"class": "type01"})

    result = set()

    for section in sections:
        dl = section.find_all("dl")
        dt = [item.text.strip() for item in list(map(lambda x: x.find('dt'), dl)) if item is not None]
        dd = [item.text.strip() for item in list(map(lambda x: x.find_all('dd')[-1], dl)) if item is not None]

        dt_len = len(dt)
        dd_len = len(dl)

        for i in range(0, max(dt_len, dd_len)):
            data = (dt[i] if i < dt_len else '', dd[i] if i < dd_len else '')
            result.add(data)

    return {keyword: list(result)}


def get_result(top20_list):
    yyyyMMddHHmm = datetime.now().strftime("%Y%m%d%H%M")
    return {yyyyMMddHHmm: list(map(lambda kwd: search_sections(kwd), top20_list))}
