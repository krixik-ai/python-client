from dotenv import load_dotenv
import os
from pathlib import Path

test_base_dir = os.path.dirname(os.path.abspath(__file__))
env_path = Path(os.path.abspath(__file__)).parent.parent
env_file_path = os.path.join(env_path, ".env")
load_dotenv(env_file_path)
USER_API_KEY = os.getenv("USER_API_KEY")
USER_API_URL = os.getenv("USER_API_URL")
USER_ID = os.getenv("USER_ID")
user_stage = "dev"
