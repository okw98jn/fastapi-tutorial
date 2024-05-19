import os

from dotenv import load_dotenv


def get_env_variable(name: str) -> str:
    """
    環境変数を取得する

    Args:
        name (str): 環境変数名

    Returns:
        str: 環境変数の値

    Raises:
        EnvironmentError: 環境変数が設定されていない場合に発生する例外
    """
    load_dotenv()

    value = os.environ.get(name)

    if value is None:
        error_message = f"Environment variable {name} not set."
        raise EnvironmentError(error_message)

    return value
