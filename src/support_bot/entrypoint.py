import os
import logging
import logging.config

from support_bot.settings.base_settings import BaseAppSettings

logging.config.fileConfig("conf/logging.conf")
logger = logging.getLogger("hotmart-challenge")

base_settings = BaseAppSettings()
env = base_settings.env.get_secret_value()

def main() -> None:
    logger.info(f"Agent thinking...")
    logger.info(env)

if __name__ == "__main__":
    main()