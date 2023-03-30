import requests
import datetime

url = "https://thispersondoesnotexist.com/image"

path = "e:/Images/DownRandom"

while True:
    r = requests.get(url, stream=True)
    fileName = datetime.datetime.now()
    with open(r"{}/{}.jpg".format(path,fileName), "wb") as f:
        for chunk in r.iter_content(chunk_size=512):
            f.write(chunk)
