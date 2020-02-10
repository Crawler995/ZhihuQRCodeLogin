# Zhihu QRCode Login

One line to login Zhihu by QRCode.

## Usage
```python
from zhihu_qrcode_login import login_handler

# if remember_me = True, the cookies will be saved in your disk, 
# and next time you can login without scanning QRCode.
# return requests.Session
session = login_handler.login(remember_me=True)
# and later you can also use get_session() to get the session.
# session = login_handler.get_session()

# use it!
# you can use get_visit_headers() to get the headers which can visit Zhihu successfully.
session.get('https://www.zhihu.com/collections/mine', headers=login_handler.get_visit_headers())
```

## TODO
1. After users scan the QRCode and confirm login on their devices, close the QRCode automatically.