from bs4 import BeautifulSoup
import requests
import shutil
import time
import sys
import io
import os

sys.stdout = io.TextIOWrapper(sys.stdout.detach(), encoding='utf-8')
sys.stderr = io.TextIOWrapper(sys.stderr.detach(), encoding='utf-8')
domain = "https://www.sex.com"
page = "/user/kollinz/pornstars/?page=2"
session = requests.Session()


def begin_session():
    session.headers.update({
        'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) \
                        AppleWebKit/537.11 (KHTML, like Gecko) \
                        Chrome/23.0.1271.64 Safari/537.11',
        'Accept': 'text/html,application/xhtml+xml,application/xml;\
                    q=0.9,image/webp,image/apng,*/*;\
                    q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
        'Accept-Encoding': 'gzip, deflate, br',
        'Accept-Language': 'en-US,en;q=0.8',
        'Connection': 'keep-alive',
        'Cookie': 'locale=en;\
                   _ga=GA1.2.342256780.1582442624; \
                   __auc=dc0ed33217070ee3542327f1fb2; \
                   _gid=GA1.2.958184418.1582595256; \
                   ad_float_vid=2; \
                   ad_float_vidblock=7; \
                   autologin_sex_sf=QXBwXE1vZGVsXFVzZXJNb2RlbDpjMjl6WVhSam\
                                    FHeGxlVUJuYldGcGJDNWpiMjA9OjE1ODMyNzkz\
                                    OTA6MmFmZDNhZTViMjY3Y2ZiMzVhMzRiOWM2Yz\
                                    k2MzE2NjI1NDBlMTQyZWY3NTEzZGVmYWMzZDlm\
                                    NjM4ZGQ1MGIzOQ%3D%3D; \
                   sess_sex=urj2c1s0991oha2s135avjjbjm; \
                   __asc=550a85df1707f1f6ca5bcbd38ed; _\
                   pk_id.1.bca8=2fa695d9495df3fb.1582442624.\
                                5.1582680731.1582680731.; \
                   _pk_ses.1.bca8=1',
        'Referer': 'https://www.sex.com'})
    return session


def make_soup(url):
    response = session.get(url, timeout=5)
    content = BeautifulSoup(response.content, "html.parser")
    return content


def find_images_on_page(content):
    titles = []
    urls = []
    srcs = []
    i = 0
    for pin_container in content.findAll(
            'div', attrs={"class": "masonry_box small_pin_box"}):
        pin_image = pin_container.find('img', attrs={"class": "image"})
        img_title = pin_image.get('alt')
        if (img_title == ""):
            img_title = i
        img_source = pin_image.get('data-src')
        titles.append(img_title)
        srcs.append(img_source)
        pin_link = pin_container.find('a', attrs={"class": "image_wrapper"})
        link_url = pin_link.get('href')
        urls.append(link_url)
    return (titles, srcs, urls)


def find_full_image(link):
    full_url = domain + link
    content = make_soup(full_url)
    image_frame = content.find('div', attrs={"class": "image_frame"})
    image = image_frame.find('img', )
    image_source = image.get('src')
    return(image_source)


def write_image_to_file(title, src):
    file_extension = src.split('.')[-1].split('?')[0]
    filename = ("{}\\{}.{}".format(os.getcwd(), title, file_extension))
    print("[INFO] Downloading \"{}\"".format(filename))
    r = session.get(src, stream=True)
    if r.status_code == 200:
        with open(filename, 'wb') as f:
            r.raw.decode_content = True
            shutil.copyfileobj(r.raw, f)
    else:
        print("{}[ERROR] \"{}\" download failed with status code {}{}"
              .format('\033[91m', filename, r.status_code, '\033[0m'))


def check_directory(page):
    current_directory = os.getcwd()
    # TODO: add forward-slash check on page, adjust index variable
    directory_name = page.split('/')[-2]
    target_directory = '{}\\{}'.format(current_directory, directory_name)
    if (os.path.exists(target_directory)):
        os.chdir(target_directory)
    else:
        os.mkdir(target_directory)
        os.chdir(target_directory)

def scrape_page(page):
    titles, srcs, urls = find_images_on_page(page)
    for i in range(len(titles)):
        write_image_to_file(titles[i], find_full_image(urls[i]))
        time.sleep(2)


def scrape_all_pages(start_page):
    current_page = start_page
    while(True):
        # scrape_page(current_page)
        # current_page = next_page(current_page)
        print(next_page(current_page))
        break


def next_page(page):
    pagination = page.find('div', attrs={'class': 'pagination'})
    print(pagination)
    for button in pagination.findAll('a', attrs="btn btn-default btn-2ndChance"):
        print(button.get_text())
        if button.get_text() == 'Next':
            return (domain + button.get('href'))
    print('Last Page Reached')


begin_session()
check_directory(page)
start_page = make_soup(domain + page)
scrape_all_pages(start_page)
# print("{}\n{}\n{}\n{}\n-----------------"
      # .format(titles[0], srcs[0], urls[0], find_full_image(urls[0])))


# for i in range(len(titles)):
#     print("{}\n{}\n{}\n------------------".format(titles[i], srcs[i], urls[i]))
# save_images_on_page(titles, urls)
