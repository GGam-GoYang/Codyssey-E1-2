import json

class Quiz():
    def __init__(self, question, choices, answer):
        self.question = question
        self.choices = choices 
        self.answer = answer

    def display(self, idx):
        print("======   문제    ======")
        print(f"문제 {idx} : {self.question}", end="\n\n")
    
        print("====== 보기 목록 ======")
        for choice in self.choices:
            print(choice)
        print("=======================")


    def check_answer(self, user_inp):
        return user_inp == self.answer


class QuizGame():
    def __init__(self):
        self.menu_list = ["1. 퀴즈 풀기", "2. 퀴즈 추가", "3. 퀴즈 목록", "4. 점수 확인", "5. 퀴즈 종료"]
        self.inp_type = {"Menu":"메뉴", "Choices":"보기", "Main" : "퀴즈 메뉴", "QuizList" : "퀴즈 목록"}
        self.select = [self.start_quiz, self.add_quiz, self.list_quiz, self.check_score, self.exit_quiz]
        self.high_score = 0
        self.score = 0
        self.quiz_list = None

    def load_quiz(self):
        try:
            with open("state.json", "r", encoding="utf-8") as file:
                data = json.load(file) 
                self.high_score = data.get("high_score", 0)
                self.quiz_list = [Quiz(item["question"], item["choices"], item["answer"]) for item in data["quizzes"]]

        except FileNotFoundError:
            print("퀴즈 목록 파일이 없습니다. 새로 생성합니다.")
            

    def print_info(self, output="Main", choices=None):
        print(f"====== {self.inp_type[output]} ======")
        if output == "Main":
            for menu in self.menu_list:
                print(menu)
        elif output == "QuizList":
            for choice in choices:
                print(choice)
        print("=======================")

    def check_inp(self, inp_type="Menu"):
        while True:
            print(f"{self.inp_type[inp_type]} 선택 : ", end ='')
       
            inp = input().strip()
            try:
                inp = int(inp)
            except ValueError:
                print(f"{self.inp_type[inp_type]} 선택은 숫자로 해야 합니다!")
                continue
            
            if inp_type == "Menu" and 1 <= inp <= 5:
                return inp - 1

            elif inp_type == "Choices" and 1 <= inp <= 4:
                return inp 
            
            else:
                print(f"{self.inp_type[inp_type]} 선택 범위를 확인 하십시오!")

    def select_menu(self):
        inp = self.check_inp()
        self.select[inp]()

    def start_quiz(self):
        self.score = 0
        print("퀴즈를 시작합니다.")

        for i, quiz in enumerate(self.quiz_list, start=1):
            quiz.display(i)

            user_input = self.check_inp("Choices")

            if quiz.check_answer(user_input):
                print("정답입니다!")
                self.score += 1
    
            else:
                print(f"오답입니다! 정답은 {quiz.answer}번입니다.")
                
        print(f"최종 점수 : {self.score}")
        

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
                self.print_info()
                self.select_menu()
        except (KeyboardInterrupt, EOFError):
            print("\n입력이 중단되어 프로그램을 종료합니다.")

QuizGame().run()