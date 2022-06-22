import requests
from bs4 import BeautifulSoup as bs
import pandas as pd

df = pd.DataFrame(columns=["公司代號", "公司簡稱", "發言日期", "發言時間", "主旨"])
url = "https://mops.twse.com.tw/mops/web/ajax_t05sr01_1"
page = requests.get(url)
soup = bs(page.text, features="html.parser")
table = soup.find("table", class_="hasBorder")
tr = table.find_all('tr')
# print(tr)
for series in tr[1:]:
    number = series.find("td").text
    name = series.find_all("td", style="text-align:left !important;")[0].text
    day = series.find_all("td", style="text-align:left !important;")[1].text
    time = series.find_all("td", style="text-align:left !important;")[2].text
    content = series.find_all("td", style="text-align:left !important;")[3].text.replace('\r\n', ' ')
    # print(content)
    series = pd.Series([number, name, day, time, content],
                       index=["公司代號", "公司簡稱", "發言日期", "發言時間", "主旨"])
    df = df.append(series, ignore_index=True)
df.to_csv('hw_2.csv', encoding="utf-8", index=False)
