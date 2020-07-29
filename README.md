# rssscraper
Python script to scrape RSS feeds of popular news websites for articles containing keywords<br>
Pulls from the RSS feeds provided in feeds.json

```
scraper.py -a "kw kw k_w..." -o "kw kw k_w..."
-a, -o: Take a string of space seperated search terms.
        Underscores will be replaced by spaces before searching
Searching with -a search terms will only pull articles which contain all keywords in their title
Searching with -o search terms will only pull articles which contain any keywords in their title
Searching with -o and -a will pull any article which contains all -a keywords or any -o keywords

ex.
scraper.py -a "America COVID-19 Mask"
scraper.py -o "Soccer Football Leg_injury"
scraper.py -a "U.S Russia" -o "China Canada Australia"
```
Information scraped is stored in the articles directory as JSON data files. Each file has a corresponding HTML<br>
document in the data directory, allowing user friendly view of scraped data