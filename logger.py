import logging
import os
import json
from datetime import datetime

def get_config():
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "backend", "APIs_and_configs", "config.json"))
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

config = get_config()
logs_path = config.get("logs_path", os.path.abspath(os.path.join(os.path.dirname(__file__), "logs")))

if not os.path.exists(logs_path):
    os.makedirs(logs_path, exist_ok=True)

log_file = os.path.join(logs_path, f"kairo_{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.log")

logger = logging.getLogger("KairoAI")
logger.setLevel(logging.INFO)

if config.get("save_logs", True):
    file_handler = logging.FileHandler(log_file, encoding='utf-8')
    file_handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)
