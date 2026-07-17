from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    app_name: str = "Tattle Tales"
    debug: bool = True

    host: str = "0.0.0.0"
    port: int = 8000

    #ollama
    ollma_base_url: str = "http://localhost:11434"
    ollama_model: str = "qwen2:7b"

    class Config:
        env_file = ".env"

Settings = Settings()