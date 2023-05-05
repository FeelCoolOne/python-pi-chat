import json
import re
from requests import session, post
from sseclient import SSEClient

from heypi.tools import Tools


class Conversation:
    def __init__(self, identifiers=None):
        self.cookie = None
        self.current_started = None
        self.current_text = None
        self.ended = False

        if identifiers is not None and 'cookie' in identifiers:
            self.cookie = identifiers['cookie']
        else:
            identifiers = self.init_conversation()
            self.cookie = identifiers['cookie']

    def get_identifiers(self):
        return {
            'cookie': self.cookie
        }

    def init_conversation(self):
        headers = {
            'method': 'POST',
            'accept': 'application/json',
            'x-api-version': '2',
            'referer': 'https://heypi.com/talk',
            'content-type': 'application/json',
        }

        if self.cookie:
            headers['cookie'] = f"__Host-session={self.cookie}"

        data = json.dumps([])

        body, request, url, cookies = Tools.request("https://heypi.com/api/chat/start", headers, data, True)
        data = json.loads(body)

        if '__Host-session' in cookies:
            self.cookie = cookies['__Host-session']

        if not isinstance(data, dict) or 'latestMessage' not in data:
            raise Exception("Failed to init conversation")

        return {
            'cookie': self.cookie
        }

    def ask(self, message, callback=None):
        self.current_text = ''

        headers = {
            'method': 'POST',
            'accept': 'text/event-stream',
            'Accept-Encoding': 'gzip, deflate, br',
            'referer': 'https://heypi.com/talk',
            'content-type': 'application/json',
            'cookie': f"__Host-session={self.cookie}"
        }

        data = json.dumps({'text': message.text})
        response = post("https://heypi.com/api/chat", headers=headers, data=data, stream=True)
        client = SSEClient(response)
        for event in client.events():
            message_data = self.handle_packet(event.data)

            if not message_data or 'text' not in message_data:
                continue

            tokens = message_data['text'][len(self.current_text):]
            self.current_text = message_data['text']

            if callback:
                callback(self.current_text, tokens)

        if not self.current_text:
            self.ended = True
            self.current_text = "I'm sorry, please start a new conversation!"

            if callback:
                callback(self.current_text, self.current_text)

        return self.current_text

    def handle_packet(self, raw):
        match = re.search(r'(\{"text".+\})', raw)

        if not match:
            return False

        data = json.loads(match.group(1))

        if not data:
            return False

        return data

    def is_ended(self):
        return self.ended
