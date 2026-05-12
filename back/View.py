def clearScreen() :
    for i in range(50) :
        print()

def startMenu() :
    
    clearScreen()
    print("나만의 비서 Cal - Bi 서버와의 접속 준비를 마쳤습니다.")
    input("Press Enter!")

def guestInfo() :
    
    clearScreen()
    print("현재 [게스트] 로 연결되었습니다.")
    print("데이터의 저장을 위해서 로그인을 권장드립니다.")
    input("Press Enter!")

def signMenu() :

    clearScreen()
    print("Cal-Bi : 저와 함께 체계적으로 계획을 세워봐요!")
    print()
    print("Select Menu number(0~9)")
    print("1. 로그인")
    print("2. 회원가입")
    print("3. 게스트 상태 유지")
    print()
    
def mainMenu_clients(user) :

    clearScreen()

    print("Cal-Bi : 오늘도 행복한 순간들로 채워가봐요!")
    print()
    print("Select Menu number(0~9)")
    print("1. 일정 조회하기")
    print("2. 일정 등록하기")
    print("3. 일정 삭제하기")
    print("4. cal-bee호출하기")
    print("0. 로그아웃 하기")
    print()

def mainMenu_admin(user) :

    clearScreen()

    print("Cal-Bi : 오늘도 행복한 순간들로 채워가봐요!")
    print("admin 모드입니다.")
    print()
    print("Select Menu number(0~9)")
    print("1. 유저 관리하기")
    print("2. 일정 관리하기")
    print("3. 정산 관리하기")
    print("0. 로그아웃 하기")
    print()

def print_ai_response(stream):
    print("\n🐝 Cal-Bee : ", end="")
    
    for chunk in stream:
        print(chunk['message']['content'], end="", flush=True)
    
    print("\n")