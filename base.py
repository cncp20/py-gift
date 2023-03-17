import os
import json
import time
from common.utils import check_file, timestamp_to_string
from common.error import UserExistsError

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

    def _read_users(self, time_to_str=False):
        with open(self.user_json, "r") as f:
            data = json.loads(f.read())
        if time_to_str:
            for k, v in data.items():
                v["create_time"] = timestamp_to_string(v["create_time"])
                v["update_time"] = timestamp_to_string(v["update_time"])
            data[username] = v
        return data

    def _write_user(self, **user):
        if "username" not in user:
            raise ValueError("username required")
        if "role" not in user:
            raise ValueError("role required")
        user["active"] = True
        user["create_time"] = time.time()
        user["update_time"] = time.time()
        user["gifts"] = []
        
        users = self._read_users()

        if user["username"] in users:
            raise UserExistsError("username %s has exists" % user["username"])
        
        users.update({
            user["username"]: user
        })

        json_users = json.dumps(users)
        with open(self.user_json, "w") as f:
            f.write(json_users)

if __name__ == "__main__":
    user_path = os.path.join(os.getcwd(), "storage", "user.json")
    gift_path = os.path.join(os.getcwd(), "storage", "gift.json")
    print(user_path, gift_path)
    base = Base(user_path, gift_path)

    # users = base._read_users()
    # print(users)

    base._write_user(username="admin", role="admin")