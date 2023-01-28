import requests
from bs4 import BeautifulSoup
import pandas as pd
from config_url import URLLIST

sess = requests.Session()

lst = [i for i in range(1, 10)] # 7 page

x = []

for n in lst:
    url = URLLIST.crawler_fourth_one_url + str(n)
    res = sess.get(url)
    soup = BeautifulSoup(res.text, 'lxml')

    print(url)

    # Grab only the main content part of the page
    main_page = soup.find('div', {'class': 'ProductListContent'})
    # print(main_page)

    main_page_for_link = main_page.find_all('a', class_='detailLink detailUrl', href=True)
    for pr in main_page_for_link:
        pr_partial_link = URLLIST.crawler_fourth_two_url + pr['href']
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
            product_picture = URLLIST.crawler_fourth_two_url + str(product_picture_2)
            print(product_picture)

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

        df.to_excel('farma.xlsx', index=False)
