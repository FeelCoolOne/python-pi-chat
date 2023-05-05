import requests
import re

class Tools:
    debug_flag = False

    @staticmethod
    def debug(message, data=None):
        if Tools.debug_flag:
            print(f"[DEBUG] {message}")

    @staticmethod
    def request(url, headers=None, data=None, return_request=False):
        if headers is None:
            headers = {}

        default_headers = {
            'accept-language': 'en-US,en;q=0.9',
            'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36',
            'origin': 'https://heypi.com',
        }

        headers.update(default_headers)

        if data is not None:
            response = requests.post(url, headers=headers, data=data)
        else:
            response = requests.get(url, headers=headers)

        if return_request:
            cookies = {}
            for key, value in response.cookies.items():
                cookies[key] = value

            headers = response.headers
            body = response.text
            url = response.url

            Tools.debug(f"URL: {url}")
            Tools.debug("Cookies: " + ','.join(cookies.keys()))
            Tools.debug(f"Body: {body}")

            return body, response.request, url, cookies
        else:
            return response.text
