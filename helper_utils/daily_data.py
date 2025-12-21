from functools import lru_cache

import requests
from bs4 import BeautifulSoup


def get_dollar_today():
    url = "https://www.tgju.org/profile/price_dollar_rl"

    headers = {
        "User-Agent": "Mozilla/5.0"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    # پیدا کردن h3 که شامل نرخ فعلی دلاره
    price_h3 = soup.find('h3', {'class': 'line clearfix mobile-hide-block', 'data-target': 'profile-tour-step-2'})

    if price_h3:
        # داخل این h3 → span class="value" → span data-col="info.last_trade.PDrCotVal"
        value_span = price_h3.find('span', class_='value')
        if value_span:
            price_span = value_span.find('span', {'data-col': 'info.last_trade.PDrCotVal'})
            if price_span:
                amount = int(price_span.text.replace(',', '')) // 10
                return amount
            else:
                return None
        else:
            return None
    else:
        return None


@lru_cache(maxsize=60)
def get_dollar_today_2():
    url = "https://www.tgju.org/profile/price_dollar_rl"
    headers = {"User-Agent": "Mozilla/5.0"}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    price_h3 = soup.find('h3', {'class': 'line clearfix mobile-hide-block', 'data-target': 'profile-tour-step-2'})
    if price_h3:
        value_span = price_h3.find('span', class_='value')
        if value_span:
            price_span = value_span.find('span', {'data-col': 'info.last_trade.PDrCotVal'})
            if price_span:
                amount = int(price_span.text.replace(',', '')) // 10
                return amount
    return 0