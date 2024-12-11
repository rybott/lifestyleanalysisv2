import imaplib
import email
from datetime import datetime, timedelta
import re
import pandas as pd
from bs4 import BeautifulSoup
import requests

class GNews:
    def __init__(self):
        api_key = '1c1f12734a93758fea9858a87005d1b8'
        categories = ['general', 'world', 'nation', 'business', 'technology', 'entertainment', 'sports', 'science', 'health']

        category = []
        datetime = []
        title = []
        source = []
        description = []
        content = []
        urls = []

        for cat in categories:
            url = f"https://gnews.io/api/v4/top-headlines?category={cat}&lang=en&country=us&max=10&apikey={api_key}"
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                articles = data["articles"]

                for i in range(len(articles)):
                    try:
                        category.append(cat)
                        datetime.append(articles[i]['publishedAt'])
                        title.append(articles[i]['title'])
                        source.append(articles[i]['source']['name'])
                        description.append(articles[i]['content'])
                        content.append(articles[i]['description'])
                        urls.append(articles[i]['url'])
                    except:
                        pass
            else:
                # Add an error logging system
                continue
        return pd.DataFrame({
            'category': category,
            'datetime': datetime,
            'title': title,
            'source': source,
            'description': description,
            'content': content,
            'url': urls
        })

class APNews_alerts:
    def __init__(self, day):
        pass
        imap_server = "imap.gmail.com"
        email_address = "r.bonannibott@gmail.com"
        pw = "aaed bssv hrij tgfa "
        imap = imaplib.IMAP4_SSL(imap_server)
        imap.login(email_address, pw)

        # Start End Date
        end_date = datetime.now()
        start_date = end_date - timedelta(days=day)
        start_str = start_date.strftime("%d-%b-%Y")
        end_str = (end_date + timedelta(days=1)).strftime("%d-%b-%Y")

        # Discover
        imap.select('"Discover Transactions"')
        _, msgnums = imap.search(None, f'(SINCE "{start_str}" BEFORE "{end_str}")')
    