import string
import requests
from bs4 import BeautifulSoup
import os


# function to format title and description
def format_string(s):
    for i in s:
        if i in string.punctuation:
            s = s.replace(i, '')
        s = s.replace(' ', '_')
    return s


page_input = int(input("Enter number of pages: "))
type_input = input("Enter article type: ")

page_link = 'https://www.nature.com/nature/articles?sort=PubDate&year=2020&page='


saved = []
links = []

for j in range(1, page_input+1):

    page = requests.get(page_link + str(j))
    soup = BeautifulSoup(page.content, 'html.parser')

    folder_name = 'Page_' + str(j)
    os.mkdir(folder_name)

    if page.status_code == 200:

        for item in soup.select('article'):

            if type_input == item.select_one('span[class="c-meta__type"]').text:

                    link = item.find(href=True)
                    links.append(link['href'])
                    title = item.select_one('a[data-track-action="view article"]').text
                    mod_title = format_string(title)
                    saved.append(f'{mod_title}.txt')
        i = 0
        for item in links:
            link = 'https://nature.com' + item
            article_page = requests.get(link)
            article_soup = BeautifulSoup(article_page.content, 'html.parser')

            if article_page.status_code == 200:
                text = article_soup.select_one('div[class="c-article-body u-clearfix"]').text
                file_name = os.path.join(folder_name, f'{saved[i]}')

                with open(file_name, 'w') as f:
                    f.write(text)

            else:
                print('The article URL returned ' + str(page.status_code) + '!')
            i = i + 1
    else:
        print('The URL returned ' + str(page.status_code) + '!')

print("Saved all articles.")

