from flask_login import UserMixin


class User(UserMixin):
    def __init__(self, username, access_token, refresh_token):
        """
        Initializes user with username
        and tokens.
        """
        self._username = username
        self._access_token = access_token
        self._refresh_token = refresh_token


    def get_id(self):
        return self._username


    def is_authenticated(self):
        return True


    def get_access_token(self):
        return self._access_token


    def get_refresh_token(self):
        return self._refresh_token
