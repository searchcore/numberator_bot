from os import getenv
from sys import exit

def get_token_from_env(env_name: str):
    bot_token = getenv(env_name)
    if not bot_token:
        exit(f'Error: no token provided in env variable {env_name}')
    return bot_token

