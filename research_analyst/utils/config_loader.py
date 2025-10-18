import os
from pathlib import Path
import yaml

def _project_root() -> Path:
    return Path(__file__).resolve().parents[1]

def load_config(config_path:str | None = None) -> dict:

    env_path= os.getenv("PATH_TO_CONFIG")

    if config_path is None:
        config_path = env_path or str(_project_root() / "config" / "configuration.yaml")
 
    path=Path(config_path)
    if not path.absolute():
        path=_project_root() / path


    with open(path, 'r', encoding='utf-8') as file:
        config = yaml.safe_load(file) or {}
    return config

# config=load_config()  # Load config at module import time
# print(config)