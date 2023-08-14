from comcrawl import IndexClient
import json
import os


with open('./collinfo.json', 'r') as f:
    collinfo = json.load(f)
    collinfo = [entry['id'].replace('CC-MAIN-', '') for entry in collinfo]
print(collinfo)

sites = {
    'cnn': 'cnn.com/*',
    'fox': 'foxnews.com/*',
    'msnbc': 'msnbc.com/*'
}

for site in sites.keys():
    for idx in collinfo:
        filename = site + '_' + idx + '.json'
        collected = os.listdir('../url_data/')
        if filename in collected:
            # print('{} already collected'.format(filename))
            continue
        else:
            print(filename)
        try:
            index_range = [idx]
            client = IndexClient(index_range)
            client.search(sites[site], threads=4)
            search_results = [res for res in client.results if res['status'] == '200']

            save_results = []
            for i in search_results:
                if str(i.get('url')).count('/') > 3:
                    save_results.append(i)
            # if save_results==[]:
            #     print('got an empty list')
            #     continue

            fout = open('../url_data/' + filename, 'w', encoding='utf-8')
            json.dump(save_results, fout, indent=4)
            fout.close()
            print('completed')
        except Exception as e:
            try:
                os.remove(filename)
                print('{} deleted'.format(filename))
            except:
                pass
            print('For {} got exception {}'.format(filename, e))
            # time.sleep(600)
