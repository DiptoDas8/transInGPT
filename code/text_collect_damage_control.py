from newsplease import NewsPlease
import pandas as pd
import json
import os

import requests
from bs4 import BeautifulSoup

def extract_metadata(url):
    try:
        response = requests.get(url)
        response.raise_for_status()
        soup = BeautifulSoup(response.content, 'html.parser')

        title = soup.find('title').text.strip() if soup.find('title') else ""
        # date = soup.find('meta', {'name': 'date'})['content'] if soup.find('meta', {'name': 'date'}) else ""
        # authors = [author.text.strip() for author in soup.find_all('meta', {'name': 'author'})]
        description = soup.find('meta', {'name': 'articleBody'})['content'] if soup.find('meta', {'name': 'articleBody'}) else ""

        return {
            'title': title,
            'description': description
        }
    except requests.exceptions.RequestException as e:
        print("Error fetching the URL:", e)
        return None

mycolumns = ['authors', 'date_download', 'date_modify', 'date_publish', 'description', 'filename', 'image_url',
             'language', 'localpath', 'title', 'title_page', 'title_rss', 'source_domain', 'maintext', 'url']


all_jsons = [f for f in os.listdir('../url_data/') if f.endswith('.json')]
all_jsons.sort()
for fname in all_jsons:
    print('**** {}'.format(fname.replace('.json', '')))
    try:
        df_fname = pd.read_excel('../news_data/xlsx_data/'+fname.replace('.json', '')+'.xlsx')
        # print(df_fname.shape)
        if df_fname.shape[0]!=0:
            try:
                done_urls = df_fname['url'].tolist()
            except Exception as e1:
                print('excel column to list {}'.format(e1))
        else:
            done_urls = []

        with open('../news_data/failed_urls/failed_urls-{}.txt'.format(fname.replace('.json', '')), 'r') as fin:
            old_failed_urls = [u.strip() for u in fin.readlines()]
        # print(failed_urls)

        articles_list = []
        failed_urls = set()

        for i, url in enumerate(old_failed_urls):
            if url in done_urls:
                print(url)
                continue
            try:
                article = NewsPlease.from_url(url)
                article = vars(article)
                for key in article.keys():
                    if article[key] == None or article[key] == []:
                        article[key] = ''
                    else:
                        article[key] = str(article[key])
                # pprint(article)
                articles_list.append(article)
            except Exception as e2:
                print('newsplease 2 step {} {}'.format(i, e2))
                try:
                    second_try = extract_metadata(url)
                    article = dict()
                    for key in mycolumns:
                        article[key]=''
                        if key=='title':
                            article[key] = second_try['title']
                        elif key=='maintext':
                            article[key] = second_try['description']
                        elif key=='url':
                            article[key] = url
                    articles_list.append(article)
                    print('{} {} retrieved through request'.format(i, url))
                except Exception as e3:
                    print('requests step {}'.format(e3))
                    failed_urls.add(url)


        df = pd.DataFrame(articles_list)
        df = pd.concat([df_fname, df]).sort_values(by=['url'])
        df.to_excel('../news_data/xlsx_data/'+fname.replace('.json', '')+'.xlsx', index=False)

        fout = open('../news_data/failed_urls/failed_urls-{}.txt'.format(fname.replace('.json', '')), 'w',
                    encoding='utf-8')
        for url in list(failed_urls):
            fout.write(url + '\n')
        fout.close()

    except Exception as e4:
        print('reading files step {}'.format(e4))

