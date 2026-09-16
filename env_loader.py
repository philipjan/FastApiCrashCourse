import os

from dotenv import load_dotenv


class EnvLoader:
    @staticmethod
    def initializeEnvs():
        load_dotenv()
        print(f"load_dotenv() loaded")
        print(f"Database URL: {os.getenv('POSTGRES_BASE_URL')}")
