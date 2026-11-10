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