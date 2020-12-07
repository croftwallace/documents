#!/usr/bin/python

import requests

url="http://127.0.0.1:5000/api/img/search"

files={'file': ('00b4eedd51f64e548e74d9c0a4de0290.JPG', open('00b4eedd51f64e548e74d9c0a4de0290.JPG', 'rb'), 'image/jpg', {})}

payload={'Table': "zjsjk"}

r = requests.post(url, data=payload, files=files)

print(r)
print(r.content)

