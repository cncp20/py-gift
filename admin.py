import os
from base import Base


class Admin(Base):
    def __init__(self, username, user_json, gift_json):
        self.username = username
        super().__init__(user_json, gift_json)
        self.get_user()

    def get_user(self):
        users = self._Base__read_users()
        current_user = users.get(self.username)
        if current_user == None:
            raise Exception("no user")
        if not current_user.get("active"):
            raise Exception("not active")
        if current_user.get("role") != "admin":
            raise Exception("not admin")
        self.user = current_user
        self.role = current_user.get("role")
        self.username = current_user.get("username")
        self.active = current_user.get("active")

    def add_user(self, username, role):
        if self.role != "admin":
            raise Exception("no permission")
        self._write_user(username=username, role=role)

    def update_user_active(self, username):
        self._change_active(username)

    def update_user_role(self, username, role):
        self._change_role(username, role)

    
    def add_gift(self, first_level, second_level, gift_name, gift_count):
        self._write_gift(first_level, second_level, gift_name, gift_count)

    def delete_gift(self, first_level, second_level, gift_name):
        self._delete_gift(first_level, second_level, gift_name)
    
    def update_gift(self, first_level, second_level, gift_name, gift_count):
        self._gift_update(first_level, second_level, gift_name, gift_count, True)

if __name__ == '__main__':
    user_path = os.path.join(os.getcwd(), "storage", "user.json")
    gift_path = os.path.join(os.getcwd(), "storage", "gift.json")
    admin = Admin("admin", user_path, gift_path)
    # print(admin.username, admin.role)
    # admin.add_user("user2", "normal")
    # admin.update_user_active("user2")
    # admin.update_user_role("user2", "admin")
    # admin.add_gift("level1", "level2", "iphone", 10)
    admin.update_gift("level1", "level1", "airpods", 200)

    