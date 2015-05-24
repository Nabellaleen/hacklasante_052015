from hls_server.fields import Field, BasicField

class User:

    name = BasicField(title='Pseudonyme', weight=0.4, ftype='char')
    sexe = BasicField(title='Sexe', weight=0.7, ftype='qcm')
    firstname = BasicField(title='Prénom', weight=0.6, ftype='char')
    lastname = BasicField(title='Nom de famille', weight=0.3, ftype='char')
    birthyear = BasicField(title='Année de naissance', weight=0.9, ftype='number')
    nationality = BasicField(title='Nationalité', weight=0.2, ftype='qcm')
    legalstatus = BasicField(title='Statut légal', weight=0.2, ftype='qcm')
    secu = BasicField(title='Couverture médicale', weight=0.3, ftype='qcm')
    
    blood_group = Field(title='Groupe sanguin', weight=0.7)

    def __init__(self, **kwargs):
        # Automatically add init parameters as instance fields
        for k, v in kwargs.items():
            field = getattr(self, k, None)
            if not field:
                continue
            field.set_value(v)

    def get_basic_namespace(self):
        # TODO : Improve being less dynamic / more explicit
        result = {}
        for field_name, field in User.get_fields():
            if field.is_basic_field():
                result[field_name] = field.get_value()
        return result

    @classmethod
    def get_fields(cls):
        for elt_name in dir(cls):
            elt = getattr(cls, elt_name)
            if isinstance(elt, Field):
                yield elt_name, elt
