import json

class QuizGame():
    def __init__(self, quiz_list):
        print(quiz_list)
        self.questions = [quiz["question"] for quiz in quiz_list]
        self.answers = [quiz["choices"] for quiz in quiz_list]
        self.answer = [quiz["answer"] for quiz in quiz_list]
        self.score = 0

    def run(self):
        for i in range(len(self.questions)):
            print(f"문제 {i+1}: {self.questions[i]}")
            while True:
                self.choice = input("정답을 입력하세요: ")
                if self.choice in self.answers[i]:
                    break
                print("선택지에 없는 답입니다. 다시 입력하세요.")

            if self.choice.isdigit() and int(self.choice) == self.answer[i]:
                print("정답입니다!")
                self.score += 1
            else:
                print(f"오답입니다! 정답은 {self.answer[i]}입니다.")

        return None

class Quiz():
    def __init__(self):
        self.menu_list = ["1. 퀴즈 풀기","2. 퀴즈 추가", "3. 퀴즈 목록", "4. 점수 확인", "5. 퀴즈 종료"]
        self.select = [self.start_quiz, self.add_quiz, self.list_quiz, self.check_score, self.exit_quiz]
        self.high_score = 0
        self.quiz_list = None

    def load_quiz(self):
        try:
            with open("state.json", "r", encoding="utf-8") as file:
                data = json.load(file) 
                self.high_score = data.get("high_score", 0)
                self.quiz_list = data.get("quizzes", [])
                print(self.high_score, self.quiz_list)

        except FileNotFoundError:
            print("퀴즈 목록 파일이 없습니다. 새로 생성합니다.")
            

    def print_menu(self):
        print("====== 퀴즈 메뉴 ======")
        for menu in self.menu_list:
            print(menu)
        print("======================")

    def check_inp(self):
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

    def select_menu(self):
        inp = self.check_inp()
        self.select[inp]()

    def start_quiz(self):
        print("퀴즈를 시작합니다.")
        QuizGame(self.quiz_list).run()

    def add_quiz(self):
        print("퀴즈를 추가합니다.")

    def list_quiz(self):
        print("퀴즈 목록을 확인합니다.")

    def check_score(self):
        print("점수를 확인합니다.")

    def exit_quiz(self):
        print("퀴즈를 종료합니다.")
        exit()

    def run(self):
        try:
            self.load_quiz()
            while True:
                self.print_menu()
                self.select_menu()
        except (KeyboardInterrupt, EOFError):
            print("\n입력이 중단되어 프로그램을 종료합니다.")

Quiz().run()