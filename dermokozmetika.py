import requests
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import pandas as pd

sess = requests.Session()

lst = [i for i in range(1, 7)]

x = []

for i in lst:
    url = "https://www.dermokozmetika.com.tr/hediye-setleri?pg=" + str(i)

    res = sess.get(url)

    soup = BeautifulSoup(res.text, 'lxml')

    print(url)

    main_page = soup.find('div', {'class': 'my--4 row'})

    main_page_for_link = main_page.find_all('a', class_='catalog', href=True)

    for pr in main_page_for_link:
        pr_partial_link = pr['href']
        pr_link = pr_partial_link
        print(pr_link)

        detail = sess.get(pr_link)
        soup_detail = BeautifulSoup(detail.text, 'html.parser')

        product_brand_1 = soup_detail.find(class_='col-md')
        if product_brand_1 is not None:
            product_brand = product_brand_1.text
            print(product_brand)

        product_name_1 = soup_detail.find('h1', {'class': 'block-subtitle h2'})
        if product_name_1 is not None:
            product_name = product_name_1.text
            print(product_name)

        product_category_1 = soup_detail.find('nav', {'class': 'breadcrumb'})
        product_category_1 = [i.text for i in product_category_1]
        print("ok")
        if len(product_category_1) < 4:
            product_main_category = None
            product_category = None
            product_subcategory = None
        else:
            if product_category_1[1] is not None:
                product_main_category = product_category_1[1]
            else:
                product_main_category = None
            print(product_main_category)
            if product_category_1[2] is not None:
                product_category = product_category_1[2]
            else:
                product_category = None
            print(product_category)
            if product_category_1[3] is not None:
                product_subcategory = product_category_1[3]
            else:
                product_subcategory = None
            print(product_subcategory)

        product_info_1 = soup_detail.find('div', {'class': 'product-detail'})
        if product_info_1 is not None:
            product_info_1 = product_info_1.text
            product_info = product_info_1.replace("\u200b", "")

            print(product_info)

        product_picture_1 = soup_detail.find('img', {'class': 'block-img img-lazy'})
        if product_picture_1 is not None:
            product_picture = product_picture_1["data-src"]

            print(product_picture)

        product_price_with_vat_1 = soup_detail.find('p', {'class': 'block-text h2 text-danger'})
        if product_price_with_vat_1 is not None:
            product_price_with_vat_1 = product_price_with_vat_1.text
            product_price_with_vat = product_price_with_vat_1.split("\xa0")[1]

            print(product_price_with_vat)

        product_short_info_1 = soup_detail.find('h2', {'class': 'h5 block-subtitle text-gray-dark'})
        if product_short_info_1 is not None:
            product_short_info = product_short_info_1.text

            print(product_short_info)

        x.append({'url': url,
                  'pr_link': pr_link,
                  'product_brand': product_brand,
                  'product_name': product_name,
                  'product_main_category': product_main_category,
                  'product_category': product_category,
                  'product_subcategory': product_subcategory,
                  'product_picture': product_picture,
                  'product_price_with_vat': product_price_with_vat,
                  'product_short_info' : product_short_info
                      })

        df = pd.DataFrame(x)

        df.to_excel('dermokozmetika_hediye_setleri.xlsx', index=False)
