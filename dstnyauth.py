import requests
import json
import datetime


class DstnyAuth:
    def __init__(self, user, passwd, redirect="mysoluno"):
        self.status = False
        self.expires = datetime
        self.auth_token = ""
        self.refresh_token = ""
        self.redirect = redirect
        self.user = user
        self.passwd = passwd

        match self.redirect:
            case "mysoluno":
                self.redirect = "https://mysoluno.se"
            case "tools":
                self.redirect = "https://tools.soluno.se/oauth/callback"
            case default:
                self.redirect = "https://mysoluno.se"
        self.authenticate()
        pass

    def authenticate(self):
        url = "https://sso.soluno.se/api/v1/auth"
        headers = {
            "accept": "application/json, text/plain, */*",
            "Content-Type": "application/json;charset=UTF-8"
        }
        params = {
            "user": self.user,
            "password": self.passwd,
            "redirect_uri": str(self.redirect)
        }
        resp = requests.post(url, headers=headers, data=json.dumps(params))
        try:
            if resp.status_code != 200:
                return 0
            else:
                self.auth_token = json.loads(resp.text)['access_token']
                self.refresh_token = json.loads(resp.text)['refresh_token']
                expires = json.loads(resp.text)['expires']
                expires = datetime.datetime.fromisoformat(expires)
                self.expires = expires + datetime.timedelta(hours=1)
                # self.expires = parser.parse(expires)
                self.status = True

        except all:
            return 0

    def check_auth(self):
        expires = self.expires
        now = datetime.datetime.now()
        if now <= expires.datetime.replace(tzinfo=None):
            self.status = True
        else:
            self.status = False
