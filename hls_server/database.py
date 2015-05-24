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

            weightnorm=0.0
            
            for field_key, field_value in fields.items():
				
				field=self.get_field(field_key)				
				field_user_value = user.get_value(field_key)
				
				if not field_value or not field_user_value:
					continue
				
				weightnorm=weightnorm+field.weight
				fieldscore=0.0
				if field.ftype == 'number':
					if abs(field_user_value-field_value)<12.5:
						fieldscore=field.weight*(100.0-8*abs(field_user_value-field_value))
					else:
						fieldscore=100.0
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
                'score': user_score
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
