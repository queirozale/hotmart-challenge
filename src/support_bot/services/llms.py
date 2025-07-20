from langchain.chat_models import init_chat_model
import os

from support_bot.settings.base_settings import BaseAppSettings

base_settings = BaseAppSettings()
open_api_key = base_settings.open_api_key.get_secret_value()
os.environ["OPENAI_API_KEY"] = open_api_key

RESPONSE_MODEL_VERSION = "openai:gpt-4.1"
GRADER_MODEL_VERSION = "openai:gpt-4.1"
TEMPERATURE = 0

RESPONDE_MODEL = init_chat_model(RESPONSE_MODEL_VERSION, temperature=TEMPERATURE)
GRADER_MODEL = init_chat_model(GRADER_MODEL_VERSION, temperature=TEMPERATURE)
