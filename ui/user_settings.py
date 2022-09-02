class UserSettings:
    """User settings class
    This holds settings that the user can change.
    FIXME For now, the values are hard coded.
    Use a config file of some sort to persist the data.
    """

    def __init__(self) -> None:
        self._database_path = "../share-data/"
        self._import_path = "../share-data/"

    def get_database_path(self):
        return self._database_path

    def get_import_path(self):
        return self._import_path
