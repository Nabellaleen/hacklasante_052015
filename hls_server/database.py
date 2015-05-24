from csv import DictReader as csv_reader
from csv import DictWriter as csv_writer

from hls_server.user import User, get_fields
from pyxdameraulevenshtein import damerau_levenshtein_distance, normalized_damerau_levenshtein_distance, damerau_levenshtein_distance_withNPArray, normalized_damerau_levenshtein_distance_withNPArray

_database = None


def init_database(filepath):
    global _database
    _database = HlsDatabase(filepath)


def get_database():
    return _database


class HlsDatabase:

    restore_db_path = 'data/origin_db.csv'

    _users = {}
    filepath = None
    fetched = False

    def __init__(self, filepath):
        self.filepath = filepath
        self.fetch()
        self.fetched = True

    def restore(self):
        self.fetch(filepath=restore_db_path)
        self.commit()

    def fetch(self, filepath=None):
        if not filepath:
            filepath = self.filepath
        with open(filepath, 'r') as csvfile:
             database = csv_reader(csvfile, delimiter=',')
             for row in database:
                new_user = User()
                for key, value in row.items():
                    new_user.set_value(key, value)
                self.add_user(new_user)

    def commit(self):
        if not self.fetched:
            return
        with open(self.filepath, 'w') as csvfile:
            fieldnames = [key for key, value in get_fields()]
            writer = csv_writer(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for user in self._users.values():
                writer.writerow(user.get_namespace())

    def add_user(self, user):
        user_id = str(len(self._users.keys()))
        user.set_value('user_id', user_id)
        self._users[user_id] = user

        self.commit()
        return user

    def pop_user(self, user_id):
        user = self._users.pop(user_id)
        self.commit()
        return user

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

            weightnorm=0.0

            for field_key, field_value in fields.items():

                field=self.get_field(field_key)
                field_user_value = user.get_value(field_key)

                if not field_value or not field_user_value:
                    continue

                weightnorm=weightnorm+field.weight
                fieldscore=0.0
                if field.ftype == 'number':
                    if abs(int(field_user_value)-int(field_value))<10:
                        fieldscore=(100.0-8*abs(int(field_user_value)-int(field_value)))
                        print(fieldscore,field_user_value,field_value)
                    else:
                        fieldscore=0.0
                    user_score=user_score+fieldscore

                if field.ftype == 'qcm':
                    if field_user_value==field_value:
                        fieldscore=field.weight*100.0
                    else:
                        fieldscore=0.0
                    user_score=user_score+fieldscore

                if field.ftype == 'char':
                    distance=damerau_levenshtein_distance(field_user_value, field_value)
                    string_len=max(len(field_user_value),len(field_value))
                    fieldscore=100.0-(100.0*field.weight*distance/string_len)
                    user_score=user_score+fieldscore

            result.append({
                'user': user,
                'score': user_score,
                'quality': 1.0
                })

        for item in result:
            if abs(weightnorm)>0.01:
                item['score']=item['score']/weightnorm
            else:
                item['score']=0.0

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
