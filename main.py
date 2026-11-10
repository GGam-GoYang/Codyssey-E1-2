import json
from quiz_recovery import DEFAULT_QUIZZES

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
        self.inp_type = {"Menu":"메뉴 선택", "Choices":"보기 선택", "Main" : "퀴즈 메뉴", "QuizList" : "퀴즈 목록", "AddQuiz" : "추가할 퀴즈 입력", "Choice_list" : "추가할 보기 입력", "Answer" : "정답 입력"}
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
            result = self.save_json()

            if result is True:
                print("state.json을 새로 저장했습니다!")
            else:
                print("데이터 저장에 실패했습니다! 아래 오류를 해결 후 재시도 바랍니다!")
                print(f"오류 : \n{result}\n")
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

    def check_highscore(self, score):
        if score > self.high_score:
            self.high_score = score
            return True
        return False

    def print_info(self, output="Main", print_idx=0): # 목록 출력 함수, output 인자에 의해 메인 메뉴 출력, 퀴즈 목록 출력 으로 나뉨
        print(f"========= {self.inp_type[output]} ==========")

        if output == "Main":
            for menu in self.menu_list:
                print(menu)

        elif output == "QuizList":
            if not self.quiz_list:
                print("등록된 퀴즈가 없습니다.")
                return
            
            for source, title in [("default", "========= 기본 퀴즈 =========="), ("user", "====== 사용자 추가 퀴즈 ======")]:
                idx = 1
                quizzes = [quiz for quiz in (self.quiz_list) if quiz.source == source]

                if not quizzes:
                    continue

                print(title)

                for quiz in quizzes:
                    print(f"{idx}번 : {quiz.question}")
                    idx+=1
                
        elif output == "AddQuiz":
            if not self.quiz_list:
                print("등록된 퀴즈가 없습니다.")
                return

            source, title = ("user", "====== 사용자 추가 퀴즈 ======")
            idx = 1
            quizzes = [quiz for quiz in (self.quiz_list) if quiz.source == source]

            if not quizzes:
                print("등록된 퀴즈가 없습니다.")
                return

            print(title)

            if print_idx == 0:
                for quiz in quizzes:
                    print(f"{idx}번 : {quiz.question}")
                    idx+=1
            else:
                quiz = quizzes[-1]
                print(f"{len(quizzes)}번 : {quiz.question}")
                for i, choice in enumerate(quiz.choices, start=1):
                    print(choice)
                print(f"정답 : {quiz.answer}번")


        print("=" * 30)

    def check_add(self):
        
        while True:
            res = input().strip().lower()

            if res == 'y':
                return 'y'
            elif res == 'n':
                return 'n'
            elif res == 'c':
                return 'c'
            else:
                print("잘못된 입력입니다. 다시 시도하십시오.")
                continue

    def check_num(self, inp_type, inp):
        try:
            inp = int(inp.strip())
            return inp
        
        except ValueError:
            print(f"{self.inp_type[inp_type]}은 숫자로 해야 합니다!")
            return False

    def check_inp(self, inp_type="Menu"): # 사용자 입력값 검증 및 리턴, inp_type 인자에 의해 메뉴 선택, 보기 선택으로 나뉨

        while True:
            print(f"{self.inp_type[inp_type]} : ", end ='')
       
            inp = input()

            if inp.strip() == "":
                print("빈 입력은 허용되지 않습니다!")
                continue

            if inp_type == "AddQuiz":
                print(f"입력한 퀴즈 : {inp}")
                print("추가하시겠습니까? (y:추가 / n:다시입력 / c:취소) : ", end='')
                if (res := self.check_add()) == 'y':
                    return inp
                elif res == 'n':
                    continue
                elif res == 'c':
                    return None
            
            elif inp_type == "Choice_list":
                print(f"입력한 보기 :{inp}")
                print("추가하시겠습니까? (y:추가 / n:다시입력 / c:취소) : ", end='')

                if (res := self.check_add()) == 'y':
                    return inp
                elif res == 'n':
                    continue
                elif res == 'c':
                    return None
            
            elif inp_type == "Answer":
                print(f"입력한 정답 : {inp}")
                if (inp := self.check_num(inp_type, inp)) is False:
                    continue

                if not (1 <= inp <= 4):
                    print("정답은 1~4 사이의 숫자여야 합니다!")
                    continue
                
                print("추가하시겠습니까? (y:추가 / n:다시입력 / c:취소) : ", end='')

                if (res := self.check_add()) == 'y':
                    return inp
                elif res == 'n':
                    continue
                elif res == 'c':
                    return None
            
            if (inp := self.check_num(inp_type, inp)) is False:
                continue

            if inp_type == "Menu" and 1 <= inp <= 5:
                return inp - 1

            elif inp_type == "Choices" and 1 <= inp <= 4:
                return inp 

            else:
                print(f"{self.inp_type[inp_type]} 선택 범위를 확인 하십시오!")
                continue 

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
        self.print_info("AddQuiz", 1)
        result = self.save_json()
        if result is not True:
            print("데이터 저장에 실패했습니다! 아래 오류를 해결 후 재시도 바랍니다!")
            print(f"오류 : \n{result}")
        else:
            print("퀴즈가 성공적으로 추가되었습니다!")

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