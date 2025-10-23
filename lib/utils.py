import os, re, unicodedata, json, datetime, csv, pathlib
from dateutil import tz
from typing import Dict, Any, Optional, List
from config import LOG_DIR, LOG_RETENTION_DAYS, LOG_MAX_BYTES

def ensure_dir(path:str):
    os.makedirs(path, exist_ok=True)

def normalize_key(name:str) -> str:
    s = name.strip().lower()
    s = ''.join(c for c in unicodedata.normalize('NFKD', s) if not unicodedata.combining(c))
    s = re.sub(r'\s+', ' ', s)
    return s

def today_log_path() -> str:
    ensure_dir(LOG_DIR)
    d = datetime.datetime.utcnow().strftime("%Y-%m-%d")
    base = os.path.join(LOG_DIR, f"{d}.csv")
    if os.path.exists(base) and os.path.getsize(base) > LOG_MAX_BYTES:
        i = 1
        while os.path.exists(os.path.join(LOG_DIR, f"{d}_part{i}.csv")) and os.path.getsize(os.path.join(LOG_DIR, f"{d}_part{i}.csv")) > LOG_MAX_BYTES:
            i += 1
        return os.path.join(LOG_DIR, f"{d}_part{i}.csv")
    return base

def write_log(event:str, user_key:str="", meta:Optional[Dict[str,Any]]=None):
    path = today_log_path()
    newfile = not os.path.exists(path)
    with open(path, "a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if newfile:
            w.writerow(["ts","event","user_key","meta_json"])
        ts = datetime.datetime.utcnow().isoformat()
        w.writerow([ts, event, user_key, json.dumps(meta or {}, ensure_ascii=False)])

def purge_old_logs():
    ensure_dir(LOG_DIR)
    now = datetime.datetime.utcnow()
    for fn in os.listdir(LOG_DIR):
        if not fn.endswith(".csv"): continue
        path = os.path.join(LOG_DIR, fn)
        try:
            date_part = fn.split(".csv")[0].split("_part")[0]
            d = datetime.datetime.strptime(date_part, "%Y-%m-%d")
            if (now - d).days > LOG_RETENTION_DAYS:
                os.remove(path)
        except:
            continue
