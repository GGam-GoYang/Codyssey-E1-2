# Git 커밋과 브랜치 이력

저장소: https://github.com/GGam-GoYang/Codyssey-E1-2

기준 커밋: `0f9a51159ed4236b817642e1c8228e2789e3a284` — 51개 커밋

## git log --oneline --graph 실제 조회 출력

```text
* 0f9a511 Feat : 일반 출제와 랜덤 출제 메뉴 분리
*   a699dd5 Merge : 원격 main 변경 통합 및 충돌 해결
|\  
| * 9ffb5be Refactor : 메뉴 입력 함수 간소화
| * 6ccec9a Refactor : 추가 퀴즈 객체를 직접 전달하도록 출력 처리 간소화
| * d7d675f Refactor : print_added_quiz 함수 개선
| * d11dac9 Fix : 미플레이 상태와 0점 종료를 구분을 위한 딕셔너리 Key 추가
| * bc68445 Fix : 임시 파일 저장 후 교체하여 기존 데이터 보호
| *   8b210bf Merge pull request #5 from GGam-GoYang/fix/data-validation
| |\  
| | * 356b3d5 Refactor : 출력 함수 디자인 일부 수정
| | * 10625a7 Docs : docstring 일부 수정
| | * ae48e98 Fix : 종료 확인 중 입력 중단 처리 및 SystemExit 적용
| | * e13cdb0 Fix : 데이터 복구 전 원본 백업 및 백업 실패 시 저장 차단
| | * 6f1249e Refactor : 파일 유효성 검사 기능 보완 및 파일 분리
* | | 367a23b Refactor : Quiz.from_dict로 퀴즈 객체 생성 개선
|/ /  
* | c151dd3 Merge branch 'main' of https://github.com/GGam-GoYang/Codyssey-E1-2
|\| 
| *   33524f4 Merge pull request #4 from GGam-GoYang/refactor/module-split
| |\  
| | *   80cc881 Merge branch 'main' into refactor/module-split
| | |\  
| | |/  
| |/|   
| | * d808cb4 Docs : 코드 내 함수별 docstring 추가
| | * 1e8e636 Fix : 들여쓰기 수정
| | * fde37f4 Refactor : 출력 함수 파일 분리
| | * 67f88a0 Refactor : 클래스 내 출력 함수 기능별 분리
| | * 148520f Refactor : 입력 함수 파일 분리
| | * 93a6321 Refactor : 클래스별 파일 분리
* | | 1378fd2 Docs : 실제 실행 사진 추가
|/ /  
* / 7560b4f Refactor : 출력 함수 중복 제거
|/  
* 26497d2 Refactor : 저장 함수 중복 제거
* cc4871d Refactor : 입력 함수 리팩토링
* 4f2d4bb Feat : 비정상 종료 방지를 위한 종료 함수 구현
*   3ed1106 Merge pull request #3 from GGam-GoYang/feature/quiz-add
|\  
| * b64e6d7 Feat : 퀴즈 추가 기능 구현
|/  
*   463ff8f Merge pull request #2 from GGam-GoYang/feature/data-recovery
|\  
| * e58c6d8 Fix : 데이터 구조 검증 및 예외 처리 추가
| * cefe80b Feat : 데이터 파일 손상 시 예외 처리 및 기본 데이터 복구 구현
| * a81baa8 Feat : 복구용 기본 퀴즈 데이터 추가
|/  
*   7394c3d Merge pull request #1 from GGam-GoYang/feature/quiz-play
|\  
| * 2138f2d FIx : 결과 저장 실패 안내 및 재시도 흐름 보완
| * 7f009e4 Feat : 최고 점수 저장 기능 구현
| * c04df13 주석 일부 수정
| * cb01645 Fix : 퀴즈 개수 0개인 경우 대응 및 주요 함수 주석 추가
| * e5d5756 Refactor : state.json 구조 일부 변경 및 퀴즈 출력 함수 개선
| * fc69460 Feat: 퀴즈 목록 출력 구현
| * b981683 Refactor : 퀴즈 출력 및 정답 판정을 Quiz 클래스로 이관
| * 3015957 Feat: 퀴즈 내용 추가
| * 526feb1 Feat : 퀴즈 풀기 기능 구현
| * 0d2d18a Refactor : Quiz, QuizGame 클래스 재정의
| * f5b2a52 Quizgame 클래스 기초 구현 및 state.json 추가
|/  
* b266ac6 EOF 입력 반영
* be5c04f 입력함수 개선
* 8fad98d 간단한 입∙출력 함수 구현
* ed1950b .gitignore 추가
* b0430d5 Initial commit
```

## 병합 커밋 실제 조회 출력

```text
a699dd5 Merge : 원격 main 변경 통합 및 충돌 해결
8b210bf Merge pull request #5 from GGam-GoYang/fix/data-validation
c151dd3 Merge branch 'main' of https://github.com/GGam-GoYang/Codyssey-E1-2
33524f4 Merge pull request #4 from GGam-GoYang/refactor/module-split
80cc881 Merge branch 'main' into refactor/module-split
3ed1106 Merge pull request #3 from GGam-GoYang/feature/quiz-add
463ff8f Merge pull request #2 from GGam-GoYang/feature/data-recovery
7394c3d Merge pull request #1 from GGam-GoYang/feature/quiz-play
```

