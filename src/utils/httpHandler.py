import libs.urequests as urequests


class HttpHandler:
    def __init__(self, base_url, token_auth, endpoint):
        self.BASE_URL = base_url
        self.endpoint = endpoint
        self.token_auth = token_auth
        self.basicAuthorization = {'Authorization': 'Basic '+self.token_auth}
        self.BASE_ERROR = "Error at HttpHandler"

    def get(self, endpoint):
        try:
            return urequests.get(self.BASE_URL + endpoint)

        except Exception as err:
            error_message = "\nUrl: " + self.BASE_URL + "\n" + self.BASE_ERROR + ".get: \n"
            raise type(err)(error_message + err.args[0])

    def post(self, data=None):
        try:
            return urequests.post(self.BASE_URL + self.endpoint, data=data,
                                  headers=self.basicAuthorization)

        except Exception as err:
            error_message = "\nUrl: " + self.BASE_URL + "\n" + self.BASE_ERROR + ".post: \n"
            error_message += "data to send: " + data + "\n"
            raise type(err)(error_message + err.args[0])
