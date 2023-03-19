from base import Base
import os
import random

class User(Base):
    def __init__(self, username, user_json, gift_json):
        self.username = username
        self.gift_random = list(range(1, 101))
        super().__init__(user_json, gift_json)
        self.get_user()

    def get_user(self):
        users = self._Base__read_users()
        user = users[self.username]
        self.user = user
        self.role = user["role"]
        self.active = user["active"]
        self.gifts = user["gifts"]

    def get_gifts(self):
        gifts = self._read_gifts()
        gift_lists = []

        for level_one, level_one_pool in gifts.items():
            for level_two, level_two_pool in level_one_pool.items():
                for gift_name, gift_info in level_two_pool.items():
                    gift_lists.append(gift_name)

        return gift_lists

    def choice_gifts(self):
        first_level = None
        level_one_count = random.choice(self.gift_random)
        if 1 <= level_one_count <= 50:
            first_level = "level1"
        elif 50 < level_one_count <= 80:
            first_level = "level2"
        elif 80 < level_one_count <= 95:
            first_level = "level3"
        elif 95 < level_one_count:
            first_level = "level4"
        else:
            raise Exception("random error")
        gifts = self._read_gifts()
        level_one = gifts[first_level]

        second_level = None
        level_two_count = random.choice(self.gift_random)
        if 1 <= level_two_count <= 50:
            second_level = "level1"
        elif 50 < level_two_count <= 80:
            second_level = "level2"
        elif 80 < level_two_count <= 100:
            second_level = "level3"
        else:
            raise Exception("random error")
        level_two = level_one[second_level]

        if len(level_two) == 0:
            print("没中奖")
            return
        gift_names = []
        for k, _ in level_two.items():
            gift_names.append(k)
        gift_name = random.choice(gift_names)    
        gift_info = level_two[gift_name]
        if gift_info["count"] == 0:
            print("没中奖")
            return
        gift_info["count"] -= 1
        level_two[gift_name] = gift_info
        level_one[second_level] = level_two
        gifts[first_level] = level_one

        self._save(gifts, self.gift_json)
        self.user["gifts"].append(gift_name)
        self.update()
        print(gift_name)

    def update(self):
        users = self._Base__read_users()
        users[self.username] = self.user

        self._save(users, self.user_json)

if __name__ == '__main__':
    user_path = os.path.join(os.getcwd(), "storage", "user.json")
    gift_path = os.path.join(os.getcwd(), "storage", "gift.json")
    user = User("user1", user_path, gift_path)
    # print(user.username, user.role, user.active)

    # result = user.get_gifts()
    # print(result)
    user.choice_gifts()
    