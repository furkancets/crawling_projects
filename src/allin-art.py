import requests
from bs4 import BeautifulSoup
import json
import pandas as pd
from config_url import URLLIST

sess = requests.Session()

lst = [i for i in range(1, 3)] #7 page

for n in lst:
    url = URLLIST.crawler_one_three_url
    res = sess.get(url)
    soup = BeautifulSoup(res.text, 'lxml')
    print(url)

    # Grab only the main content part of the page
    main_page = soup.find('div', {'class': 'sc-eicpiI jZhPZM pf-30_ pf-r pf-r-ew'})

    x = []

    main_page_for_link = main_page.find_all('a', href=True)
    for pr in main_page_for_link:
        pr_partial_link = pr['href']
        pr_link = pr_partial_link
        url = URLLIST.crawler_one_two_url + pr_link
        print(url)
        artist_name = pr["href"].strip('/').split('/')[1]
        print(artist_name)

        detail = sess.get(url)
        soup_detail = BeautifulSoup(detail.text, 'html.parser')

        product_detail = soup_detail.find_all('a', class_="product-item style--three alt color--light with-secondary-image", href=True)
        for pa in product_detail:
            pr_partial_link = pa['href']
            pr_link = pr_partial_link
            url_2 = URLLIST.crawler_one_two_url + pr_link
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
