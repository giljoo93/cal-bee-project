import Control, Model

## 실행 부분

user = Model.clients()      #create object
Control.start(user)         #Starting ...

while True :
    Control.signCall(user)  #signmenu call
    Control.menuCall(user)  #mainmenu call

    