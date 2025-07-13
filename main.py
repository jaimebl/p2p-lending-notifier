import importlib
import logging
import pkgutil

import providers
from providers.capital_rise import CapitalRise

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

def run_all_providers():
    """Dynamically discover and run all P2PLendingBase subclasses."""
    for _, module_name, _ in pkgutil.iter_modules(providers.__path__):
        if module_name not in ["p2p_lending_base", "__init__"]:
            logging.info(f"🚀 Running {module_name} provider...")
            module = importlib.import_module(f"providers.{module_name}")
            class_name = module_name.title().replace("_", "")
            scraper_class = getattr(module, class_name)
            scraper_class().check_and_notify()

if __name__ == "__main__":
    CapitalRise().run()
    # run_all_providers()
