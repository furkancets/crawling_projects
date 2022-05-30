import urllib3
import requests
from bs4 import BeautifulSoup
from urllib.request import urlopen
import re
from csv import writer
import csv
import json
import pandas as pd

sess = requests.Session()

lst = [i for i in range(1,3)] #7 page



for n in lst:
    url = 'https://www.all-in-line.com/pages/art-exhibition'
    res = sess.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    #print(soup.prettify())
    print(url)

    # Grab only the main content part of the page
    main_page = soup.find('div', {'class': 'sc-eicpiI jZhPZM pf-30_ pf-r pf-r-ew'})
    # print(main_page)



    x=[]
    main_page_for_link = main_page.find_all('a', href=True)
    for pr in main_page_for_link:
        pr_partial_link = pr['href']
        pr_link = pr_partial_link
        url = 'https://www.all-in-line.com/' + pr_link
        print(url)
        artist_name = pr["href"].strip('/').split('/')[1]
        print(artist_name)

        detail = sess.get(url)
        soup_detail = BeautifulSoup(detail.text, 'html.parser')

        #product_name_1 = soup_detail.find('span', attrs={'class':'title'})
        #if product_name_1 is not None:
        #    product_name = product_name_1.next_element.text
        #    print(product_name)

        #manufacturer_1 = soup_detail.find('span', attrs={'class':'product-vendor text-size--small'})
        #if manufacturer_1 is not None:
            #manufacturer = manufacturer_1.next_element.next_element.next_element
            #print(manufacturer)

        product_detail = soup_detail.find_all('a', class_="product-item style--three alt color--light with-secondary-image", href=True)
        for pa in product_detail:
            pr_partial_link = pa['href']
            pr_link = pr_partial_link
            url_2 = 'https://www.all-in-line.com/' + pr_link
            print(url_2)
            product_name = pa["href"].strip('/').split('/')[1]
            print(product_name)

            detail_2 = sess.get(url_2)
            pro_detail = BeautifulSoup(detail_2.text, 'html.parser')

            product_variant_1 = json.loads(pro_detail.find('script', type='application/ld+json').text)["offers"]
            if product_variant_1 is not None:
                for i, k in enumerate(product_variant_1):

                    print(i, k["name"], k["price"], product_name, artist_name)
                    x.append({"artist_name": artist_name,
                            "product_name": product_name,
                            "variants": k["name"],
                            "price": k["price"]})
        df = pd.DataFrame(x)
        df.to_excel('art_exhibition.xlsx', index=False)

        #print("ok")

        #product_price_1 = soup_detail.find(class_='price')
        #if product_price_1 is not None:
         #   product_price = product_price_1.get_text()
          #  product_price_1.replace("\n", "")
           # print(product_price)
        #print(1)

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

        #x.append({
                    #'product_name': a[2],
                    #'variants': a[1],
                    #'price' : a[3]

                    #})

        #df = pd.DataFrame(a)

        #df.to_excel('abc.xlsx', index=False)

        #file = open('vitaminler_denemelerrrr.csv', 'w', newline='', encoding='utf-8')
        #writer = csv.writer(file)
        #headers = ([url, pr_link, product_brand, product_name,
        #            product_main_category, product_category, product_subcategory, product_picture,
        #            product_long_info, product_label])
        #writer.writerow(headers)
        #file.close()m