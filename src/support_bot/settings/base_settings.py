from typing import Any, Tuple, Type
import json
from pydantic import Field, SecretStr
from pydantic_settings import (
    BaseSettings,
    PydanticBaseSettingsSource,
    SettingsConfigDict,
    YamlConfigSettingsSource,
)


class BaseAppSettings(BaseSettings):
    env: SecretStr = Field(
        default=SecretStr(""),
        description="Secret value for the environment type.",
        alias="ENV_TYP",
    )

    model_config = SettingsConfigDict(
        env_file="conf/.env",
        env_file_encoding="utf-8",
        yaml_file="conf/config.yaml",
        yaml_file_encoding="utf-8",
        extra="ignore",
    )

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls: Type[BaseSettings],
        init_settings: PydanticBaseSettingsSource,
        env_settings: PydanticBaseSettingsSource,
        dotenv_settings: PydanticBaseSettingsSource,
        file_secret_settings: PydanticBaseSettingsSource,
    ) -> Tuple[PydanticBaseSettingsSource, ...]:
        return (
            init_settings,
            dotenv_settings,
            YamlConfigSettingsSource(settings_cls),
            env_settings,
            file_secret_settings,
        )


class BaseYamlSettings(BaseAppSettings):
    config_path: str

    def get_config_dict(self) -> dict[str, Any]:
        return {}