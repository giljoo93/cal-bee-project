import mysql.connector
import View
from datetime import date

def serverConn() :
    conn = mysql.connector.connect(
    host="127.0.0.1",
    user="root",
    password="1234",
    database="calbee",
    port=3306)
    return conn

def login(user) :
    conn = serverConn()
    cursor = conn.cursor(dictionary=True)
    View.clearScreen()
    user.id = input("아이디 입력 : ")
    View.clearScreen()
    user.pw = input("비밀번호 입력 : ")

    sql = "SELECT * FROM users WHERE USER_ID = %s"
    cursor.execute(sql,(user.id,))
    result = cursor.fetchone()

    if result is None :
        View.clearScreen()
        print("존재하지 않는 아이디입니다.")
        input("Press Enter!")
    elif result["USER_PW"] == user.pw :
        View.clearScreen()
        print("로그인 성공")
        print(f"{result['USER_ID']}님 환영합니다.")
        input("Press Enter!")
        
        user.grant = result['USER_GRANT']
        user.usercode = result['USER_CODE']

        user.isItSign = False
        user.isItMain = True
    else :
        View.clearScreen()
        print("비밀번호가 틀렸습니다.")
        input("Press Enter!")
    conn.close()

def signUp(user) :
    conn = serverConn()
    cursor = conn.cursor(dictionary=True)
    nowdate = date.today()
    while True :
        View.clearScreen()
        print("Cal-Bi : 회원가입 페이지입니다!")
        print("Cal-Bi : ID를 입력해주세요.")
        user.id = input("ID : ",)
        
        sql = "SELECT USER_ID FROM users WHERE USER_ID = %s"
        cursor.execute(sql,(user.id,))
        result = cursor.fetchone()

        if result is None :
            View.clearScreen()
            print("실습용 프로그램이므로 패스워드는 보안기능이 없으니 단순하게 지정해주세요.")
            print("ex) 1234, 1111, ...")
            user.pw = input("Password : ",)
            sql = "INSERT INTO users VALUES (NULL,%s,%s,%s,2)"
            cursor.execute(sql,(user.id,user.pw,nowdate))
            print("계정이 생성되었습니다.")
            conn.commit()
            input("Press Enter!")
            break

        else :
            View.clearScreen()
            print("중복되는 아이디가 존재합니다.")
            input("Press Enter!")
    conn.close()
    
def searchSchedule(user, n) : # params n, 0-일반조회 1-일정번호조회
    conn = serverConn()
    cursor = conn.cursor(dictionary=True)
    usercode = user.usercode
    View.clearScreen()
    print("기록된 일정을 조회합니다.")

    sql = "SELECT * FROM schedule WHERE USER_CODE = %s"
    cursor.execute(sql,(usercode,))
    result = cursor.fetchall()
    index = 0
    for row in result :
        index = index + 1
        print(f"{index} : {row['SCD_DATE']},{row['SCD_TITLE']},{row['DESCRIPTION'] if row['DESCRIPTION'] != '' else '세부내용없음'}")
        print(f"{index}의 일정번호 :{row['SCD_NO']}") if n == 1 else ""
              
    input("Press Enter!")
    conn.close()
    

def insertSchedule(user) :
    conn = serverConn()
    cursor = conn.cursor(dictionary=True)
    nowdate = date.today()
    usercode = user.usercode
    while True :
        print("Cal-Bee : 신규 일정을 생성합니다.")
        print("일정의 제목을 입력하세요.")
        title = input("일정명 : ")
        if title != None :
            print("일정의 날짜을 입력하세요.")
            print("숫자로 년월일을 입력해주세요.(하이픈 포함)")
            userdate = input("날짜(yyyy-mm-dd): ")
            if len(userdate) == 10 :
                    print("일정의 메모(내용)를 입력하세요.")
                    description = input("메모(내용) : ")
                    sql = "INSERT INTO schedule " \
                        "(USER_CODE, SCD_NO, SCD_TITLE, SCD_DATE, SCD_TIME, DESCRIPTION, CREATED_AT, UPDATED_AT) " \
                        "VALUES (%s,null,%s,%s,null,%s,%s,%s)"
                    cursor.execute(sql,(usercode,title,userdate,description,nowdate,nowdate))
                    conn.commit()
                    print(f"{['SCD_DATE']},,{['SCD_TITLE']},{['DESCRIPTION']}")
                    print("일정이 추가되었습니다.")
                    input("Press Enter!")
                    break
            else :
                print("날짜 수가 10자가 아닙니다.")
            
        else :
            print("제목을 입력하지 않으셨습니다.")

def deleteSchedule(user) :
    
    print("삭제를 위해서 일정리스트를 불러옵니다.")
    print("일정의 번호를 기억해주세요.")
    input("Press Enter!")
    searchSchedule(user,1) # params 1 = 일정번호조회

    conn = serverConn()
    cursor = conn.cursor(dictionary=True)
    usercode = user.usercode

    print("삭제할 데이터의 번호를 입력하세요.")
    schedule_id = int(input())

    sql = "DELETE FROM schedule WHERE SCD_NO = %s AND USER_CODE = %s"
    cursor.execute(sql, (schedule_id, usercode))

    conn.commit()
    print("일정이 삭제되었습니다.")
    input("Press Enter!")
    conn.close()