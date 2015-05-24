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
        user1 = User(
            name='Toto',
            firstname='Flo',
            lastname='Rian',
            birthyear=1912,
            sexe='M')
        user2 = User(
            name=None,
            firstname='Gerard',
            lastname='Blabla',
            birthyear=1948,
            sexe='F')
        user3 = User(
            name='Superman',
            firstname='Gaston',
            lastname=None,
            birthyear=1974,
            sexe='F')
        self.add_user(user1)
        self.add_user(user2)
        self.add_user(user3)

    def add_user(self, user):
        user_id = str(len(self._users.keys()))
        user.set_value('user_id', user_id)
        self._users[user_id] = user

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
                if field_value!=None & field_value!=None:
                    weightnorm=weightnorm+field.weight
                    field=self.get_field(field_key)
                    
                    field_user_value = user.get_value(field_key)
                    
                    fieldscore=0.0
                    if field.ftype == 'number':
                        fieldscore=100.0-abs(field_user_value-field_value)
                    
                    if field.ftype == 'qcm':
                        if field_user_value==field_value:
                            fieldscore=100.0
                        else:
                            fieldscore=0.0
                    
                    if field.ftype == 'char':
                        distance=damerau_levenshtein_distance(field_user_value, field_value)
                        string_len=max(len(field_user_value),len(field_value))
                        fieldscore=100.0*distance/string_len
                    
            user_score=user_score+fieldscore
            result.append({
                'user': user,
                'score': user_score
                })
        result=result/weightnorm
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
