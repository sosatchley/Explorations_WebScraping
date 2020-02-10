from bs4 import BeautifulSoup
import requests
import sys
import io

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')

domain = "https://www.pinterest.com/"
page = "sosatchley/christmas-party/"

url = "https://www.sex.com"


response = requests.get(url, timeout=5)
content = BeautifulSoup(response.content, "html.parser")

# print("Status Code: " + str(response.status_code))
# print("Text: \n" + response.text)
# if "blocked" in response.text:
#     print("We've been blocked")
# print("Headers: " + response.headers.get("content-type", "unknown"))
# Yl- MIw Hb7
i = 0
for pin in content.findAll('div', attrs={"class": "masonry_box small_pin_box"}):
    print(i)
    i += 1
