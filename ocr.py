import json
import requests
import cv2
import config
import urllib.parse
import requests
import sys
import translate


def translaterFromApi(src_lang: str, target_lang: str, query: str) -> str:
    headers = {
        'Authorization': 'KakaoAK '+config.secrit_key,
    }

    params = (
        ('src_lang', src_lang),
        ('target_lang', target_lang),
        ('query', query),
    )

    response = requests.get(
        'https://dapi.kakao.com/v2/translation/translate', headers=headers, params=params).json()
    response = response['translated_text']
    print(response)
    response = sum(response, [])
    print(response)


def detect_lang(words):
    import requests

    headers = {
        'Authorization': 'KakaoAK ddd8494e7e3ce31d9effa2e31be15646',
    }

    params = (
        ('query', words),
    )

    response = requests.get(
        'https://dapi.kakao.com/v3/translation/language/detect', headers=headers, params=params).json()
    response = response['language_info'][0]['code']
    return response


class trans():
    def __init__(self, key):
        self.key = key

    def getImageAndTranslate(self, image, key: str, target_lang) -> str:
        # translator = Translator()
        url = 'https://dapi.kakao.com/v3/translation/language/detect'
        LIMIT_PX = 1024
        LIMIT_BYTE = 1024 * 1024  # 1MB
        LIMIT_BOX = 40

        def kakao_ocr_resize(image_path: str):
            """opencv-python
            ocr detect/recognize api helper
            ocr api의 제약사항이 넘어서는 이미지는 요청 이전에 전처리가 필요.

            pixel 제약사항 초과: resize
            용량 제약사항 초과  : 다른 포맷으로 압축, 이미지 분할 등의 처리 필요. (예제에서 제공하지 않음)

            :param image_path: 이미지파일 경로
            :return:
            """
            image = cv2.imread(image_path)
            height, width, _ = image.shape

            if LIMIT_PX < height or LIMIT_PX < width:
                ratio = float(LIMIT_PX) / max(height, width)
                image = cv2.resize(image, None, fx=ratio, fy=ratio)
                height, width, _ = height, width, _ = image.shape

                # api 사용전에 이미지가 resize된 경우, recognize시 resize된 결과를 사용해야함.
                image_path = "{}_resized.jpg".format(image_path)
                cv2.imwrite(image_path, image)

                return image_path
            return None

        def kakao_ocr(image_path: str, appkey: str) -> str:
            """
            OCR api request example
            :param image_path: 이미지파일 경로
            :param appkey: 카카오 앱 REST API 키
            """
            API_URL = 'https://dapi.kakao.com/v2/vision/text/ocr'

            headers = {'Authorization': 'KakaoAK {}'.format(appkey)}

            image = cv2.imread(image_path)
            jpeg_image = cv2.imencode(".jpg", image)[1]
            data = jpeg_image.tobytes()

            res = requests.post(API_URL, headers=headers,
                                files={"image": data})
            print(res.status_code)
            return requests.post(API_URL, headers=headers, files={"image": data})
        image_path = ''
        appkey = ''
        image_path, appkey = image, key

        resize_impath = kakao_ocr_resize(image_path)
        if resize_impath is not None:
            image_path = resize_impath
            print("원본 대신 리사이즈된 이미지를 사용합니다.")
        material_list = []

        output = kakao_ocr(image_path, appkey).json()
        print(output['result'])
        for i in range(0, len(output['result'])):
            material_list.append(output['result'][i]['recognition_words'])
        str1 = sum(material_list, [])
        str1 = " ".join(str1)
        print(str1)
        src_lang = translate.detect_lang(str1)
        print(src_lang)
        translate.translaterFromApi(src_lang, target_lang, str1)
