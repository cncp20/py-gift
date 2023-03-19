import os
import json
import time
from common.utils import check_file, timestamp_to_string
from common.error import UserExistsError, RoleExistsError, LevelError
from common.consts import ROLES,FIRST_LEVEL,SECOND_LEVEL

class Base(object):
    def __init__(self, user_json, gift_json):
        self.user_json = user_json
        self.gift_json = gift_json

        self._check_user_json()
        self._check_gift_json()
        self._init_gifts()

    def _check_user_json(self):
        check_file(self.user_json)

    def _check_gift_json(self):
        check_file(self.gift_json)

    def __read_users(self, time_to_str=False):
        with open(self.user_json, "r") as f:
            data = json.loads(f.read())
        if time_to_str:
            for username, v in data.items():
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
        
        users = self.__read_users()

        if user["username"] in users:
            raise UserExistsError("username %s has exists" % user["username"])
        
        users.update({
            user["username"]: user
        })
        self._save(users, self.user_json)

    def _change_role(self, username, role):
        users = self.__read_users()
        user = users.get(username)
        if not user:
            raise UserExistsError("username %s not exist" %  username)
        if role not in ROLES:
            raise RoleExistsError("role %s not exist" % role)
        user["role"] = role
        user["update_time"] = time.time()
        users[username] = user
        self._save(users, self.user_json)
        return True

    def _change_active(self, username):
        users = self.__read_users()
        user = users.get(username)
        if not user:
            raise UserExistsError("username %s not exist" %  username)
        user["active"] = not user["active"]
        user["update_time"] = time.time()
        users[username] = user
        self._save(users, self.user_json)
        return True

    def _delete_user(self, username):
        users = self.__read_users()
        user = users.get(username)
        if not user:
            raise UserExistsError("username %s not exist" %  username)
        del_user = users.pop(username)
        self._save(users, self.user_json)
        return del_user    
    
    def _read_gifts(self):
        with open(self.gift_json, "r") as f:
            data = json.loads(f.read())
        return data

    def _init_gifts(self):
        data = {
            "level1": {
                "level1": {},
                "level2": {},
                "level3": {},
            },
            "level2": {
                "level1": {},
                "level2": {},
                "level3": {},
            },
            "level3": {
                "level1": {},
                "level2": {},
                "level3": {},
            },
            "level4": {
                "level1": {},
                "level2": {},
                "level3": {},
            }
        }
        gifts = self._read_gifts()
        if len(gifts) == 0:
            self._save(data, self.gift_json)

    def _write_gift(self, first_level, second_level, gift_name, gift_count):
        if first_level not in FIRST_LEVEL or second_level not in SECOND_LEVEL:
            raise LevelError("level not exist")
        if gift_count<= 0:
            gift_count = 1
        gifts = self._read_gifts()
        current_gift_pool = gifts[first_level][second_level]
        if gift_name in current_gift_pool:
            print(current_gift_pool)
            current_gift_pool[gift_name] = {
                "name": gift_name,
                "count": current_gift_pool[gift_name]["count"] + gift_count
            }
        else:
            current_gift_pool[gift_name] = {
                "name": gift_name,
                "count": gift_count
            }
        self._save(gifts, self.gift_json)

    def _check_and_getgift(self, first_level, second_level, gift_name):
        gifts = self._read_gifts()
        level_one = gifts[first_level]
        level_two = level_one[second_level]
        if gift_name not in level_two:
            return False
        return {
            "level_one": level_one,
            "level_two": level_two,
            "gifts": gifts
        }
    
    def _gift_update(self, first_level, second_level, gift_name, gift_count=1, is_admin=False):
        data = self._check_and_getgift(first_level, second_level, gift_name)
        if data == False:
            return False
        current_gift_pool = data.get("level_one")
        current_second_gift_pool = data.get("level_two")
        gifts = data.get("gifts")
        current_gift = current_second_gift_pool.get(gift_name)
        if is_admin:
            if gift_count <= 0:
                raise Exception("gift count not 0")
            current_gift["count"] = gift_count
        else:
            if current_gift["count"] - gift_count < 0:
                raise ValueError("gift count can not be nagative")
            current_gift["count"] -= gift_count

        current_gift_pool[second_level] = current_second_gift_pool
        gifts[first_level] = current_gift_pool
        self._save(gifts, self.gift_json)


    def _delete_gift(self, first_level, second_level, gift_name):
        data = self._check_and_getgift(first_level, second_level, gift_name)

        if data == False:
            return False
        current_gift_pool = data.get("level_one")
        current_second_gift_pool = data.get("level_two")
        gifts = data.get("gifts")

        delete_gift_data = current_second_gift_pool.pop(gift_name)
        current_gift_pool[second_level] = current_second_gift_pool
        gifts[first_level] = current_gift_pool
        self._save(gifts, self.gift_json)
        return delete_gift_data

    def _save(self, data, path):
        json_data = json.dumps(data)
        with open(path, "w") as f:
            f.write(json_data)

if __name__ == "__main__":
    user_path = os.path.join(os.getcwd(), "storage", "user.json")
    gift_path = os.path.join(os.getcwd(), "storage", "gift.json")
    # print(user_path, gift_path)
    base = Base(user_path, gift_path)


    base._write_user(username="user1", role="normal")

    # users = base.__read_users(True)
    # print(users)

    # base._change_active("admin")
    # base._delete_user("admin1")

    # base._init_gifts()

    # base._gift_update("level1", "level1", "airpods", 2)