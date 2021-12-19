import requests
from bs4 import BeautifulSoup
import unicodedata

from send_email import send_email

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2228.0 Safari/537.36",
    "Accept-Language": "en-US, en;q=0.5",
}


def get_product_info(url):
    page = requests.get(url, headers=HEADERS)
    soup = BeautifulSoup(page.content, features="lxml")

    try:
        title = soup.find(id="productTitle").get_text().strip()
        price_str = soup.find(id="priceblock_ourprice").get_text()
    except:
        return None, None, None

    try:
        soup.select(id="#availability .a-color-success")[0].get_text().strip()
        available = True
    except:
        available = False

    try:
        price = unicodedata.normalize("NFKD", price_str)
        price = price.replace(",", ".").replace("$", "")
        price = float(price)
    except:
        return None, None, None


if __name__ == "__main__":
    url = "https://www.amazon.com/CanaKit-Raspberry-8GB-Extreme-Kit/dp/B08B6F1FV5/ref=sr_1_2?crid=1PYPX1MUZVM45&keywords=raspberry+pi+4+8gb&qid=1639940074&sprefix=raspberry+pi+%2Caps%2C281&sr=8-2"
    products = [(url, 170)]

    products_below_limits = []
    for product_url, limit in products:
        title, price, available = get_product_info(product_url)
        if title is not None and price < limit and available:
            products_below_limits.append((url, title, price))

    if products_below_limits:
        message = "Subject: Your item is below limit!!"

        for url, title, price in products_below_limits:
            message += f"{title}\n"
            message += f"Price: {price}\n"
            message += f"{url}\n"

        send_email(message)
