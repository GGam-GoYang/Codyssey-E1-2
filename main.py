menu_list = ["1. 퀴즈풀기","2. 퀴즈 추가", "3. 퀴즈 목록", "4. 점수 확인", "5. 퀴즈 종료"]
Start = True
def print_menu():
    print("====== 퀴즈 메뉴 ======")
    for menu in menu_list:
        print(menu)
    print("======================")

def check_inp():
    while True:
        print("메뉴 선택 : ", end ='')
        inp = input().strip()
        try:
            inp = int(inp)
        except ValueError:
            print("메뉴 선택은 숫자로 해야 합니다!")
            continue

        if 1 <= inp <= 5:
            return inp - 1

        else:
            print("메뉴 범위를 확인 하십시오!")


def select_menu():
    inp = check_inp()
    if inp == 4:
        print("프로그램을 종료합니다.")
        exit()
    else:
        print(menu_list[inp])
try:
    while Start:
        print_menu()
        select_menu()
except (KeyboardInterrupt, EOFError):
    print("\n입력이 중단되어 프로그램을 종료합니다.") 
