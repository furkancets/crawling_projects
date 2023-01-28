import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from config_url import URLLIST

def crawler_one():

    sess = requests.Session()

    lst = [i for i in range(1, 3)]

    a = []

    for n in lst:

        url = URLLIST.crawler_one_one_url + str(n)
        res = sess.get(url)
        soup = BeautifulSoup(res.text, 'lxml')
        print(url)

        # Grab only the main content part of the page
        main_page = soup.find('div', {'class': 'product-grid-border-fix fix-bottom-border'})

        main_page_for_link = main_page.find_all('a', class_='product-item style--three alt color--light with-secondary-image', href=True)
        for pr in main_page_for_link:
            pr_partial_link = pr['href']
            pr_link = pr_partial_link
            url = URLLIST.crawler_one_two_url + pr_link
            print(url)

            detail = sess.get(url)
            soup_detail = BeautifulSoup(detail.text, 'html.parser')

            product_name_1 = soup_detail.find(class_='product-title')
            if product_name_1 is not None:
                product_name = product_name_1.get_text()
                print(product_name)

            manufacturer_1 = soup_detail.find('span', attrs={'class':'product-vendor text-size--small'})
            if manufacturer_1 is not None:
                manufacturer = manufacturer_1.next_element.next_element.next_element
                print(manufacturer)

            product_variant_1 = json.loads(soup_detail.find('script', type='application/ld+json').text)["offers"]
            if product_variant_1 is not None:
                for i, k in enumerate(product_variant_1):

                    print(i, k["name"], k["price"], product_name)
                    a.append({"manufacturer": manufacturer,
                               "product_name": product_name,
                               "variants": k["name"],
                               "price": k["price"]})
            df = pd.DataFrame(a)

            return df.to_excel('allin.xlsx', index=False)
