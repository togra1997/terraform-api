from functools import wraps

import dotenv


def load_env(func):
    """
    dotenvをロードするデコレーター
    """

    @wraps(func)
    def wrapper(*args, **kwargs):
        dotenv.load_dotenv()
        return func(*args, **kwargs)

    return wrapper
