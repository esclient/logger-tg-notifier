from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
        case_sensitive=False,
    )

    TOKEN: str = Field(validation_alias="TG_BOT_TOKEN")
    CHAT_ID: str = Field(validation_alias="TG_CHAT_ID")
    THREAD_ID: int = Field(validation_alias="TG_THREAD_ID")
    HOST: str = Field(validation_alias="HOST")
    PORT: int = Field(validation_alias="PORT")
