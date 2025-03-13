import os
import requests
from p2p_lending_base import P2PLendingBase

class CapitalRise(P2PLendingBase):
    def __init__(self):
        provider_name = os.path.splitext(os.path.basename(__file__))[0]
        super().__init__(provider_name)
        self.url = "https://www.capitalrise.com/"

    def fetch_raw_html(self):
        response = requests.get(self.url, timeout=10)
        response.raise_for_status()
        return response.text

    def extract_opportunity_count(self, soup):
        investments_menu_item = soup.select_one("ul.main-menu > li.menu-item > a#main-menu-item_investments")
        ul_element = investments_menu_item.parent.find("ul", class_="sub-menu")
        return len(ul_element.find_all("li")) - 1 if ul_element else 0

if __name__ == "__main__":
    CapitalRise().run()
