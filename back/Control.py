import Model, View, DB, AI

def start(user) :

    if user.isItStart == True :
        View.startMenu()

    user.isItStart = False
    user.isItSign = True
    

def signCall(user) :

    if user.isItSign == True :

        if user.grant == 1 :
            View.guestInfo() #Guest mode Info, impossible to save data
        
        View.signMenu()
        userInput = input("Select Menu : ")
        if userInput == "1" :
            DB.login(user)
            Model.grant3_transe_admin(user)
        elif userInput == "2" :
            DB.signUp(user)
        elif userInput == "3" :
            View.clearScreen()
            print("Guest 모드로 실행합니다.")
            input("Press Enter!")
            user.isItSign = False
            user.isItMain = True        
        else :
            print("올바른 메뉴를 선택해주세요.")
            
def menuCall(user) :

    if user.isItMain == True :
        user.mainMenu()

        
def mainMenu_choice_clients(user) :

    userInput = input("Select Menu : ")
    if userInput == "1" :
        DB.searchSchedule(user, 0)
    elif userInput == "2" :
        DB.insertSchedule(user)
    elif userInput == "3" :
        DB.deleteSchedule(user)
    elif userInput == "4":
        print("cal-bee 호출하기")
        
        # 1. 사용자에게 질문을 입력받아 변수에 저장합니다.
        question = input("질문 : ")
        
        # 2. AI.py의 스트리밍 함수를 호출하여 데이터 통로(stream)를 받아옵니다.
        stream = AI.get_calbee_stream(question)
        
        # 3. 받아온 통로를 View.py로 넘겨서 화면에 타자 치듯 출력하게 합니다.
        View.print_ai_response(stream)
        input("Press Enter!",)
    elif userInput == "0" :
        Model.logout(user)
    else :
        print("올바른 메뉴를 선택해주세요.")

def mainMenu_choice_admin(user) :

    userInput = input("Select Menu : ")
    if userInput == "1" :
        print("유저 관리하기")
    elif userInput == "2" :
        print("일정 관리하기")
    elif userInput == "3" :
        print("정산 관리하기")
    elif userInput == "0" :
        Model.logout(user)
    else :
        print("올바른 메뉴를 선택해주세요.")

