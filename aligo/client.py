import requests

from urllib.parse import urljoin

from .exc import (
    AllowAuthError, AllowSenderError, AligoError, NotEnoughPoint,
)
from .decorator import required


ALIGO_HOST = 'https://apis.aligo.in/'


class Aligo:

    def __init__(self, *, auth_key, user_id, is_test):
        self.auth_key = auth_key
        self.user_id = user_id
        self.is_test = 'Y' if is_test else 'N'

        request_session = requests.Session()
        request_adapter = requests.adapters.HTTPAdapter(max_retries=3)
        request_session.mount('https://', request_adapter)
        self.request_session = request_session

    def get_response(self, response):
        response.raise_for_status()
        result = response.json()
        result_code = int(result.pop('result_code'))
        result_message = result.pop('message')
        if result_code == -201:
            raise NotEnoughPoint(result_message)
        elif result_code == -101:
            raise AllowAuthError(result_message)
        elif result_code == -103:
            raise AllowSenderError(result_message)
        elif result_code < 0:
            raise AligoError(result_code, result_message)
        return result

    def _get_payload(self):
        return {
            'key': self.auth_key,
            'user_id': self.user_id
        }

    def _post(self, url, payload=None):
        response = self.request_session.post(url, data=payload)
        return self.get_response(response)

    def _send(self, **kwargs):
        payload = {
            'testmode_yn': self.is_test,
            **self._get_payload(),
            **kwargs
        }
        url = urljoin(ALIGO_HOST, 'send/')
        return self._post(url, payload)

    @required(['sender', 'receiver', 'msg'])
    def sms_send(self, **kwargs):
        return self._send(**kwargs)

    @required(['sender', 'receiver', 'msg', 'title'])
    def lms_send(self, **kwargs):
        return self._send(**kwargs)

    @required(['sender', 'receiver', 'msg', 'title', 'image'])
    def mms_send(self, **kwargs):
        return self._send(**kwargs)

    def status(self, *, msg_id):
        url = urljoin(ALIGO_HOST, 'sms_list/')
        payload = self._get_payload()
        payload.update({'mid': msg_id})
        return self._post(url, payload)

    def remain(self):
        url = urljoin(ALIGO_HOST, 'remain/')
        return self._post(url, self._get_payload())
