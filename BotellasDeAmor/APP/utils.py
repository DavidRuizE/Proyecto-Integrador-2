# utils.py
from urllib.parse import urlencode

def query_transform(request_get):
    return urlencode(request_get)
