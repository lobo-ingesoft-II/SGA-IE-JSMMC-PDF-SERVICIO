from pydantic_settings import BaseSettings
from pydantic import Field

class Settings(BaseSettings):
    mongo_uri: str = Field(..., alias="MONGO_URI")
    url_api_pre_registro: str = Field(..., alias="SERVIDOR_API_PREMATRICULA_URL")

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()

#print("DEBUG settings.mongo_uri:", settings.mongo_uri)
# import os

# env_path = os.path.join(os.path.dirname(__file__), ".env")
# print("¿Existe .env?:", os.path.exists(env_path))
# if os.path.exists(env_path):
#     with open(env_path) as f:
#         print("Contenido de .env:")
#         print(f.read())


# print(settings.mongo_uri)  