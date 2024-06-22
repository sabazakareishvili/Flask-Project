import requests
import sqlite3
from bs4 import BeautifulSoup


def get_news():

    conn = sqlite3.connect('news.db')
    cursor = conn.cursor()
    url = 'https://tabula.ge/ge/news'
    response = requests.get(url)
    info = BeautifulSoup(response.text, 'html.parser')
    data = info.find('div', class_='PagedNewsItemList_listWrap__Jr25w PagedNewsItemList_type-grid__3ougZ')
    full_info = data.find_all('div', class_='news-item-list-item')


    for item in full_info:

        time = item.find('time').attrs['title']
        title = item.find('strong', class_='Vertical_title__2S29g item-title').text
        image = item.find('img', class_='Thumbnail_thumbnail__4GIBv').attrs['src']
        link = item.find('a').attrs['href']
        url = f'https://tabula.ge{link}'
        res = requests.get(url)
        content = BeautifulSoup(res.text, 'html.parser')
        information = content.find('div', class_='ArticleContent_contentTextWrapper__n-T_q content-text').text


        cursor.execute('''
        CREATE TABLE IF NOT EXISTS News
        (Id INTEGER PRIMARY KEY AUTOINCREMENT,
        Posted_Time DATETIME NOT NULL,
        Title TEXT,
        Image TEXT,
        Content TEXT
        )
        ''')

        cursor.execute('''
        INSERT INTO News (Posted_Time, Title, Image,Content) VALUES (?,?,?,?)
        ''',(time,title,image,information))

        conn.commit()


if __name__ == '__main__':
    print(get_news())
