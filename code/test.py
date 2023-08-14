from newsplease import NewsPlease
import time

s = time.time()
articles = NewsPlease.from_urls(['http://www.cnn.com/2000/ALLPOLITICS/stories/03/27/burton.reno/',
                                 'http://www.cnn.com/2001/ALLPOLITICS/03/11/palmbeach.recount/index.html',
                                 'http://www.cnn.com/2001/ALLPOLITICS/06/07/tax.primer/'], timeout=6)

print(time.time()-s)
print(articles)

