class Quiz():
    def __init__(self, question, choices, answer, source):
        self.question = question
        self.choices = choices 
        self.answer = answer
        self.source = source

    @classmethod
    def from_dict(cls, data):
        """딕셔너리에서 퀴즈 객체를 생성합니다."""
        return cls(
            data["question"],
            data["choices"],
            data["answer"],
            data["source"]
        )
    
    def display(self, idx):
        print("============ 문제 ============")
        print(f"문제 {idx} : {self.question}", end="\n\n")
    
        print("========= 보기 목록 ==========")
        for choice in self.choices:
            print(choice)
        print("==============================")


    def check_answer(self, user_inp):                                   
        return user_inp == self.answer