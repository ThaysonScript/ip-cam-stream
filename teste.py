from pyintelbras import IntelbrasAPI
from pyintelbras.helpers import parse_response
from dotenv import load_dotenv
import logging, sys, os

stream = logging.StreamHandler(sys.stdout)
stream.setLevel(logging.DEBUG)
log = logging.getLogger('pyintelbras')
log.addHandler(stream)
log.setLevel(logging.DEBUG)

load_dotenv()

camera_ip = os.getenv("CAMERA_IP")
camera_user = os.getenv("CAMERA_USER")
camera_password = os.getenv("CAMERA_PASSWORD")

intelbras = IntelbrasAPI(f"http://{camera_ip}")
intelbras.login(f"{camera_user}", f"{camera_password}")

response = intelbras.configManager.get(action='getConfig', name='ChannelTitle')

# print(response.text)

# response_formmat = parse_response(response.text)
# print(response_formmat)

# print(response_formmat.get('table').get('ChannelTitle')[0].get('Name'))

response = intelbras.snapshot(channel=1, type=0)

print(response.status_code)

if response.status_code == 200:
    with open("img.jpeg", "wb") as bf:
        bf.write(response.content)