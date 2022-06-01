import urllib3
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from csv import writer
import csv
import pandas as pd

sess = requests.Session()

lst = [i for i in range(1,10)] #7 page

x = []

for n in lst:
    url = 'https://www.evdekieczanem.com/medikal--saglik?sayfa=' + str(n)
    res = sess.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    #print(soup.prettify())
    print(url)

    # Grab only the main content part of the page
    main_page = soup.find('div', {'class': 'ProductListContent'})
    # print(main_page)

    main_page_for_link = main_page.find_all('a', class_='detailLink detailUrl', href=True)
    for pr in main_page_for_link:
        pr_partial_link = "https://www.evdekieczanem.com/" + pr['href']
        pr_link = pr_partial_link
        print(pr_link)

        detail = sess.get(pr_link)
        soup_detail = BeautifulSoup(detail.text, 'html.parser')

        product_brand_1 = soup_detail.find(class_='right_line Marka')
        if product_brand_1 is not None:
            product_brand = product_brand_1.get_text().replace("\n", " ")
            product_brand = product_brand.strip()
            print(product_brand)

        product_name_1 = soup_detail.find(class_='ProductName')
        if product_name_1 is not None:
            product_name = product_name_1.get_text().replace("\n", " ").split("(")[0]
            product_name = product_name.strip()
            print(product_name)

        #product_barcode_1 = soup_detail.find(class_='fr col chbarcode')
        #if product_barcode_1 is not None:
            # product_barcode = product_barcode_1.next_element
            # print(product_barcode)

        pc1 = soup_detail.find(class_='proCategoryTitle categoryTitleText')
        if pc1 is not None:
            pc2 = pc1.get_text().replace("\n", " ")
            pc3 = pc2.split(sep=">")
            product_category = pc3[1].strip()
            product_subcategory = pc3[2].strip()
            print(product_category)
            print(product_subcategory)

        product_barcode_1 = soup_detail.find(class_='Formline', id='divBarkod')
        if product_barcode_1 is not None:
            product_barcode = product_barcode_1.get_text()
            product_barcode = product_barcode.replace("\n", " ")
            product_barcode = product_barcode.split(":")
            product_barcode = product_barcode[1].strip()
            # product_barcode = [int(i) for i in product_barcode.split() if i.isdigit()]
            # product_barcode = product_barcode[0]
            print(product_barcode)

        product_long_info = soup_detail.find(class_='urunTabAlt').get_text().replace("\n", " ").strip()
        print(product_long_info)


        product_picture_1 = soup_detail.find('img', class_='cloudzoom')
        if product_picture_1 is not None:
            product_picture_2 = product_picture_1['src']
            product_picture = "https://www.evdekieczanem.com/" + str(product_picture_2)
            print(product_picture)

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
        print('product_label: ', product_label) okey
        '''

        x.append({'url': url,
                    'pr_link': pr_link,
                    'product_brand': product_brand,
                    'product_name': product_name,
                    'product_category': product_category,
                    'product_subcategory': product_subcategory,
                    'product_picture': product_picture,
                    'product_long_info': product_long_info,
                    'product_barcode': product_barcode})

        df = pd.DataFrame(x)

        df.to_excel('evdekieczanem_medikal_saglik.xlsx', index=False)

        #file = open('vitaminler_denemelerrrr.csv', 'w', newline='', encoding='utf-8')
        #writer = csv.writer(file)
        #headers = ([url, pr_link, product_brand, product_name,
        #            product_main_category, product_category, product_subcategory, product_picture,
        #            product_long_info, product_label])
        #writer.writerow(headers)
        #file.close()m