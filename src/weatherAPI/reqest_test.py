import requests
import requests
r = requests.get("http://abehiroshi.la.coocan.jp/")
#view encoded text data
print(r.text.encode('utf-8'))
#view http connection status
print(r.status_code, type(r.status_code))
#view data header
print(r.headers)
#view data character code
print(r.encoding)
#view unencoded text data
print(r.content)