def validate_quiz(item, idx):
    """퀴즈 항목의 유효성을 검사합니다.

    Args:
        item (dict): 퀴즈 항목을 나타내는 딕셔너리.
        idx (int): 퀴즈 항목의 인덱스.

    Raises:
        ValueError: 퀴즈 항목이 유효하지 않은 경우 발생합니다.
    """
    if not isinstance(item, dict):
        raise ValueError(f"quizzes[{idx}]은 딕셔너리여야 합니다.")

    if not isinstance(item.get("question"), str) or not item["question"].strip():
        raise ValueError(f"quizzes[{idx}]['question']은 빈 문자열이 아닌 문자열이어야 합니다.")

    if not isinstance(item.get("choices"), list) or len(item["choices"]) != 4:
        raise ValueError(f"quizzes[{idx}]['choices']은 길이가 4인 리스트여야 합니다.")

    if any(not isinstance(choice, str) or not choice.strip() for choice in item["choices"]):
        raise ValueError(f"quizzes[{idx}]['choices']의 모든 항목은 빈 문자열이 아닌 문자열이어야 합니다.")

    if type(item.get("answer")) is not int or not 1 <= item["answer"] <= 4:
        raise ValueError(f"quizzes[{idx}]['answer']은 1~4 사이의 정수여야 합니다.")

    if item.get("source") not in ("default", "user"):
        raise ValueError(f"quizzes[{idx}]['source']은 \"default\" 또는 \"user\"이여야 합니다.")

def validate_state(data):
    """저장된 상태 데이터의 유효성을 검사합니다.

    Args:
        data (dict): 저장된 상태 데이터를 나타내는 딕셔너리.

    Raises:
        ValueError: 상태 데이터가 유효하지 않은 경우 발생합니다.
    """
    if not isinstance(data, dict):
        raise ValueError("최상위 데이터는 딕셔너리여야 합니다.")

    if "has_played" in data and type(data["has_played"]) is not bool:
        raise ValueError("has_played는 Boolean 이어야 합니다.")

    quizzes = data.get("quizzes")
    if not isinstance(quizzes, list):
        raise ValueError("quizzes는 리스트여야 합니다.")

    for idx, item in enumerate(quizzes):
        validate_quiz(item, idx)

    high_score = data.get("high_score", 0)
    if type(high_score) is not int or high_score < 0:
        raise ValueError("high_score는 0 이상의 정수여야 합니다.")