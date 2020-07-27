import requests
import json
import sys, getopt
from bs4 import BeautifulSoup


# Function to save article list to file
def save_function(article_list):
    with open('articles.txt', 'a') as outfile:
        json.dump(article_list, outfile)


# Windsor Star, CBS, CTV
def rss(feed, src):
    article_list = []
    keywords = ['OGVG', 'Ontario Greenhouse Vegetable Growers', 'Greenhouse', 'COVID-19']

    try:
        # Get rss feed using requests and read it using BeautifulSoup
        r = requests.get(feed)
        soup = BeautifulSoup(r.content, features='xml')

        # Scrape the xml
        articles = soup.find_all('item')

        # Parse all articles, only keep relevant ones
        for a in articles:
            title = a.find('title').text
            link = a.find('link').text
            published = a.find('pubDate').text

            # Check title for keywords
            for w in title.split():
                if w in keywords:
                    article = {
                        'title': title,
                        'link': link,
                        'published': published,
                        'src': src
                    }
                    article_list.append(article)
                    #print('Title: {}\nSource: {}\n'.format(title, src))
                    #print('=================================\n')

        return save_function(article_list)

    except Exception as e:
        print('Windsor Star scraping job failed. See exception:')
        print(e)


print('Starting scraping\n')

# Load RSS feed data from JSON file
with open('feeds.json', 'r') as f:
    data = f.read()
feeds = json.loads(data)

# Scrape all feeds
for f in feeds['feeds']:
    print(f['link'], '\n', f['src'])
    rss(f['link'], f['src'])

print('Finished scraping')
