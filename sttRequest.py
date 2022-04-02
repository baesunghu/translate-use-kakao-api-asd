import requests
import json


class sttRequester():
    def __init__(self):
        pass

    def sttRequester(self, key, fileLocation):
        try:
            kakao_speech_url = "https://kakaoi-newtone-openapi.kakao.com/v1/recognize"

            rest_api_key = key

            headers = {
                "Content-Type": "application/octet-stream",
                "X-DSS-Service": "DICTATION",
                "Authorization": "KakaoAK " + rest_api_key,
            }

            with open(fileLocation, 'rb') as fp:
                audio = fp.read()

            res = requests.post(kakao_speech_url, headers=headers, data=audio)
            result_json_string = res.text[res.text.index(
                '{"type":"finalResult"'):res.text.rindex('}')+1]
            result = json.loads(result_json_string)
            return result['value']

        except ValueError:
            return "E03"
