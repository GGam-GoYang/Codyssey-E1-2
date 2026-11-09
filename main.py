import json

class Quiz():
    def __init__(self, question, choices, answer, source):
        self.question = question
        self.choices = choices 
        self.answer = answer
        self.source = source

    def display(self, idx):
        print("============ 문제 ============")
        print(f"문제 {idx} : {self.question}", end="\n\n")
    
        print("========= 보기 목록 ==========")
        for choice in self.choices:
            print(choice)
        print("==============================")


    def check_answer(self, user_inp):
        return user_inp == self.answer


class QuizGame():
    def __init__(self): # QuizGame 초기화
        self.menu_list = ["1. 퀴즈 풀기", "2. 퀴즈 추가", "3. 퀴즈 목록", "4. 점수 확인", "5. 퀴즈 종료"]
        self.inp_type = {"Menu":"메뉴", "Choices":"보기", "Main" : "퀴즈 메뉴", "QuizList" : "퀴즈 목록"}
        self.select = [self.start_quiz, self.add_quiz, self.list_quiz, self.check_score, self.exit_quiz]
        self.high_score = 0
        self.quiz_list = None

    def load_json(self): # 데이터 로드 함수
        try:
            with open("state.json", "r", encoding="utf-8") as file:
                data = json.load(file) 
                self.high_score = data.get("high_score", 0)
                self.quiz_list = [Quiz(item["question"], item["choices"], item["answer"], item["source"]) for item in data["quizzes"]]

        except FileNotFoundError:
            print("퀴즈 목록 파일이 없습니다. 새로 생성합니다.")

    def convert_json(self):
        return {
            "quizzes" : [
                {"question" : quiz.question,
                 "choices" : quiz.choices,
                 "answer" : quiz.answer,
                 "source" : quiz.source}
                 for quiz in self.quiz_list
            ],
            "high_score" : self.high_score
        }

    def save_json(self):
        data = self.convert_json()
        
        try:
            with open("state.json", "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            return True
        except OSError as error:
            return error

    def check_highscore(self, score):
        if score > self.high_score:
            self.high_score = score
            return True
        return False

    def print_info(self, output="Main"): # 목록 출력 함수, output 인자에 의해 메인 메뉴 출력, 퀴즈 목록 출력 으로 나뉨
        print(f"========= {self.inp_type[output]} ==========")

        if output == "Main":
            for menu in self.menu_list:
                print(menu)

        elif output == "QuizList":
            if not self.quiz_list:
                print("등록된 퀴즈가 없습니다.")
                return
            
            for source, title in [("default", "========= 기본 퀴즈 =========="), ("user",    "====== 사용자 추가 퀴즈 ======")]:
                idx = 1
                quizzes = [quiz for quiz in (self.quiz_list) if quiz.source == source]

                if not quizzes:
                    continue

                print(title)

                for quiz in quizzes:
                    if quiz.source != source:
                        continue

                    print(f"{idx}번 : {quiz.question}")
                    idx+=1

        print("=" * 30)

    def check_inp(self, inp_type="Menu"): # 사용자 입력값 검증 및 리턴, inp_type 인자에 의해 메뉴 선택, 보기 선택으로 나뉨

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

    def select_menu(self): # 사용자 입력값 메뉴 선택으로 치환
        inp = self.check_inp()
        self.select[inp]()

    def start_quiz(self): # 퀴즈 풀기 함수
        score = 0

        if not self.quiz_list:
            print("등록된 퀴즈가 없습니다.\n등록 후 다시 진행 바랍니다.")
            return

        print("퀴즈를 시작합니다.")

        for i, quiz in enumerate(self.quiz_list, start=1):
            quiz.display(i)

            user_input = self.check_inp("Choices")

            if quiz.check_answer(user_input):
                print("정답입니다!")
                score += 1
    
            else:
                print(f"오답입니다! 정답은 {quiz.answer}번입니다.")
                
        print(f"최종 점수 : {score}")
        if self.check_highscore(score):
            print(f"축하합니다! 최고 점수 {score}점을 달성했습니다!")
        result = self.save_json()
        if result is not True:
            print("데이터 저장에 실패했습니다! 아래 오류를 해결 후 재시도 바랍니다!")
            print(f"오류 : \n{result}")


    def add_quiz(self): # 퀴즈 추가 함수
        print("퀴즈를 추가합니다.")


    def list_quiz(self): # 퀴즈 목록 출력 함수(print_info 재사용)
        self.print_info("QuizList")

    def check_score(self): # 최고 점수 출력 함수
        print("점수를 확인합니다.")
        print(f"당신의 최고 점수는 {self.high_score}점 입니다!")

    def exit_quiz(self): # 종료 함수
        print("퀴즈를 종료합니다.")
        exit()

    def run(self):
        try:
            self.load_json()
            while True:
                self.print_info()
                self.select_menu()
        except (KeyboardInterrupt, EOFError):
            print("\n입력이 중단되어 프로그램을 종료합니다.")

QuizGame().run()