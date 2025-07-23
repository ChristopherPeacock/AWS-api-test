from bs4 import BeautifulSoup
import requests

def get_instagram_hashtags(query):
    url = f"https://www.best-hashtags.com/hashtag/{query}/"
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')
    hashtags = soup.find("div", {"class": "tag-box tag-box-v3 margin-bottom-40"}).text
    return hashtags.strip()