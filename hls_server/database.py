from csv import DictReader as csv_reader

from hls_server.user import User
from pyxdameraulevenshtein import damerau_levenshtein_distance, normalized_damerau_levenshtein_distance, damerau_levenshtein_distance_withNPArray, normalized_damerau_levenshtein_distance_withNPArray

_database = None


def init_database(filepath):
    global _database
    _database = HlsDatabase(filepath)


def get_database():
    return _database


class HlsDatabase:

    _users = {}

    def __init__(self, filepath):
        with open(filepath) as csvfile:
             database = csv_reader(csvfile, delimiter=',')
             for row in database:
                new_user = User()
                for key, value in row.items():
                    new_user.set_value(key, value)
                self.add_user(new_user)

    def add_user(self, user):
        user_id = str(len(self._users.keys()))
        user.set_value('user_id', user_id)
        self._users[user_id] = user
        return user

    def pop_user(self, user_id):
        return self._users.pop(user_id)

    def get_user(self, user_id):
        return self._users[user_id]

    def get_field(self, name):
        for field_name, field in User.get_fields():
            if field_name == name:
                return field
        return None

    def get_fields_names(self):
        for field_name, field in User.get_fields():
            yield field_name

    def search_users(self, fields):
        result = []
        for user_id, user in self._users.items():
            user_score=0.0
            result.append({
                'user': user,
                'score': user_score
                })
        return result

    def get_missing_fields(self, fields, users):
        request_fields = set(fields)
        db_fields = set(self.get_fields_names())
        result_fields = []
        for field_name in db_fields - request_fields:
            values = [getattr(user['user'], field_name, None) for user in users]
            if all(values):
                field = self.get_field(field_name)
                result_fields.append({
                    'name': field_name,
                    'field': field})
        return result_fields
