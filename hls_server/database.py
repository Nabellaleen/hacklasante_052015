from hls_server.user import User

_database = None


def init_database(filepath):
    global _database
    _database = HlsDatabase(filepath)


def get_database():
    return _database


class HlsDatabase:

    def __init__(self, filepath):
        pass

    def get_field(self, name):
        for field_name, field in User.get_fields():
            if field_name == name:
                return field
        return None

    def get_fields_names(self):
        for field_name, field in User.get_fields():
            yield field_name

    def search_users(self, fields):
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
        # TODO
        return [{'user': user1,
                 'score': 0.7},
                {'user': user2,
                 'score': 0.4},
                {'user': user3,
                 'score': 0.2}]

    def get_missing_fields(self, fields, users):
        request_fields = set(fields)
        db_fields = set(self.get_fields_names())
        result_fields = []
        for field_name in db_fields - request_fields:
            values = [getattr(user['user'], field_name, None).get_value() for user in users]
            if all(values):
                field = self.get_field(field_name)
                result_fields.append({
                    'name': field_name,
                    'field': field})
        return result_fields
