def print_menu(menu_list):
    print("========= 퀴즈 메뉴 ==========")
    for menu in menu_list:
        print(menu)
    print("=" * 30)

def print_quiz_list(quiz_list):
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

def print_added_quiz(quiz_list):
    print("========= 추가한 퀴즈 ==========")
    if not quiz_list:
        print("등록된 퀴즈가 없습니다.")
        return

    source, title = ("user", "====== 사용자 추가 퀴즈 ======")
    quizzes = [quiz for quiz in (quiz_list) if quiz.source == source]

    if not quizzes:
        print("등록된 퀴즈가 없습니다.")
        return

    print(title)

    quiz = quizzes[-1]
    print(f"{len(quizzes)}번 : {quiz.question}")
    for choice in quiz.choices:
        print(choice)
    print(f"정답 : {quiz.answer}번")

    print("=" * 30)