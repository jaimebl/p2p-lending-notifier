import logging
import os

from bs4 import BeautifulSoup

from gist_handler import get_gist_value, update_gist_value
from telegram_notifier import send_telegram_message

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

class P2PLendingBase:
    def __init__(self, provider_name):
        self.provider_name = provider_name
        self.telegram_bot_token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.telegram_chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.gist_id = os.getenv("GIST_ID")
        self.github_token = os.getenv("GIST_ACCESS_TOKEN_SECRET")

    def fetch_raw_html(self):
        """Subclasses must implement this to fetch raw HTML content from their provider."""
        raise NotImplementedError("Subclasses must implement fetch_raw_html")

    def validate_and_process_page(self):
        """Fetches and validates the page content, then processes it into BeautifulSoup."""
        logging.info(f"🔍 Fetching {self.provider_name} page...")
        try:
            html = self.fetch_raw_html()
            return BeautifulSoup(html, "html.parser")
        except Exception as e:
            logging.error(f"⚠️ Scraping failed: Unable to fetch {self.provider_name} page: {e}")
            send_telegram_message(self.telegram_bot_token, self.telegram_chat_id,
                                  f"⚠️ Error: Failed to fetch {self.provider_name} page.\n{e}")
            raise

    def get_opportunity_count(self):
        """Handles exception and calls subclass-specific logic."""
        try:
            soup = self.validate_and_process_page()
            return self.extract_opportunity_count(soup)
        except Exception as e:
            logging.error(f"⚠️ Failed to extract opportunities count: {e}")
            send_telegram_message(self.telegram_bot_token, self.telegram_chat_id,
                                  f"⚠️ Warning: Failed to scrape {self.provider_name}. Structure may have changed.")
            raise

    def extract_opportunity_count(self, soup):
        """Must be implemented by subclasses."""
        raise NotImplementedError("Subclasses must implement extract_opportunity_count")

    def check_and_notify(self):
        """Checks for new opportunities and sends a notification if the count changes."""
        logging.info("🔍 Checking for new opportunities...")

        last_opps = get_gist_value(self.gist_id, self.provider_name, self.github_token)
        new_opps = self.get_opportunity_count()

        if new_opps > last_opps:
            message = f"🔺 New {self.provider_name} opportunities available: {new_opps}!"
            send_telegram_message(self.telegram_bot_token, self.telegram_chat_id, message)
            update_gist_value(self.gist_id, self.provider_name, self.github_token, new_opps)
        elif new_opps < last_opps:
            message = f"🔻 Some {self.provider_name} opportunities have been removed. New count: {new_opps}."
            logging.info(message)
            send_telegram_message(self.telegram_bot_token, self.telegram_chat_id, message)
            update_gist_value(self.gist_id, self.provider_name, self.github_token, new_opps)
        else:
            logging.info("ℹ️ No new opportunities or same as last notification. No message sent.")

    def run(self):
        """Main entry point to check for opportunities."""
        if not all([self.telegram_bot_token, self.telegram_chat_id, self.gist_id, self.github_token]):
            logging.error("❌ Missing one or more required environment variables! Exiting.")
            exit(1)

        try:
            self.check_and_notify()
        except Exception as e:
            logging.error(f"🚨 Fatal Error: {e}")
            exit(1)
