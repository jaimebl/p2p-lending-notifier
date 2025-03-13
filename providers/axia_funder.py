import os
import requests
from p2p_lending_base import P2PLendingBase

class AxiaFunder(P2PLendingBase):
    def __init__(self):
        provider_name = os.path.splitext(os.path.basename(__file__))[0]
        super().__init__(provider_name)
        self.url = "https://www.axiafunder.com/"

    def fetch_raw_html(self):
        response = requests.get(self.url, timeout=10)
        response.raise_for_status()
        return response.text

    def extract_opportunity_count(self, soup):
        number_of_live_offers = soup.find("input", id="NumberOfLiveOffers")
        return int(number_of_live_offers["value"]) if number_of_live_offers else 0

if __name__ == "__main__":
    AxiaFunder().run()
