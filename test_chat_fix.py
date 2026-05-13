"""Direct test against the RUNNING FastAPI server."""
import requests
import json

BASE = "http://127.0.0.1:8001"

# First, register or login
try:
    reg = requests.post(f"{BASE}/auth/register", json={
        "username": "cleantest",
        "email": "cleantest@test.com",
        "password": "test1234"
    }, timeout=5)
except Exception as e:
    print(f"Connection error: {e}")
    print("Make sure the server is running on port 8001!")
    exit(1)

if reg.status_code == 400:
    reg = requests.post(f"{BASE}/auth/login", json={
        "username": "cleantest",
        "password": "test1234"
    })

data = reg.json()
print(f"Auth response keys: {list(data.keys())}")

# Determine token format (FastAPI uses 'token', Django uses 'access')
token = data.get("token") or data.get("access")
headers = {"Authorization": f"Bearer {token}"}

# Check which backend is running
info_resp = requests.get(f"{BASE}/auth/me", headers=headers)
print(f"Auth /me status: {info_resp.status_code}")

test_messages = [
    "tolong aku",
    "bantu aku", 
    "buatkan aku",
    "aku mohon",
    "mampus",
    "halo apa kabar",
]

print("\n" + "=" * 70)
for msg in test_messages:
    resp = requests.post(f"{BASE}/chat", json={
        "message": msg,
        "language": "id"
    }, headers=headers)
    
    rdata = resp.json()
    reply = rdata.get("reply", "NO REPLY")
    
    # Check if response_source exists (Django-only field)
    has_source = "response_source" in rdata
    source = rdata.get("response_source", "N/A (FastAPI)")
    
    print(f"\nINPUT:  {msg}")
    print(f"SOURCE: {source}")
    print(f"REPLY:  {reply[:150]}")
    print("-" * 70)

print("\nDONE")
