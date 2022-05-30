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

lst = [i for i in range(1, 11)] #76 page

x = []

for n in lst:
    url = 'https://www.e-bebek.com/bebek-oyuncaklari-c3776/?page=' + str(n)
    print(url)
    browser = webdriver.Chrome(ChromeDriverManager().install())
    browser.get(url)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')
    #print(soup.prettify())

    # Grab only the main content part of the page
    main_page = soup.find('div', {'class': 'row m-md-0'})
    #print(main_page)


    main_page_for_link = main_page.find_all('a', class_='product-btn product-position', href=True)


    for pr in main_page_for_link:
        pr_partial_link = pr["href"]
        pr_link = pr_partial_link
        print(pr_link)

        detail = sess.get("https://www.e-bebek.com/" + str(pr_link))
        product_url = "https://www.e-bebek.com/" + str(pr_link)
        print(product_url)
        soup_detail = BeautifulSoup(detail.text, 'html.parser')


        product_name_1 = soup_detail.find(class_='page-title fs-30')
        if product_name_1 is not None:
            product_name = product_name_1.next_element.next_element.text
            print(product_name)


        product_brand_1 = soup_detail.find('span', class_='brand-title fs-16')
        if product_brand_1 is not None:
            product_brand = product_brand_1.next_element
            product_brand = product_brand.replace("\n","").replace("\t","").strip(" ")
            print(product_brand)

            #soup_detail.find('table', class_='product-specs').text.replace("\n", " ").split("  ")


        general = soup_detail.find('table', class_='product-specs')
        if general is not None:
             general = general.text
             general = general.replace("\n", " ")
             general = general.replace("\xa0", " ")
             general = general.strip(" ")
             general = general.split("   ")
             product_barcode = [i for i in general if "Barkod" in i]
             product_barcode = " ".join(str(x) for x in product_barcode)
             product_barcode = product_barcode.split(":")
             product_barcode = product_barcode[1].strip(" ")
             print(product_barcode)
             #product_barcode = product_barcode[0]
             #soup_detail.find('table', class_='product-specs').text.replace("\n", " ").replace("\xa0"," ").strip(" ").split("   ")
             product_age_range = [i for i in general if "Yaş Aralığı" in i]
             product_age_range = " ".join(str(x) for x in product_age_range)
             product_age_range = product_age_range.split(":")
             product_age_range = product_age_range[1].strip(" ")
             print(product_age_range)
             product_origin = [i for i in general if "Üretim Yeri" in i]
             product_origin = " ".join(str(x) for x in product_origin)
             product_origin = product_origin.split(":")
             product_origin = product_origin[1].strip(" ")
             print(product_origin)
        else:
            product_barcode = None
            product_age_range = None
            product_origin = None

        pc1 = soup_detail.find_all("a" , class_='fs-14')
        if pc1 is not None:
            pc1 = pc1[1].get_text()
            product_main_category = pc1
            print(product_main_category)
        pc2 = soup_detail.find_all("a" , class_='fs-14')
        if pc2 is not None:
            pc2 = pc2[2].get_text()
            product_category = pc2
            print(product_category)
        pc3 = soup_detail.find_all("a" , class_='fs-14')
        if pc3 is not None:
            pc3 = pc3[3].get_text()
            product_subcategory = pc3
            print(product_subcategory)
        else:
            product_subcategory = None
            product_main_category = None
            product_category = None


        #product_long_info = [x.get_text().replace("\n", " ") for x in soup_detail.find_all(class_='text fs-16')]
        #product_long_info = ''.join(product_long_info)
        #print(product_long_info)


        product_picture_1 = soup_detail.find('meta', itemprop='image')
        if product_picture_1 is not None:
            str_image = product_picture_1['content']
            product_picture = str_image
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
        print('product_label: ', product_label) yok
        '''

        x.append({  'url': url,
                    'product_url': product_url,
                    'product_brand': product_brand,
                    'product_age_range' : product_age_range,
                    'product_origin' : product_origin,
                    'product_name': product_name,
                    'product_main_category': product_main_category,
                    'product_category': product_category,
                    'product_subcategory': product_subcategory,
                    'product_barcode': product_barcode,
                    'product_picture': product_picture })

        df = pd.DataFrame(x)

        df.to_excel('toyzzshop_oyuncak_yapim_oyuncaklari.xlsx', index=False)

        #file = open('vitaminler_denemelerrrr.csv', 'w', newline='', encoding='utf-8')
        #writer = csv.writer(file)
        #headers = ([url, pr_link, product_brand, product_name,
        #            product_main_category, product_category, product_subcategory, product_picture,
        #            product_long_info, product_label])
        #writer.writerow(headers)
        #file.close()m