import requests
import re
import time
import json
from pathlib import Path
from bs4 import BeautifulSoup

ID = "10115236298"
GROUP_NAME = "tsubaki-factory"
THEME_URL = "https://ameblo.jp/tsubaki-factory/theme"

# 記事リストからブログURLを取得する
urls = []
article_urls_path = "resources/article_urls_" + ID + ".json"
if Path(article_urls_path).exists():
    with open(article_urls_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        if "urls" in data and len(data["urls"]) > 0:
            urls = list(data["urls"])

if len(urls) == 0:
    print("記事リストを取得します。")
    for i in range(1, 32):
        list_url = THEME_URL + str(i) + "-" + ID + ".html"
        print("LIST URL：", list_url)
        response = requests.get(list_url)
        html = response.content
        soup = BeautifulSoup(html, "html.parser")
        for articles in soup.find("ul", class_="skin-archiveList"):
            for a in articles.find_all(href=re.compile("/" + GROUP_NAME)):
                urls.append(a.get("href"))
        time.sleep(1)

    # 記事urlを保存
    urls = set(urls)
    data = {"urls": list(urls)}
    with open(article_urls_path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False)


# 記事のタイトルと本文を取得してまとめる
pages = []
for url in urls:
    print("Article URL：", url)
    url = "https://ameblo.jp" + url
    response = requests.get(url)
    html = response.content
    soup = BeautifulSoup(html, "html.parser")
    title = soup.find("h1", class_="skin-entryTitle").text
    lines = []
    for element in soup.find("div", class_="skin-entryBody").children:
        if element.string:
            lines.append(element.string.strip())

    pages.append(
        {
            "title": title,
            "url": url,
            "lines": lines,
        }
    )

    time.sleep(1)

# JSONにまとめる
print("Total Articles: ", len(pages))
data = {"pages": pages}
with open("resources/sample_" + ID + "_sb.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False)
