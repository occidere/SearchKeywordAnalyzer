import requests
from bs4 import BeautifulSoup


def get_top20_list():
    nv_src = requests.get('https://www.naver.com').text
    result = BeautifulSoup(nv_src, "html.parser").find("ul", class_="ah_l").find_all("li", {"class": "ah_item"})

    return list(map(lambda data: data.find("span", class_="ah_k").text, result))


def search_sections(keyword):
    headers = {"user-agent": "Mozilla/5.0"}
    nv_src = requests.get('https://search.naver.com/search.naver?query=' + keyword, headers=headers).text
    sections = BeautifulSoup(nv_src, "html.parser").find_all("ul", {"class": "type01"})

    print('keyword = ' + keyword)

    result = set()

    for section in sections:
        dl = section.find_all("dl")
        dt = [item.text.strip() for item in list(map(lambda x: x.find('dt'), dl)) if item is not None]
        dd = [item.text.strip() for item in list(map(lambda x: x.find_all('dd')[-1], dl)) if item is not None]

        dt_len = len(dt)
        dd_len = len(dl)
        size = max(dt_len, dd_len)

        for i in range(0, size):
            data = (dt[i] if i < dt_len else '', dd[i] if i < dd_len else '')
            result.add(data)

    return result


if __name__ == "__main__":
    top20_list = get_top20_list()
    print('top20 : ' + top20_list.__str__())
    result_list = list(map(lambda kwd: search_sections(kwd), top20_list))
    for topics in result_list:
        for topic in topics:
            print(topic)
