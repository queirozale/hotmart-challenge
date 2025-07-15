import os
import logging
import logging.config

logging.config.fileConfig("conf/logging.conf")
logger = logging.getLogger("hotmart-challenge")


def main() -> None:
    logger.info(f"Agent thinking...")


if __name__ == "__main__":
    main()

