"""
크래딧
프로그래밍 :배성훈
총괄 프로그래밍 :배성훈
아이콘 제작 :배성훈
팀장 :배성훈

프로잭트 이름
tpkta(트프크터)(Translate Program used by Kakao Translate Api)

📢소게 
이 트프크터 는 단어를 인지하여 거기에따라 변역하는 똑똑한 프로그램입니다.
사용자는 이 프로그램 을 이용하여 다양한 언어를 변역할수있습니다.
이 프로그램은 저의 걸작이자 또한 저의 피 와 땀이 섞은 프로그램입니다.

제작자의 한마디
많이많이 사용해주세요 :배성훈
최근 작성 날짜 2022-03-11

🔨현재진행도 🔨
✔ 0.1 현재상태 기본적인 언어 구별 가는 하고 영어애서 한글로 변역하는 쳬게완료(2022-03-11 배성훈)
✔ 0.2 언어를 구별하고 거기에따라 변역을 할수있다(2022-03-12 배성훈)
✔ 0.3 출구어(결과물) 의 언어를 설정란을 통해 할수있다1
✔ 0.4 예외 처리 기능 추가
❌0.5 1차 최적화
❌0.6 2차 최적화 
❌0.7 메뉴구성 최적화
❌0.8 최종 태스트
❌0.9 publish

issue:
 1. (conplete)Selecting the same language in the first choice will be "keyError"
 Solution -> Insert the same language discrimination if statement🎉


              🔨제작자의 이메일 주소
__________________________________________________
|            chrisbae0204@gmail.com              |
--------------------------------------------------
도움을 주신 여러분 감사합니다!!
"""
# import part
import os
import sys
import ocr
import translate
import requests
choice_lang = ["kr", 'en', 'jp', 'cn', 'vi', 'id', 'ar', 'bn',
               'de', 'es', 'fr', 'hi', 'it', 'ms', 'pt', 'ru', 'th', 'tr']
B_lang = "kr"
# funtion part


def settingwriter(lang):
    """
    이 함수는 언어를 입력하여 setting.txt 에 쓰고 저장합니다

    """
    with open("setting.txt", 'w+') as file:
        file.write("lang:"+str(lang))


def settingchange():
    """
    이함수는 setting.txt 에서 설정을 읽어온 다음엔 B_lang(결과 언어)를 설정값으로 바꿉니다.
    """
    global B_lang
    if(os.path.isfile("setting.txt")):
        with open('setting.txt', 'r')as file:
            a = file.readline()
            a = a.split(":")[1]
            B_lang = a
            return a
    else:
        return


def translaterFromApi(src_lang: str, target_lang: str, query: str) -> str:
    """
    이 함수는 kakao Translate api을 사용하여 query(입력값)과 src_lang(입력값의 언어)를 
    target_lang(결과 언어)로 변역합니다
        이 api는 총 18개의 언어를 지원합니다 자세한사항은 https://developers.kakao.com/docs/latest/ko/translate/common#language 을 보세요.

    """
    headers = {
        'Authorization': 'KakaoAK ddd8494e7e3ce31d9effa2e31be15646',
    }

    params = (
        ('src_lang', src_lang),
        ('target_lang', target_lang),
        ('query', query),
    )

    response = requests.get(
        'https://dapi.kakao.com/v2/translation/translate', headers=headers, params=params).json()
    response = response["translated_text"][0][0]
    return response


def detect_lang(words):
    """
    이함수는 kakao language detect api을 이영하여 word(입력값)의 언어가 무었인지 알려줍니다.
    이 api는 총 18개의 언어를 지원합니다 자세한사항은 https://developers.kakao.com/docs/latest/ko/translate/common#language 을 보세요.

    """
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


# Main part
settingchange()
a = ocr.trans("ddd8494e7e3ce31d9effa2e31be15646")

while True:
    print("-"*100)
    print(" _____                           _         _         ")
    print("|_   _|                         | |       | |        ")
    print("  | |   _ __   __ _  _ __   ___ | |  __ _ | |_   ___ ")
    print("  | |  | '__| / _` || '_ \ / __|| | / _` || __| / _ \\")
    print("  | |  | |   | (_| || | | |\__ \| || (_| || |_ |  __/")
    print("  |_|  |_|    \__,_||_| |_||___/|_| \__,_| \__| \___|")
    print("1. 일반 변역")
    print("2. 사진 변역")
    print("3. 설정")
    print("4. 나가기")
    try:
        user_input = int(input("다음중 하나를 고르세요 : "))
    except ValueError:
        print("다시 입력하세요")
        user_input = 0
    if user_input == 1:  # 1 번째 선택지
        print("-" * 100)
        print("일반변역를 선택했습니다.")
        print("변역할 문장을 입력하세요")
        user_input = input("문장을 입력하세요 : ")

        if detect_lang(user_input) != B_lang:
            print(translaterFromApi(detect_lang(user_input), B_lang, user_input))
        else:
            print("Error E01")
    elif user_input == 2:  # 2 번째 선택지
        print("-"*100)
        print("파일 경로를 입력하세요")
        print('파일 경로들⤵')
        for i, j in enumerate(os.listdir("./")):
            print('{}. {}'.format(i+1, j))
        user_input = int(input("(여기에 나와있는 파일 목록중에서 하나를 고르시오)->"))
        user_input = os.listdir("./")[user_input-1]
        a.getImageAndTranslate(
            user_input, "ddd8494e7e3ce31d9effa2e31be15646", B_lang)
    elif user_input == 3:  # 3 번째 선택지
        print("-"*100)
        print("결과 문장 언어를 선택합니다")
        print("1.한국어 2.영어 3.일본어 4.중국어")
        print("5.베트남어 6.인도네시아어 7.아랍어 8.뱅갈어")
        print("9.독일어 10.스페인어 11.프랑스어 12.힌디어")
        print("13.아탈리아어 14.말레이시아어 15.네덜란드어 16.포르투갈어")
        print("17.러시아어 18.태국어 19.터키어")
        try:
            user_input = int(input("다음중 하나를 고르세요 : "))
            print("설정이 잘 적용이 될려면 이 프로그램을 다시 시작 하세요")
            B_lang = choice_lang[user_input-1]
            settingwriter(B_lang)
        except ValueError:
            print("다시 입력하세요")
            user_input = 0

    elif user_input == 4:  # 4 번째 선택지
        sys.exit()
