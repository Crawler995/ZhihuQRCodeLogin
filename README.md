# Zhihu QRCode Login

One line to login Zhihu by QRCode.

## Install
`pip install zhihu-qrcode-login`

## Usage
```python
from zhihu_qrcode_login import login_handler
import logging

# if remember_me = True, the cookies will be saved in your disk, 
# and next time you can login without scanning QRCode.
# if you pass a logger into it, it can output some useful log.
# return requests.Session
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger('test')
session = login_handler.login(remember_me=True, logger=logger)
# and later you can also use get_session() to get the session.
# session = login_handler.get_session()

# use it!
# you can use get_visit_headers() to get the headers which can visit Zhihu successfully.
session.get('https://www.zhihu.com/collections/mine', headers=login_handler.get_visit_headers())
```

## TODO
1. Handle the condition that users scan the QRCode but cancel the login confirmation.
2. Find more elegant approach to open and close the QRCode.