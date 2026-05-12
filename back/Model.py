import View, Control

class clients :
    def __init__(self):
        self.grant = 1          #DB grant
        self.id = ""            #DB id
        self.pw = ""            #DB pw
        self.usercode = ""      #DB PK

        self.isItStart = True   #menuCall
        self.isItSign = False   #menuCall
        self.isItMain = False   #menuCall

    def mainMenu(self) :
        View.mainMenu_clients(self)
        Control.mainMenu_choice_clients(self)

class admin(clients) :
    def __init__(self):
        super().__init__()
        self.grant = 3          #DB grant

    def mainMenu(self) :
        View.mainMenu_admin(self)
        Control.mainMenu_choice_admin(self)

def logout(user) :
    user.__class__= clients
    user.grant = 1
    user.id = ""
    user.pw = ""
    user.usercode = ""

    user.isItStart = False
    user.isItSign = True
    user.isItMain = False
    View.clearScreen()
    print("로그아웃 되었습니다.")
    input("press Enter!")

def grant3_transe_admin(user) :

    if isinstance(user, admin):
        View.clearScreen()
        print("이미 관리자 객체입니다.")
        input("Press Enter!")
    else :
        if user.grant == 3:
            user.__class__ = admin
            View.clearScreen()
            print("관리자 객체로 변경되었습니다.")
            input("Press Enter!")

