import urllib3
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from csv import writer
import csv
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import warnings
warnings.filterwarnings(action='ignore')

sess = requests.Session()

lst = [i for i in range(1, 26)] #76 page

x = []

for n in lst:
    url = 'https://www.recete.com/vitaminler/?page=' + str(n)
    print(url)
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    #print(soup.prettify())

    # Grab only the main content part of the page
    main_page = soup.find('ul', {'class': 'emosInfinite ems-inline'})
    #print(main_page)


    main_page_for_link = main_page.find_all('div', {"class": "ems-prd-description-text uni", "id": "plhUrun_urunAciklama"})


    for pr in main_page_for_link:
        pr_partial_link = pr.next_element["href"]
        pr_link = pr_partial_link
        print(pr_link)

        detail = sess.get("https://www.recete.com/" + str(pr_link))
        product_url = "https://www.recete.com/" + str(pr_link)
        print(product_url)
        soup_detail = BeautifulSoup(detail.text, 'html.parser')

        product_brand_1 = soup_detail.find('div', class_='detailBrandLabel')
        if product_brand_1 is not None:
            product_brand = product_brand_1.text
            print(product_brand)

        product_name_1 = soup_detail.find(class_='emos_H1')
        if product_name_1 is not None:
            product_name = product_name_1.next_element
            print(product_name)

        product_barcode_1 = soup_detail.find(class_='ems-prd-dtlCode-akt')
        if product_barcode_1 is not None:
             product_barcode = product_barcode_1.next_element
             product_barcode = product_barcode.replace("\r", "")
             product_barcode = product_barcode.split(":")
             product_barcode = product_barcode[1].lstrip()
             #product_barcode = [int(i) for i in product_barcode.split() if i.isdigit()]
             #product_barcode = product_barcode[0]
             print(product_barcode)

        pc1 = soup_detail.find("li" , class_='navigasyonSeviye2', recursive=True)
        if pc1 is not None:
            pc1 = pc1.text
            product_main_category = pc1
            print(product_main_category)
        pc2 = soup_detail.find("li", class_='navigasyonSeviye3')
        if pc2 is not None:
            pc2 = pc2.text
            product_category = pc2
            print(product_category)
        pc3 = soup_detail.find("li", class_='navigasyonSeviye4')
        if pc3 is not None:
            pc3 = pc3.text
            product_subcategory = pc3
            print(product_subcategory)
        else:
            product_subcategory = None


        product_long_info = [x.get_text().replace("\n", " ") for x in soup_detail.find_all(class_='spanTabUrunAciklama')]
        product_long_info = ''.join(product_long_info)
        print(product_long_info)


        product_picture_1 = soup_detail.find('li', class_='swiper-slide')
        if product_picture_1 is not None:
            str_image = product_picture_1['data-thumb']
            product_picture = "https://www.recete.com" + str(str_image)
            print(product_picture)

        product_short_1 = soup_detail.find('div', class_='ems-prd-mini-description')
        if product_short_1 is not None:
            product_short_info = product_short_1.text
            print(product_short_info)


        '''
        print('product_link: ', pr_link) okey
        print('product_brand: ', product_brand) okey
        print('product_name: ', product_name) okey 
        print('product_barcode: ', product_barcode.text) okey
        print('product_main_category: ', product_main_category) okey
        print('product_category: ', product_category) okey
        print('product_subcategory', product_subcategory) okey
        print('product_picture: ', product_picture) okey
        print('product_short_info: ', product_short_info) yok
        print('product_long_info: ', product_long_info) okey
        print('product_label: ', product_label) yok
        '''

        x.append({  'url': url,
                    'product_url': product_url,
                    'product_brand': product_brand,
                    'product_name': product_name,
                    'product_main_category': product_main_category,
                    'product_category': product_category,
                    'product_subcategory': product_subcategory,
                    'product_barcode': product_barcode,
                    'product_picture': product_picture,
                    'product_short_info': product_short_info,
                    'product_long_info': product_long_info})

        df = pd.DataFrame(x)

        df.to_excel('recete_vitaminler.xlsx', index=False)

        #file = open('vitaminler_denemelerrrr.csv', 'w', newline='', encoding='utf-8')
        #writer = csv.writer(file)
        #headers = ([url, pr_link, product_brand, product_name,
        #            product_main_category, product_category, product_subcategory, product_picture,
        #            product_long_info, product_label])
        #writer.writerow(headers)
        #file.close()m