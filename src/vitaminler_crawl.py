import urllib3
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from csv import writer
import csv
import pandas as pd

sess = requests.Session()

lst = [i for i in range(1,6)] #7 page

x = []

for n in lst:
    url = 'https://www.vitaminler.com/c/diger-takviyeler-74?pagenumber=' + str(n)
    res = sess.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    #print(soup.prettify())
    print(url)

    # Grab only the main content part of the page
    main_page = soup.find('div', {'class': 'category-products cfix'})
    # print(main_page)

    main_page_for_link = main_page.find_all('a', class_='track-link eecommerce-product-link', href=True)
    for pr in main_page_for_link:
        pr_partial_link = pr['href']
        pr_link = pr_partial_link
        print(pr_link)

        detail = sess.get(pr_link)
        soup_detail = BeautifulSoup(detail.text, 'html.parser')

        product_brand_1 = soup_detail.find(class_='track-link p-detail-spec-link')
        if product_brand_1 is not None:
            product_brand = product_brand_1['data-label']
            print(product_brand)

        product_name_1 = soup_detail.find(class_='product-page-title')
        if product_name_1 is not None:
            product_name = product_name_1.next_element
            print(product_name)

        #product_barcode_1 = soup_detail.find(class_='fr col chbarcode')
        #if product_barcode_1 is not None:
            # product_barcode = product_barcode_1.next_element
            # print(product_barcode)

        pc1 = soup_detail.find(class_='catalog_path path', recursive=True)
        if pc1 is not None:
            pc2 = pc1.text
            pc3 = pc2.split(sep="\n")
            product_main_category = [i.replace("\n", "") for i in pc3][3]
            product_category = [i.replace("\n", "") for i in pc3][10]
            product_subcategory = [i.replace("\n", "") for i in pc3][16]
            print(product_main_category)
            print(product_category)
            print(product_subcategory)

        product_long_info = [x.get_text().replace("\n", " ") for x in soup_detail.find_all(class_='product-panel-description cfix')]
        product_long_info = ''.join(product_long_info)
        print(product_long_info)


        product_picture_1 = soup_detail.find('img', class_='cloudzoom')
        if product_picture_1 is not None:
            product_picture_2 = product_picture_1['src']
            if product_picture_2 is not None:
                product_picture = product_picture_2
                print(product_picture)
        product_label = [x.get_text() for x in soup_detail.find_all('h1', class_='product-page-title')]
        product_label = ''.join(product_label)
        print(product_label)

        '''
        print('product_link: ', pr_link) okey
        print('product_brand: ', product_brand) okey
        print('product_name: ', product_name) okey 
        print('product_barcode: ', product_barcode.text) yok
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
                    'product_main_category': product_main_category,
                    'product_category': product_category,
                    'product_subcategory': product_subcategory,
                    'product_picture': product_picture,
                    'product_long_info': product_long_info,
                    'product_label': product_label})

        df = pd.DataFrame(x)

        df.to_excel('vitaminler_Diğer_Takviyeler.xlsx', index=False)

        #file = open('vitaminler_denemelerrrr.csv', 'w', newline='', encoding='utf-8')
        #writer = csv.writer(file)
        #headers = ([url, pr_link, product_brand, product_name,
        #            product_main_category, product_category, product_subcategory, product_picture,
        #            product_long_info, product_label])
        #writer.writerow(headers)
        #file.close()m