import os
import uuid
import logging
import logging.config

from support_bot.settings.base_settings import BaseAppSettings
from support_bot.controllers.graph import GRAPH

logging.config.fileConfig("conf/logging.conf")
logger = logging.getLogger("hotmart-challenge")

base_settings = BaseAppSettings()
open_api_key = base_settings.open_api_key.get_secret_value()
os.environ["OPENAI_API_KEY"] = open_api_key


def main() -> None:
    user_input = input("Digite sua pergunta: ")

    logger.info("Agent thinking...")
    config = {"configurable": {"thread_id": uuid.uuid4()}}

    result = GRAPH.invoke(
        {
            "messages": [
                {
                    "role": "user",
                    "content": user_input,
                }
            ]
        },
        config=config,
    )

    result["messages"][-1].pretty_print()


if __name__ == "__main__":
    main()
