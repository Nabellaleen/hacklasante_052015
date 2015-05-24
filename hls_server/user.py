class User:

    def __init__(self, **kwargs):
        # Automatically add init parameters as instance fields
        for k, v in kwargs.items():
            setattr(self, k, v)

    def get_namespace(self):
        # TODO : Improve being less dynamic / more explicit
        return vars(self)
