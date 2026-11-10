import json
from quiz import Quiz
from quiz_recovery import DEFAULT_QUIZZES
from input_utils import check_yes, input_text, input_number

class QuizGame():
    def __init__(self): # QuizGame 초기화
        self.menu_list = ["1. 퀴즈 풀기", "2. 퀴즈 추가", "3. 퀴즈 목록", "4. 점수 확인", "5. 퀴즈 종료"]
        self.select = [self.start_quiz, self.add_quiz, self.list_quiz, self.check_score, self.exit_quiz]
        self.high_score = 0
        self.quiz_list = None

    def recover_data(self):
        self.high_score = 0
        self.quiz_list = [Quiz(item["question"], item["choices"], item["answer"], item["source"]) for item in DEFAULT_QUIZZES]
                    
    def load_json(self): # 데이터 로드 함수
        try:
            with open("state.json", "r", encoding="utf-8") as file:
                data = json.load(file)  
                if not isinstance(data, dict):
                    raise ValueError("최상위 데이터는 딕셔너리여야 합니다.")

                if "quizzes" not in data:
                    raise ValueError("quizzes 항목이 없습니다.")

                if not isinstance(data["quizzes"], list):
                    raise ValueError("quizzes는 리스트여야 합니다.")

                self.high_score = data.get("high_score", 0)
                self.quiz_list = [Quiz(item["question"], item["choices"], item["answer"], item["source"]) for item in data["quizzes"]]

        except FileNotFoundError:
            print("데이터 파일이 없습니다. 기본 데이터를 불러옵니다.")
            
            self.recover_data()
            result = self.save_notice(success_notice=False)

            if result is True:
                print("state.json을 새로 저장했습니다!")
            else:
                print("기본 퀴즈로 게임을 진행합니다. 저장에 실패하면 변경 내용이 재실행 후 유지되지 않을 수 있습니다!")

        except (json.JSONDecodeError, UnicodeDecodeError) as error:
            print(f"데이터 파일을 해석할 수 없습니다! : {error}")
            self.recover_data()

        except OSError as error:
            print(f"데이터 파일을 읽을 수 없습니다! : {error}")
            self.recover_data()

        except ValueError as error:
            print(f"데이터 구조가 올바르지 않습니다! : {error}")
            self.recover_data()

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
        
    def save_notice(self, success_notice=True):
        result = self.save_json()
        if result is not True:
            print("데이터 저장에 실패했습니다! 아래 오류를 해결 후 재시도 바랍니다!")
            print(f"오류 : \n{result}")
            return False

        elif success_notice:
            print("데이터 저장에 성공했습니다!")

        return True
        
    def check_highscore(self, score):
        if score > self.high_score:
            self.high_score = score
            return True
        return False

    def print_menu(self):
        print("========= 퀴즈 메뉴 ==========")
        for menu in self.menu_list:
            print(menu)
        print("=" * 30)

    def print_quiz_list(self):
        print("========= 퀴즈 목록 ==========")

        if not self.quiz_list:
            print("등록된 퀴즈가 없습니다.")
            return

        for source, title in [("default", "========= 기본 퀴즈 =========="), ("user", "====== 사용자 추가 퀴즈 ======")]:
            quizzes = [quiz for quiz in (self.quiz_list) if quiz.source == source]

            if not quizzes:
                continue

            print(title)

            for idx, quiz in enumerate(quizzes, start=1):
                print(f"{idx}번 : {quiz.question}")

        print("=" * 30)

    def print_added_quiz(self):
        print("========= 추가한 퀴즈 ==========")
        if not self.quiz_list:
            print("등록된 퀴즈가 없습니다.")
            return

        source, title = ("user", "====== 사용자 추가 퀴즈 ======")
        quizzes = [quiz for quiz in (self.quiz_list) if quiz.source == source]

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

    def check_inp(self, inp_type="Menu"): # 사용자 입력값 검증 및 리턴, inp_type 인자에 의해 메뉴 선택, 보기 선택으로 나뉨
        if inp_type == "AddQuiz":
            return input_text("퀴즈")

        elif inp_type == "Choice_list":
            return input_text("보기")

        elif inp_type == "Menu":
            return input_number("메뉴 선택", 1, 5) - 1

        elif inp_type == "Choices":
            return input_number("보기 선택", 1, 4)
        
        elif inp_type == "Answer":
            return input_number("정답", 1, 4, confirm=True)

        else:
            raise ValueError(f"지원하지 않는 입력 종류입니다: {inp_type}")
                


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

        self.save_notice()


    def add_quiz(self): # 퀴즈 추가 함수
        choices = []
        answer = None
        source = "user"

        print("퀴즈를 추가합니다.")
        if (question := self.check_inp("AddQuiz")) is None:
            print("퀴즈 추가를 취소합니다.")
            return
        
        for i in range(4):
            print(f"{i+1}번째 보기")
            if (choice := self.check_inp('Choice_list')) is None:
                print("퀴즈 추가를 취소합니다.")
                return
            
            choices.append(f"{i+1}번 : {choice}")

        if (answer := self.check_inp("Answer")) is None:
            print("퀴즈 추가를 취소합니다.")
            return
       
        self.quiz_list.append(Quiz(question, choices, answer, source))  
        self.print_added_quiz()
        
        if self.save_notice(success_notice=False):
            print("퀴즈가 성공적으로 추가되었습니다!")

    def list_quiz(self): 
        self.print_quiz_list()

    def check_score(self): # 최고 점수 출력 함수
        print("점수를 확인합니다.")
        print(f"당신의 최고 점수는 {self.high_score}점 입니다!")

    def exit_quiz(self): # 종료 함수
        result = self.save_notice()
        if result is not True:
        
            while True:
                print("그래도 종료하시겠습니까? : (y : 종료 / n : 취소)")
                res = check_yes(allow_cancel=False)
                if res == 'y':
                    print("프로그램을 종료합니다.")
                    break
                elif res == 'n':
                    print("프로그램 종료를 취소합니다.")
                    return 
                
                else:
                    continue

        else:
            print("프로그램을 종료합니다.")
        exit()

    def run(self):
        
        self.load_json()
        while True:
            try:
                self.print_menu()
                self.select_menu()
            except (KeyboardInterrupt, EOFError):
                #print("\n입력이 중단되어 프로그램을 종료합니다.")
                self.exit_quiz()