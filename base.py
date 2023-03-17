import os
from common.utils import check_file

class Base(object):
    def __init__(self, user_json, gift_json):
        self.user_json = user_json
        self.gift_json = gift_json

        self._check_user_json()
        self._check_gift_json()

    def _check_user_json(self):
        check_file(self.user_json)

    def _check_gift_json(self):
        check_file(self.gift_json)

if __name__ == "__main__":
    user_path = os.path.join(os.getcwd(), "storage", "user.json")
    gift_path = os.path.join(os.getcwd(), "storage", "gift.json")
    print(user_path, gift_path)
    base = Base(user_path, gift_path)