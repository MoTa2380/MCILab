from dotenv import load_dotenv, find_dotenv
import os


class EnvironmentVariableError(Exception):
    """Custom exception for environment variable errors."""
    pass


class Settings:
    def __init__(self) -> None:
        dotenv_path = find_dotenv()
        if not dotenv_path:
            raise FileNotFoundError(".env file was not found.")

        load_dotenv(dotenv_path=dotenv_path)

    def get_environment_variable(self, name: str) -> str:
        
        if not name:
            raise ValueError("The name of the environment variable must be specified.")


        value = os.getenv(name)
        if value is None:
            raise EnvironmentVariableError(f"Environment variable {name} is not set.")

        return value



settings = Settings()