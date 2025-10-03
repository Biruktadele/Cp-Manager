# myapp/cron.py
import requests
from .models import Problem

def fetch_problem():
    print("Cron job ran successfully!")
    url = "https://alfa-leetcode-api.onrender.com/daily"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
    except requests.RequestException as exc:
        print("❌ Failed to fetch problem:", exc)
        return

    data = resp.json() or {}
    dl = data.get("questionLink")
    if not dl:
        print("❌ No problem link found in response")
        return
    # prefer update_or_create so repeated runs don't create duplicates
    Problem.objects.update_or_create(
        deep_link=dl,
        defaults={
            "title": data.get("questionTitle", "No title"),
            "description": data.get("body", "No description"),
            "difficulty": data.get("difficulty", "Unknown"),
            "is_daily_problem": True,
            "topic_tags": data.get("topicTags", []) or [],
            "deep_link": data.get("questionLink") or "",
        },
    )
    print("✅ Problem fetched and saved successfully")

def check_health():
    print("Health check ran successfully!")
    url = "http://127.0.0.1:8000/cp/health/"
    try:
        resp = requests.get(url, timeout=10)
        resp.raise_for_status()
        print("✅ Health check successful:", resp.json())
    except requests.RequestException as exc:
        print("❌ Health check failed:", exc)