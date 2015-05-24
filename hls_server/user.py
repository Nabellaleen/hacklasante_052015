 # -*- coding: utf-8 -*-


from hls_server.fields import Field, BasicField

user_fields = {
    'name': BasicField(title='Pseudonyme', weight=0.4, ftype='char'),
    'sexe': BasicField(title='Sexe', weight=0.7, ftype='qcm'),
    'firstname': BasicField(title='Prénom', weight=0.6, ftype='char'),
    'lastname': BasicField(title='Nom de famille', weight=0.3, ftype='char'),
    'birthyear': BasicField(title='Année de naissance', weight=0.9, ftype='number'),
    'nationality': BasicField(title='Nationalité', weight=0.2, ftype='qcm'),
    'legalstatus': BasicField(title='Statut légal', weight=0.2, ftype='qcm'),
    'secu': BasicField(title='Couverture médicale', weight=0.3, ftype='qcm'),

    'blood_group': Field(title='Groupe sanguin', weight=0.7),
    'user_id': BasicField(title='ID Utilisateur', weight=0),
}

def get_field(name):
    return user_fields[name]

def get_fields():
    return user_fields.items()

class User:

    def __init__(self, **kwargs):
        # Automatically add init parameters as instance fields
        for k, v in kwargs.items():
            self.set_value(k, v)

    def get_basic_namespace(self):
        # TODO : Improve being less dynamic / more explicit
        result = {}
        for field_name, field in get_fields():
            if field.is_basic_field():
                value = getattr(self, field_name, None)
                result[field_name] = value
        return result

    def get_namespace(self):
        result = {}
        for field_name, field in get_fields():
            value = getattr(self, field_name, None)
            result[field_name] = value
        return result

    @classmethod
    def get_fields(cls):
        for field_name, field in get_fields():
            yield field_name, field

    def set_value(self, name, value):
        field = get_field(name)
        if not field:
            return
        setattr(self, name, value)

    def __repr__(self):
        return "<User({0}, {1})>".format(self.user_id, self.name)
