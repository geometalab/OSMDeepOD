import environ
import os

root = environ.Path(os.getcwd())
cwenv = environ.Env(
    REDIS_HOST=(str, 'db'),
    REDIS_PORT=(str, '6379'),
    REDIS_PASS=(str, 'crosswalks'),
    OUTPUT_DIR=(str, '.'),
)
environ.Env.read_env(root('.env'))  # reading .env file
