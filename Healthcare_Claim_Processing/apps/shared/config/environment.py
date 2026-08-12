from pathlib import Path

from dotenv import load_dotenv


def load_environment() -> None:
    """
    Load application environment variables from apps/.env.
    """

    apps_dir = Path(__file__).resolve().parents[2]
    env_file = apps_dir / ".env"

    load_dotenv(env_file)