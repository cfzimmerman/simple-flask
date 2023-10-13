import requests
from dotenv import load_dotenv
from typing import List
from os import environ
from definitions import SuccessResponse, ErrorResponse, PostColor, GetColor

load_dotenv()

server_url: str = environ.get("SERVER_URL")

# Test version
version = requests.get(f"{server_url}/")
parsed: SuccessResponse = version.json()
assert parsed["code"] // 100 == 2

"""
class PostColor(TypedDict):
    user_uuid: str
    color: str
"""

# Test post
users: List[PostColor] = [
    {"user_uuid": "1", "color": "purple"},
    {"user_uuid": "2", "color": "red"},
    {"user_uuid": "3", "color": "white"},
    {"user_uuid": "4", "color": "blue"},
]

for user in users:
    res: SuccessResponse = requests.post(f"{server_url}/set_color", json=user).json()
    assert res["code"] // 100 == 2

for user in users:
    res: SuccessResponse = requests.get(f"{server_url}/get_color", params=user).json()
    assert res["code"] // 100 == 2
    assert res["data"] == user["color"]

# Test errors
unmatched_user: ErrorResponse = requests.get(f"{server_url}/get_color").json()
assert unmatched_user["code"] // 100 == 4

missing_body: ErrorResponse = requests.post(f"{server_url}/set_color", json="").json()
assert missing_body["code"] // 100 == 4

print("✅ All tests pass")
