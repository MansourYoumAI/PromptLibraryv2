from typing import List, Dict, Any, Optional
from config import METIERS, CATEGORIES, AUTHORS
from lib.utils import normalize_key

DB = {
    "metiers": METIERS.copy(),
    "categories": CATEGORIES.copy(),
    "authors": AUTHORS.copy(),
    "prompts": [],
    "submissions": [],
    "bookmarks": [],
    "ratings": []
}

def list_metiers(active_only=True) -> List[Dict[str,Any]]:
    return [m for m in DB["metiers"] if (m.get("is_active",True) or not active_only)]

def list_categories(metier_id:str, active_only=True) -> List[Dict[str,Any]]:
    return [c for c in DB["categories"] if c["metier_id"]==metier_id and (c.get("is_active",True) or not active_only)]

def get_or_create_category(metier_id:str, name:str) -> Dict[str,Any]:
    key = normalize_key(name)
    for c in DB["categories"]:
        if c["metier_id"]==metier_id and normalize_key(c["name"])==key:
            return c
    new = {"id": key.replace(" ","-"), "metier_id": metier_id, "name": name.strip(), "is_active": True}
    DB["categories"].append(new)
    return new

def list_authors(active_only=True) -> List[Dict[str,Any]]:
    return [a for a in DB["authors"] if (a.get("is_active",True) or not active_only)]

def get_or_create_author(display_name:str) -> Dict[str,Any]:
    key = normalize_key(display_name)
    for a in DB["authors"]:
        if a["normalized_key"]==key:
            return a
    new = {"id": f"auth_{key.replace(' ','-')}", "display_name": display_name.strip(), "normalized_key": key, "is_active": True}
    DB["authors"].append(new)
    return new

def create_submission(payload:Dict[str,Any]) -> Dict[str,Any]:
    author = get_or_create_author(payload.get("author_display_name","Unknown"))
    sub = {
        "id": f"sub_{len(DB['submissions'])+1:05d}",
        "title": payload["title"],
        "description": payload.get("description",""),
        "metier_id": payload["metier_id"],
        "category_id": payload["category"]["id"],
        "category_name": payload["category"]["name"],
        "author_id": author["id"],
        "author_display_name_snapshot": author["display_name"],
        "craft_context": payload["craft_context"],
        "craft_role": payload["craft_role"],
        "craft_action": payload["craft_action"],
        "craft_format": payload["craft_format"],
        "craft_tone": payload["craft_tone"],
        "full_text": payload["full_text"],
        "status": "pending",
        "review_comment": "",
        "created_by": payload.get("user_key",""),
    }
    DB["submissions"].append(sub)
    return sub

def list_submissions(status:Optional[str]=None) -> List[Dict[str,Any]]:
    items = DB["submissions"]
    if status:
        items = [s for s in items if s["status"]==status]
    return items

def approve_submission(sub_id:str) -> Optional[Dict[str,Any]]:
    for s in DB["submissions"]:
        if s["id"]==sub_id:
            s["status"]="approved"
            p = {
                "id": f"p_{len(DB['prompts'])+1:05d}",
                "title": s["title"],
                "description": s["description"],
                "metier_id": s["metier_id"],
                "category_id": s["category_id"],
                "category_name": s["category_name"],
                "author_id": s["author_id"],
                "author_display_name_snapshot": s["author_display_name_snapshot"],
                "craft_context": s["craft_context"],
                "craft_role": s["craft_role"],
                "craft_action": s["craft_action"],
                "craft_format": s["craft_format"],
                "craft_tone": s["craft_tone"],
                "full_text": s["full_text"],
                "avg_rating": 0.0,
                "uses_total": 0,
                "status": "published",
                "version": "1.0"
            }
            DB["prompts"].append(p)
            s["published_prompt_id"] = p["id"]
            return p
    return None

def list_prompts(metier_id:str=None, category_id:str=None) -> List[Dict[str,Any]]:
    items = [p for p in DB["prompts"] if p["status"]=="published"]
    if metier_id:
        items = [p for p in items if p["metier_id"]==metier_id]
    if category_id:
        items = [p for p in items if p["category_id"]==category_id]
    return items

def get_prompt(prompt_id:str):
    for p in DB["prompts"]:
        if p["id"]==prompt_id:
            return p
    return None

def rate_prompt(user_key:str, prompt_id:str, stars:int):
    found = None
    for r in DB["ratings"]:
        if r["user_key"]==user_key and r["prompt_id"]==prompt_id:
            r["stars"]=stars
            found = r
            break
    if not found:
        DB["ratings"].append({"user_key": user_key, "prompt_id": prompt_id, "stars": stars})
    vals = [r["stars"] for r in DB["ratings"] if r["prompt_id"]==prompt_id]
    for p in DB["prompts"]:
        if p["id"]==prompt_id:
            p["avg_rating"] = sum(vals)/len(vals) if vals else 0.0
            break

def toggle_bookmark(user_key:str, prompt_id:str) -> bool:
    for i,b in enumerate(DB["bookmarks"]):
        if b["user_key"]==user_key and b["prompt_id"]==prompt_id:
            DB["bookmarks"].pop(i)
            return False
    DB["bookmarks"].append({"user_key": user_key, "prompt_id": prompt_id})
    return True

def list_bookmarks(user_key:str):
    ids = [b["prompt_id"] for b in DB["bookmarks"] if b["user_key"]==user_key]
    return [p for p in DB["prompts"] if p["id"] in ids]
