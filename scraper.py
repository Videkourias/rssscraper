import requests
import json
import sys, getopt, os
import webbrowser
from bs4 import BeautifulSoup


# Function to save article list to file
def save_function(article_list):
    fname = 'articles.json'

    # Check if file already exists
    if os.path.isfile(fname):
        with open(fname, 'r') as f:
            data = json.load(f)
            articles = data['articles']
            articles.extend(article_list)

        with open(fname, 'w') as f:
            json.dump(data, f)
    else:
        # Convert list of dictionaries to one dictionary
        dictionary = {
            'articles': article_list
        }

        with open(fname, 'w') as f:
            json.dump(dictionary, f)


# Verifies that txt contains all of kwand or any of kwor
def verify(txt, kwand, kwor):
    kwall = True
    kwany = False

    for w in kwand:
        if w.lower() not in txt:
            kwall = False
            break

    for w in kwor:
        if w.lower() in txt:
            kwany = True
            break

    return kwall or kwany


# Method to GET RSS feeds from links passed through feed argument
def rss(feed, src, kwand, kwor):
    article_list = []

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

            if verify([w.lower() for w in title.split()], kwand, kwor):
                article = {
                    'title': title,
                    'link': link,
                    'published': published,
                    'src': src
                }
                article_list.append(article)

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
        print('Searching for articles with title containing all '
              'of:\n{}\nor any of:\n{}\n'.format(kwand, kwor))

        # Load RSS feed data from JSON file
        with open('feeds.json', 'r') as f:
            data = f.read()
        feeds = json.loads(data)

        # Scrape all feeds
        for f in feeds['feeds']:
            rss('https://windsorstar.com/feed', 'Windsor Star', kwand, kwor)
            # rss(f['link'], f['src'], kwand, kwor)

        print('Finished scraping')

    else:
        print("No search terms(keywords) have been provided, try using -a or -o. Exiting...")

# Creates HTML page using info pulled from articles.txt
def createHTML():
    with open('data.html', 'wb') as f:
        inner = '''
        <html>
        <head><title>Data</title></head>
        <body>
            <table>
                <thead>
                    <th>Title</th>
                    <th>Link</th>
                    <th>Publish Date</th>
                    <th>Source</th>
                </thead>
        '''


        inner = inner + '''
            </table>
        </body>
        </html>
        '''


if __name__ == '__main__':
    main(sys.argv[1:])
