import requests
import config


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
    response = response
    print(response)
    response = response['translated_text']
    print(response)
    response = sum(response, [])
    print(response)
    print("".join(response))


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

# Note: original query string below. It seems impossible to parse and
# reproduce query strings 100% accurately so the one below is given
# in case the reproduced version is not "correct".
#response = requests.get('https://dapi.kakao.com/v3/translation/language/detect?query=Kakao Enterprise provides the AI platform essentials to enterprises by evolving Kakao’s AI technology and service expertise into innovative, ready-to-deploy business services.', headers=headers)
# Note: original query string below. It seems impossible to parse and
# reproduce query strings 100% accurately so the one below is given
# in case the reproduced version is not "correct".
#response = requests.get('https://dapi.kakao.com/v2/translation/translate?src_lang=kr&target_lang=en&query=%EC%95%88%EB%85%95%ED%95%98%EC%84%B8%EC%9A%94', headers=headers)
