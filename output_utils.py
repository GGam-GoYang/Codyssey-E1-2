def print_menu(menu_list):
    """메뉴 항목을 순서대로 출력합니다.

    Args:
        menu_list (list[str]): 출력할 메뉴 문자열 목록.
    """
    print("========= 퀴즈 메뉴 ==========")
    for menu in menu_list:
        print(menu)
    print("=" * 30)

def print_quiz_list(quiz_list):
    """기본 퀴즈와 사용자 퀴즈를 구분하여 각각 1번부터 출력합니다.

    Args:
        quiz_list (list[Quiz] | None): 출력할 퀴즈 목록.
            비어 있거나 None이면 등록된 퀴즈가 없음을 안내합니다.
    """
    print("========= 퀴즈 목록 ==========")

    if not quiz_list:
        print("등록된 퀴즈가 없습니다.")
        return

    for source, title in [("default", "========= 기본 퀴즈 =========="), ("user", "====== 사용자 추가 퀴즈 ======")]:
        quizzes = [quiz for quiz in (quiz_list) if quiz.source == source]

        if not quizzes:
            continue

        print(title)

        for idx, quiz in enumerate(quizzes, start=1):
            print(f"{idx}번 : {quiz.question}")

    print("=" * 30)

def print_added_quiz(added_quiz):
    """마지막 사용자 퀴즈의 번호, 문제, 보기와 정답을 출력합니다.

    Args:
        added_quiz (Quiz): 새로 추가한 사용자 퀴즈 객체.
    """
    print("====== 사용자 추가 퀴즈 ======")
    print(f"문제 : {added_quiz.question}")

    for choice in added_quiz.choices:
        print(choice)

    print(f"정답 : {added_quiz.answer}번")

    print("=" * 30)