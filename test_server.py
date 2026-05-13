import urllib.request
import urllib.error
import json
import sys

BASE_URL = "http://127.0.0.1:8000"

def fetch(method, url, data=None, headers=None):
    if headers is None: headers = {}
    if data is not None:
        data = json.dumps(data).encode("utf-8")
        headers["Content-Type"] = "application/json"
    req = urllib.request.Request(url, data=data, headers=headers, method=method)
    try:
        with urllib.request.urlopen(req, timeout=5) as response:
            return response.status, json.loads(response.read().decode())
    except urllib.error.HTTPError as e:
        try:
            return e.code, json.loads(e.read().decode())
        except:
            return e.code, e.read().decode()
    except urllib.error.URLError as e:
        return 0, str(e)
    except Exception as e:
        return 0, str(e)

try:
    print("Testing server...", flush=True)
    status, res = fetch("GET", BASE_URL)
    if status == 0:
        print("Server is not running on localhost:8000 or timed out:", res)
        sys.exit(0)
    print("Server is up!", status)

    # Register
    print("Registering...", flush=True)
    status, reg = fetch("POST", f"{BASE_URL}/auth/register", data={
        "username": "testuser_debug2",
        "email": "test_debug2@example.com",
        "password": "password"
    })
    
    if status == 400: # Already exists
        print("User already exists, logging in...", flush=True)
        status, reg = fetch("POST", f"{BASE_URL}/auth/login", data={
            "username": "testuser_debug2",
            "password": "password"
        })
    
    if status not in (200, 201):
        print("Auth failed:", reg)
        sys.exit(1)
        
    token = reg["token"]
    print("Got token:", token[:10], "...")

    # Post to chat
    print("Sending chat message...", flush=True)
    status, chat_res = fetch("POST", f"{BASE_URL}/chat", data={
        "message": "Halo, ini tes debug.",
        "language": "id"
    }, headers={"Authorization": f"Bearer {token}"})

    print("Chat status:", status)
    print("Chat response:", chat_res)

except Exception as e:
    import traceback
    traceback.print_exc()
