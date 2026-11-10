def check_yes(allow_cancel=True):
    """허용된 확인 문자를 입력받을 때까지 재입력을 요청합니다.

    Args:
        allow_cancel (bool): 'c' 허용 여부. 기본값은 True.

    Returns:
        str: 'y', 'n' 또는 취소가 허용된 경우 'c'.
    """
    allowed = ('y', 'n', 'c') if allow_cancel else ('y', 'n')
    
    while True:
        res = input().strip().lower()

        if res in allowed:
            return res
        
        print("잘못된 입력입니다. 다시 시도하십시오.")

def input_text(label):
    """빈 문자열이 아닌 내용을 입력받고 등록 여부를 확인합니다.

    Args:
        label (str): 입력 안내에 표시할 항목 이름.

    Returns:
        str | None: 등록에 동의한 문자열 또는 취소 시 None.
    """
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
    """허용 범위의 정수를 입력받고 필요하면 등록 여부를 확인합니다.

    Args:
        label (str): 입력 안내에 표시할 항목 이름.
        minimum (int): 입력 가능한 최솟값.
        maximum (int): 입력 가능한 최댓값.
        confirm (bool): 등록 확인 여부. 기본값은 False.

    Returns:
        int | None: 범위 내 정수 또는 등록 확인에서 취소 시 None.
    """
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