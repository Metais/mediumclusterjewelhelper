import requests


class Session:
    def __init__(self):
        self.session = self.login()
        self.baseURI = "https://www.pathofexile.com/api/trade/search/Settlers"
        self.itemFetchURI = "https://www.pathofexile.com/api/trade/fetch/"

    @staticmethod
    def login():
        """
        Log in to the PoE website
        :rtype: Returns a logged in session object
        """
        session = requests.Session()

        # headers
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Content-Type': 'application/json'
        }

        # login
        cookie_name, cookie_value = 'POESESSID', '9447c476ea9df62f8cfb67ce31e4011f'
        session.cookies.set(cookie_name, cookie_value)
        session.headers.update(headers)

        return session
