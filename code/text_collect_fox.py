# from newsplease import NewsPlease
# import pandas as pd
# import json
# import os
# from pprint import pprint


# def collect_news():
#     all_jsons = [f for f in os.listdir('../url_data/') if f.endswith('.json')]

#     for fname in all_jsons:
#         # fname = 'msnbc_2008-2009.json'
#         if fname.replace('.json', '')+'.xlsx' in os.listdir('../news_data/'):
#             print('{} already done'.format(fname))
#             continue
#         with open('../url_data/'+fname, 'r', encoding='utf-8') as fin:
#             print('{} currently doing'.format(fname))
#             file_data = json.load(fin)
#             list_of_urls = [entry['url'] for entry in file_data]
#             print(len(list_of_urls))
#             with open('../news_data/'+fname.replace('.json','')+'.txt', 'w', encoding='utf-8') as fout:
#                 for u in list_of_urls:
#                     fout.write(u+'\n')

#         articles_list = []
#         failed_urls = set()
#         print(len(list_of_urls))
#         for i, url in enumerate(list_of_urls):
#             print(i, url)
#             try:
#                 article = NewsPlease.from_url(url)
#                 article = vars(article)
#                 for key in article.keys():
#                     if article[key] == None or article[key] == []:
#                         article[key] = ''
#                     else:
#                         article[key] = str(article[key])
#                 # pprint(article)
#                 articles_list.append(article)
#             except Exception as e:
#                 print('{} {}'.format(i, e))
#                 failed_urls.add(url)

#         df = pd.DataFrame(articles_list)
#         df.to_excel('../news_data/'+fname.replace('.json', '')+'.xlsx', index=False)

#         fout = open('../news_data/failed_urls-{}.txt'.format(fname.replace('.json', '')), 'w', encoding='utf-8')
#         for url in list(failed_urls):
#             fout.write(url+'\n')
#         fout.close()



# collect_news()


import os
import json
import pandas as pd
from tqdm import tqdm  # Import the tqdm library
from newsplease import NewsPlease  # Assuming you have the newsplease library installed

def collect_news():
    all_jsons = [f for f in os.listdir('../url_data/') if f.endswith('.json') and f.startswith('fox')]
    all_jsons = sorted(all_jsons)

    for fname in all_jsons:
        if fname.replace('.json', '')+'.xlsx' in os.listdir('../news_data/'):
            print('{} already done'.format(fname))
            continue
        with open('../url_data/'+fname, 'r', encoding='utf-8') as fin:
            file_data = json.load(fin)
            list_of_urls = [entry['url'] for entry in file_data]

            with open('../news_data/'+fname.replace('.json','')+'.txt', 'w', encoding='utf-8') as fout:
                for u in list_of_urls:
                    fout.write(u+'\n')

        articles_list = []
        failed_urls = set()

        with tqdm(total=len(list_of_urls), dynamic_ncols=True) as pbar:  # Initialize the progress bar
            # Prepend the filename from all_jsons to the description
            pbar.set_description(fname) 

            for i, url in enumerate(list_of_urls):
                try:
                    article = NewsPlease.from_url(url)
                    article = vars(article)
                    for key in article.keys():
                        if article[key] == None or article[key] == []:
                            article[key] = ''
                        else:
                            article[key] = str(article[key])
                    articles_list.append(article)
                except Exception as e:
                    failed_urls.add(url)
                pbar.update(1)  # Update the progress bar

        df = pd.DataFrame(articles_list)
        df.to_excel('../news_data/'+fname.replace('.json', '')+'.xlsx', index=False)

        with open('../news_data/failed_urls-{}.txt'.format(fname.replace('.json', '')), 'w', encoding='utf-8') as fout:
            for url in list(failed_urls):
                fout.write(url+'\n')

if __name__ == "__main__":
    collect_news()