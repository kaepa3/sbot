import os
import time
import json
import hashlib
import hmac
import base64
import uuid
import requests
import datetime
from os.path import exists
from dotenv import load_dotenv
load_dotenv()

dir_name = "./responses"
if not exists(dir_name):
    os.makedirs(dir_name)

token = os.environ.get("OPENTOKEN")
secret = os.environ.get("SECRETKEY")
nonce = str(uuid.uuid4())
t = int(round(time.time() * 1000))
string_to_sign = "{}{}{}".format(token, t, nonce)
string_to_sign = bytes(string_to_sign, "utf-8")
secret = bytes(secret, "utf-8")
sign = base64.b64encode(
    hmac.new(secret, msg=string_to_sign, digestmod=hashlib.sha256).digest()
)

apiHeader = {}
apiHeader["Authorization"] = token
apiHeader["Content-Type"] = "application/json"
apiHeader["charset"] = "utf8"
apiHeader["t"] = str(t)
apiHeader["sign"] = str(sign, "utf-8")
apiHeader["nonce"] = nonce

response = requests.get("https://api.switch-bot.com/v1.1/devices", headers=apiHeader)
devices = response.json()

timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
response_file = f"{dir_name}/devices_{timestamp}.json"
with open(response_file, "w") as f:
    json.dump(devices, f)

print("Success get devices list.")
