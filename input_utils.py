def check_yes(allow_cancel=True):
        allowed = ('y', 'n', 'c') if allow_cancel else ('y', 'n')
        
        while True:
            res = input().strip().lower()

            if res in allowed:
                return res
            
            print("잘못된 입력입니다. 다시 시도하십시오.")

def input_text(label):
        while True:
            inp = input(f"{label} 입력 : ")

            if inp.strip() == "":
                print("빈 입력은 허용되지 않습니다!")
                continue

            print(f"입력한 {label} : {inp}")
            print("추가 하시겠습니까? (y : 예, n : 다시 입력, c : 취소) : ", end="")

            res = check_yes()

            if res == 'y':
                return inp
            elif res == 'n':
                continue
            elif res == 'c':
                return None

def input_number(label, minimum, maximum, confirm=False):
    while True:

        inp = input(f"{label} 입력 : ")

        if inp.strip() == "":
            print("빈 입력은 허용되지 않습니다!")
            continue
        
        try:
            inp = int(inp.strip())
        
        except ValueError:
            print(f"{label}은 숫자로 해야 합니다!")
            continue

        if not minimum <= inp <= maximum:
            print(f"{label}은 {minimum} ~ {maximum} 사이의 숫자여야 합니다!")
            continue

        if confirm:
            print(f"입력한 {label} : {inp}")
                            
            print("추가하시겠습니까? (y : 추가 / n : 다시입력 / c : 취소) : ", end='')
            res = check_yes()
            
            if res == 'n':
                continue
            elif res == 'c':
                return None

        return inp