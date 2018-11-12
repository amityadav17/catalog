class Entity(dict):
    def __init__(self, member_list=None):
        if member_list:
            super().__init__(member_list)

    def add_member(self, member_name, member_value):
        self[member_name] = member_value

    def add_member_if_not_exist(self, member_name, member_value):
        if member_name not in self:
            self[member_name] = member_value

    def update_member_if_exist(self, member_name, member_value):
        if member_name in self:
            self[member_name] = member_value

    def remove_member(self, member_name):
        self.pop(member_name)

    def member_exist(self, member_name):
        return member_name in self

    def get_member(self, member_name):
        return self[member_name]

    def set_member(self, member_name, member_value):
        self[member_name] = member_value

    def replace_none_by_empty(self, member_name):
        if member_name in self and self[member_name] is None:
            self[member_name] = ""

    def replace_all_none_by_empty(self):
        for key, value in self.items():
            if value is None:
                self[key] = ""

    def remove_none_members(self):
        for key, value in self.items():
            if value is None:
                self.pop(key)
                self.remove_none_members()
                break

    def replace_all_empty_by_none(self):
        for key, value in self.items():
            if value == "":
                self[key] = None
