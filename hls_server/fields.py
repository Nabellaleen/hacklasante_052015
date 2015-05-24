class Field:

    title = None
    basic_field = False
    weight = None
    ftype = None

    def __init__(self, **kwargs):
    # Automatically add init parameters as instance fields
        for k, v in kwargs.items():
            setattr(self, k, v)

    def is_basic_field(self):
        return self.basic_field

    def get_weight(self):
        return self.weight

    def get_ftype(self):
        return self.ftype


class BasicField(Field):

    basic_field = True
