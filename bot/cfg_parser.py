from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr
from dotenv import load_dotenv

# Загружаем переменные окружения из файла .env
load_dotenv()


class Settings(BaseSettings):
    # Токен бота, загружается из переменных окружения
    bot_token: SecretStr

    # Конфигурация модели для pydantic: путь к .env и кодировка
    model_config = SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')


# Создаем экземпляр конфигурации для использования в проекте
config = Settings() # type: ignore
