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
                    # print('Title: {}\nSource: {}\n'.format(title, src))
                    # print('=================================\n')

        return save_function(article_list)

    except Exception as e:
        print('{} scraping job failed. See exception:'.format(src))
        print(e)


def main(argv):
    # Keyword lists
    kwand = []
    kwor = []

    # Handle arguments
    try:
        opts, args = getopt.getopt(argv, "h:a:o:", ['help', 'and=', 'or='])
    except getopt.GetoptError:
        print('scraper.py -a "kw kw k_w..." -o "kw kw k_w..."')
        sys.exit(2)

    for opt, arg in opts:
        if opt in ('-h', '--help'):
            print('scraper.py -a "kw kw k_w..." -o "kw kw k_w..."')
            sys.exit()
        elif opt in ("-a", "--and"):
            words = arg.split(' ')
            for w in words:
                kwand.append(w.replace('_', ' '))
        elif opt in ("-o", "--or"):
            words = arg.split(' ')
            for w in words:
                kwor.append(w.replace('_', ' '))

    if kwand or kwor:
        print('Starting scraping\n')
        print('Searching for articles with title containing all of:\n{}\nor any of:\n{}\n'.format(kwand, kwor))

        # Load RSS feed data from JSON file
        with open('feeds.json', 'r') as f:
            data = f.read()
        feeds = json.loads(data)

        # Scrape all feeds
        for f in feeds['feeds']:
            pass
            # rss(f['link'], f['src'])

        print('Finished scraping')

    else:
        print("No search terms(keywords) have been provided, try using -a or -o. Exiting...")


if __name__ == '__main__':
    main(sys.argv[1:])
