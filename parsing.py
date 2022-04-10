import requests
from bs4 import BeautifulSoup as BS
from lib_sql.tables_sql import TablesSQL
from lib_sql.sql_config import db
from pict_parse import *

from multiprocessing import Pool

# Open connection with DB
cursor = db.cursor()

# Object of TableSQL class
table_sql = TablesSQL(cursor)



# Parsing URL
URL = 'https://neman.kg/sitemap/'

# Get response for URL
def get_response(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
        # print(response.text)
    else:
        return f'Error - {response.status_code}'


# Search all categories
def get_categories_urls(html):
    urls = []
    soup = BS(html, 'html.parser')
    menu = soup.find('div', class_ = 'ty-sitemap__tree-section')
    categories = menu.find_all('ul', class_ = 'ty-sitemap__tree-section-list')

    for category in categories:
        parent = category.find('li', class_ = 'ty-sitemap__tree-list-item parent')
        category_name = parent.find('a').text.strip()       # Take category names
        link = parent.find('a').get('href')
        table_sql.add_new_content('category', 'name, url', f"'{category_name}', '{link}'")       # Add to db.table
        urls.append(link)
    return urls

urls = get_categories_urls(get_response(URL))       # Get category URLS


# Search last page for category
def get_last_page_number(url):
    url_numb = 1
    action = True
    while action:
        url1 = url+'page-'+str(url_numb)
        response = requests.get(url1)
        if response.status_code == 200:
            url_numb += 1
        else:
            action = False
    return url_numb


# Parsing page data script
def get_page_data(html):
    soup = BS(html, 'html.parser')
    items = soup.find('div', class_ = 'ty-pagination-container cm-pagination-container').\
        find_all('div', class_ = 'ty-column3')

    cat_name = soup.find('div', class_ = 'ut2-extra-block-title').\
        find('h1', class_ = 'ty-mainbox-title').\
        find('span').text.strip()

    for item in items:
        try:
            title = item.find('div', class_ = 'ut2-gl__name').\
                find('a', class_ = 'product-title').text.strip()

            price = item.find('div', class_ = 'ut2-gl__price').\
                find('span', class_ = 'ty-price-update').\
                find('span', class_ = 'ty-price-num').text.strip()

            cat_id = table_sql.get_definite_content('id', 'category', 'name', cat_name)

            try:
                image_url_parse = item.find('div', class_ = 'ut2-gl__image').find('img').get('data-src')
            except Exception as ex:
                image_url_parse = 'photo_exists'
            if image_url_parse != 'photo_exists':
                save_data(get_name(image_url_parse), get_file(image_url_parse))
                image_url_db = '/images/'+str(get_name(image_url_parse))
            else:
                image_url_db = '/images/photo_exists.png'
            columns = 'name, price, category_id, image_url'
            values = f"'{title}','{price}','{cat_id[0]}','{image_url_db}'"
            table_sql.add_new_content('products', columns, values)
            print(title)    # Debug
        except Exception as ex:
            continue

# Parsing main script
for url in urls:
    last_page = get_last_page_number(url)
    for i in range(1, last_page):
        page_url = url + 'page-' + str(i)
        print(page_url)
        get_page_data(get_response(page_url))


# Close connection with DB
cursor.close()

