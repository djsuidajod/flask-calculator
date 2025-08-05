# 🖩 Flask 계산기 (일반 & 공학)

**Python Flask**와 **PostgreSQL**로 구현한 웹 기반 계산기입니다.  
일반 사칙연산뿐만 아니라 공학용 수학 함수를 지원하며,  
각 모드별 결과를 별도의 데이터베이스 테이블에 저장하여 관리합니다.

---

## 📑 목차
1. [✨ 주요 기능](#-주요-기능)
2. [🗄 데이터베이스 구조](#-데이터베이스-구조)
3. [🚀 설치 및 실행 방법](#-설치-및-실행-방법)
4. [📷 화면 예시](#-화면-예시)
5. [📄 라이선스](#-라이선스)

---

## ✨ 주요 기능

### 🔹 일반 계산기
- ➕ ➖ ✖ ➗ 사칙연산(`+`, `-`, `*`, `/`)
- ➿ 괄호 연산 지원
- 🛡 `eval()` 미사용, 안전한 파서 직접 구현
- 💾 결과를 `history` 테이블에 저장

### 🔹 공학 계산기
- 📐 Python `math` 모듈 기반
- 🧮 지원 함수: `sin`, `cos`, `tan`, `log`, `sqrt`, `pow`, `pi`, `e` 등
- 🛡 허용된 함수만 실행 가능(화이트리스트 방식)
- 💾 결과를 `sci_history` 테이블에 저장

### 🔹 공통 기능
- 📜 각 모드별 계산 이력 조회
- ♻ 이력 초기화(데이터 삭제 + ID 시퀀스 초기화)
- 🔄 모드 선택 시 입력 예시(placeholder)와 모드 라벨 동적 변경

---

## 🗄 데이터베이스 구조

**`history` 테이블** (일반 계산기)  
| 컬럼명       | 타입               | 설명               |
|--------------|-------------------|--------------------|
| id           | SERIAL PRIMARY KEY| 고유 ID            |
| expression   | TEXT              | 입력 수식          |
| result       | DOUBLE PRECISION  | 계산 결과          |
| created_at   | TIMESTAMP         | 생성 시각          |

**`sci_history` 테이블** (공학 계산기)  
| 컬럼명       | 타입               | 설명               |
|--------------|-------------------|--------------------|
| id           | SERIAL PRIMARY KEY| 고유 ID            |
| expression   | TEXT              | 입력 수식          |
| result       | DOUBLE PRECISION  | 계산 결과          |
| created_at   | TIMESTAMP         | 생성 시각          |

---

## 🚀 설치 및 실행 방법

1. **저장소 클론**
```bash
git clone https://github.com/djsuidajod/flask-calculator.git
cd flask-calculator
