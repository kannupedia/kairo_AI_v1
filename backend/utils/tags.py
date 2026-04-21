import re
import requests
import json
import os
from datetime import datetime, timezone

def get_config():
    config_path = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "APIs_and_configs", "config.json"))
    try:
        with open(config_path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return {}

config = get_config()
username = config.get("username", "User")

def get_location():
    try:
        res = requests.get("http://ip-api.com/json/", timeout=5)
        if res.status_code == 200:
            data = res.json()
            return f"{data.get('city', '')}, {data.get('regionName', '')}, {data.get('country', '')}".strip(", ")
    except Exception:
        pass
    return "Unknown Location"

def get_country_time_by_name(country):
    try:
        res = requests.get(f"https://restcountries.com/v3.1/name/{country}", timeout=5)
        if res.status_code == 200:
            data = res.json()[0]
            tz = data.get("timezones", ["UTC"])[0] 
            utcnow = datetime.now(timezone.utc)
            if tz.startswith("UTC"):
                offset = tz.replace("UTC", "")
                if offset:
                    sign = 1 if offset[0] == "+" else -1
                    parts = offset[1:].split(":")
                    if len(parts) == 2:
                        hours, minutes = map(int, parts)
                        delta = sign * (hours * 3600 + minutes * 60)
                        local_time = utcnow.timestamp() + delta
                        return datetime.fromtimestamp(local_time, timezone.utc).strftime("%I:%M %p")
            return utcnow.strftime("%I:%M %p")
    except Exception:
        pass
    return datetime.now(timezone.utc).strftime("%I:%M %p")

def process_tags(text):
    if not isinstance(text, str):
        return text

    # Handle explicit tags
    text = text.replace("{[(__USERNAME__)]}", username)
    
    now = datetime.now()
    text = text.replace("{[(__DATE__)]}", now.strftime("%Y-%m-%d"))
    text = text.replace("{[(__TIME__)]}", now.strftime("%I:%M %p"))
    
    # Location tag
    if "{[(__LOCATION__)]}" in text:
        loc = get_location()
        text = text.replace("{[(__LOCATION__)]}", loc)
    elif "{[(LOCATION)]}" in text:
        loc = get_location()
        text = text.replace("{[(LOCATION)]}", loc)
        
    # Country Time tags e.g., {[(__INDIA_TIME__)]}
    pattern = r"\{\[\(__([a-zA-Z]+)_TIME__\)\]\}"
    matches = re.finditer(pattern, text)
    for match in matches:
        country_name = match.group(1)
        country_time = get_country_time_by_name(country_name)
        text = text.replace(match.group(0), country_time)
        
    return text
