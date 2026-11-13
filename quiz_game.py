import os
import json
import random
from quiz import Quiz
from quiz_recovery import DEFAULT_QUIZZES
from input_utils import check_yes, input_text, input_number
from output_utils import print_menu, print_quiz_list, print_added_quiz
from validators import validate_state
from datetime import datetime

class QuizGame():
    def __init__(self):
        """메뉴와 기능을 연결하고 게임 상태를 초기화합니다."""
        self.menu_list = ["1. 퀴즈 풀기", "2. 퀴즈 풀기(랜덤)", "3. 퀴즈 추가", "4. 퀴즈 목록", "5. 점수 확인", "6. 퀴즈 종료"]
        self.select = [self.start_quiz, lambda: self.start_quiz(shuffle=True), self.add_quiz, self.list_quiz, self.check_score, self.exit_quiz]
        self.has_played = False
        self.high_score = 0
        self.quiz_list = None
        self.save_blocked = False

    def recover_data(self):
        """최고 점수를 초기화하고 기본 퀴즈를 메모리에 복구합니다."""
        self.has_played = False
        self.high_score = 0
        self.quiz_list = [Quiz.from_dict(item) for item in DEFAULT_QUIZZES]

    def backup_data(self):
        """JSON 데이터를 백업합니다.

        Returns:
            bool: 백업 성공 시 True, 실패 시 False.
        """
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S-%f")
        backup_name = f"state-backup-{timestamp}.json"

        try:
            with open("state.json", "rb") as source:
                data = source.read()

            with open(backup_name, "xb") as backup:
                backup.write(data)

        except OSError as error:
            self.save_blocked = True
            print(f"원본 데이터 백업에 실패했습니다: {error}")
            print("원본 보호를 위해 이번 실행에서는 저장하지 않습니다.")
            return False

        print(f"원본 데이터를 백업했습니다: {backup_name}")
        print("초기 데이터로 진행됩니다. 이후 퀴즈 추가·플레이 완료·종료 시 저장에 성공하면 state.json이 현재 게임 데이터로 덮어써집니다.")
        return True

    def load_json(self):
        """저장 데이터를 불러오고, 처리 가능한 오류가 발생하면 기본 데이터로 복구합니다."""
        try:
            with open("state.json", "r", encoding="utf-8") as file:
                data = json.load(file)
                  
                validate_state(data)
                
                quizzes = [Quiz.from_dict(item) for item in data["quizzes"]] 
                self.quiz_list = quizzes
                self.has_played = data.get("has_played", False)
                self.high_score = data.get("high_score", 0)

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
            self.backup_data()
            self.recover_data()

        except OSError as error:
            print(f"데이터 파일을 읽을 수 없습니다! : {error}")
            self.backup_data()
            self.recover_data()

        except ValueError as error:
            print(f"데이터 구조가 올바르지 않습니다! : {error}")
            self.backup_data()
            self.recover_data()

    def convert_json(self):
        """현재 퀴즈와 최고 점수를 저장용 딕셔너리로 변환합니다.

        Returns:
            dict: has_played, quizzes, high_score를 포함한 딕셔너리.
        """
        return {
            "has_played" : self.has_played,
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
        """현재 게임 상태를 state.json에 저장합니다.

        Returns:
            bool | OSError: 성공하면 True, 저장 차단 또는 쓰기∙교체 실패 시 오류 객체.
        """
        if self.save_blocked:
            return OSError("원본 백업 실패로 이번 실행의 저장이 차단되었습니다.")
        
        data = self.convert_json()
        
        try:
            with open("state.json.tmp", "w", encoding="utf-8") as file:
                json.dump(data, file, ensure_ascii=False, indent=4)
            os.replace("state.json.tmp", "state.json")
            return True
        
        except OSError as error:
            return error
        
    def save_notice(self, success_notice=True):
        """게임 상태를 저장하고 성공 또는 실패를 안내합니다.

        Args:
            success_notice (bool): 성공 안내 출력 여부. 기본값은 True.

        Returns:
            bool: 저장에 성공하면 True, 실패하면 False.
        """
        result = self.save_json()
        if result is not True:
            print("데이터 저장에 실패했습니다! 아래 오류를 해결 후 재시도 바랍니다!")
            print(f"오류 : \n{result}")
            return False

        elif success_notice:
            print("데이터 저장에 성공했습니다!")

        return True
        
    def check_highscore(self, score):
        """현재 점수가 최고 점수보다 높으면 최고 점수를 갱신합니다.

        Args:
            score (int): 이번 게임에서 맞힌 문제 수.

        Returns:
            bool: 최고 점수를 갱신했으면 True, 아니면 False.
        """
        if score > self.high_score:
            self.high_score = score
            return True
        return False

    def select_menu(self):
        """메뉴를 선택받아 연결된 기능을 실행합니다."""
        inp = input_number("메뉴 선택", 1, len(self.menu_list)) - 1
        self.select[inp]()

    def start_quiz(self, shuffle=False):
        """퀴즈를 진행하고 완료 시 최고 점수를 갱신하여 저장을 시도합니다."""
        score = 0

        if not self.quiz_list:
            print("등록된 퀴즈가 없습니다.\n등록 후 다시 진행 바랍니다.")
            return

        print("퀴즈를 시작합니다.")
        play_quizzes = random.sample(self.quiz_list, len(self.quiz_list)) if shuffle else self.quiz_list
        
        for i, quiz in enumerate(play_quizzes, start=1):
            quiz.display(i)

            user_input = input_number("보기 선택", 1, 4)

            if quiz.check_answer(user_input):
                print("정답입니다!")
                score += 1
            else:
                print(f"오답입니다! 정답은 {quiz.answer}번입니다.")
                
        print(f"최종 점수 : {score}점")
        if self.check_highscore(score):
            print(f"축하합니다! 최고 점수 {score}점을 달성했습니다!")

        self.has_played = True
        self.save_notice(success_notice=False)

    def add_quiz(self):
        """사용자 퀴즈를 입력받아 메모리에 추가하고 저장을 시도합니다.

        Returns:
            None: 등록 처리를 마치거나 등록을 취소한 경우.
        """
        choices = []
        source = "user"

        print("퀴즈를 추가합니다.")
        if (question := input_text("퀴즈")) is None:
            print("퀴즈 추가를 취소합니다.")
            return
        
        for i in range(4):
            print(f"{i+1}번째 보기")
            if (choice := input_text("보기")) is None:
                print("퀴즈 추가를 취소합니다.")
                return
            
            choices.append(f"{i+1}번 : {choice}")

        if (answer := input_number("정답", 1, 4, confirm=True)) is None:
            print("퀴즈 추가를 취소합니다.")
            return
        added_quiz = Quiz(question, choices, answer, source)

        self.quiz_list.append(added_quiz)  
        print_added_quiz(added_quiz)
        
        if self.save_notice(success_notice=False):
            print("퀴즈가 성공적으로 추가되었습니다!")

    def list_quiz(self):
        """기본 퀴즈와 사용자 퀴즈의 목록을 출력합니다."""
        print_quiz_list(self.quiz_list)

    def check_score(self):
        """현재 최고 점수를 출력합니다.
        
        Returns:
            None: 플레이 기록이 없는 경우.
        """
        if not self.has_played:
            print("아직 퀴즈를 완료한 기록이 없습니다.")
            return
        
        print("점수를 확인합니다.")
        print(f"당신의 최고 점수는 {self.high_score}점 입니다!")

    def exit_quiz(self):
        """저장을 시도한 뒤 종료하며, 저장 실패 시 종료 여부를 확인합니다.

        Returns:
            None: 종료를 취소한 경우에만 반환하며, 그 외에는 프로그램 종료.
        """
        if self.save_notice() is not True:

            print("그래도 종료하시겠습니까? : (y : 종료 / n : 취소)")
            try:
                res = check_yes(allow_cancel=False)

            except (KeyboardInterrupt, EOFError):
                print("\n입력이 중단되었습니다. 저장하지 못한 사항은 유지되지 않습니다.")
                raise SystemExit
            if res == 'n':
                print("프로그램 종료를 취소합니다.")
                return 

        print("프로그램을 종료합니다.")
        raise SystemExit

    def run(self):
        """데이터를 불러오고 메뉴를 반복 실행하며 입력 중단 시 종료 처리를 호출합니다."""
        self.load_json()
        
        while True:
            try:
                print_menu(self.menu_list)
                self.select_menu()
            except (KeyboardInterrupt, EOFError):
                #print("\n입력이 중단되어 프로그램을 종료합니다.")
                self.exit_quiz()