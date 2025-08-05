from flask import Flask, render_template, request, redirect, url_for, flash
import re
import psycopg2
import os
import math
from psycopg2.extras import RealDictCursor

app = Flask(__name__)
app.secret_key = "change-this"  # flash 메시지 기능

# 기능: DB 연결 설정
DB_CONFIG = {
    'dbname': os.getenv('PG_DB', 'mydb'),
    'user': os.getenv('PG_USER', 'postgres'),
    'password': os.getenv('PG_PW', 'jun134679'),
    'host': os.getenv('PG_HOST', 'localhost'),
    'port': int(os.getenv('PG_PORT', '5432')),
}

# ===== 기능: 일반 계산기(사칙연산) 파서 =====
def skip_spaces(expr): return expr.lstrip()

def parse_number(expr):
    expr = skip_spaces(expr)
    m = re.match(r'\d+(\.\d+)?', expr)
    if not m:
        raise ValueError("숫자가 필요합니다.")
    num = float(m.group())
    return num, expr[len(m.group()):]

def parse_factor(expr):
    expr = skip_spaces(expr)
    if expr.startswith('('):
        val, rest = parse_expression(expr[1:])
        rest = skip_spaces(rest)
        if not rest.startswith(')'):
            raise ValueError("')'가 필요합니다.")
        return val, rest[1:]
    return parse_number(expr)

def parse_term(expr):
    val, rest = parse_factor(expr)
    while True:
        rest = skip_spaces(rest)
        if rest.startswith('*'):
            nv, rest = parse_factor(rest[1:]); val *= nv
        elif rest.startswith('/'):
            nv, rest = parse_factor(rest[1:]); val /= nv
        else:
            break
    return val, rest

def parse_expression(expr):
    val, rest = parse_term(expr)
    while True:
        rest = skip_spaces(rest)
        if rest.startswith('+'):
            nv, rest = parse_term(rest[1:]); val += nv
        elif rest.startswith('-'):
            nv, rest = parse_term(rest[1:]); val -= nv
        else:
            break
    return val, rest

def calculate_expression(expr):
    val, rem = parse_expression(expr)
    if skip_spaces(rem):
        raise ValueError("잘못된 수식입니다.")
    return val

# ===== 기능: 공학 계산기(math 모듈 사용: sin, cos, log, sqrt 등) =====
def calculate_scientific(expr):
    allowed = {k: v for k, v in math.__dict__.items() if not k.startswith("__")}
    code = compile(expr, "<string>", "eval")
    for name in code.co_names:
        if name not in allowed:
            raise NameError(f"허용되지 않은 함수: {name}")
    return eval(code, {"__builtins__": {}}, allowed)

# ===== 기능: DB 저장/조회/초기화 =====
def add_to_history(expr, result):
    with psycopg2.connect(**DB_CONFIG) as conn, conn.cursor() as cur:
        cur.execute("INSERT INTO history (expression, result) VALUES (%s, %s);", (expr, result))
        conn.commit()

def add_to_sci_history(expr, result):
    with psycopg2.connect(**DB_CONFIG) as conn, conn.cursor() as cur:
        cur.execute("INSERT INTO sci_history (expression, result) VALUES (%s, %s);", (expr, result))
        conn.commit()

def fetch_history():
    with psycopg2.connect(**DB_CONFIG) as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT id, expression, result, created_at
            FROM history
            ORDER BY id DESC
            LIMIT 100;
        """)
        return cur.fetchall()

def fetch_sci_history():
    with psycopg2.connect(**DB_CONFIG) as conn, conn.cursor(cursor_factory=RealDictCursor) as cur:
        cur.execute("""
            SELECT id, expression, result, created_at
            FROM sci_history
            ORDER BY id DESC
            LIMIT 100;
        """)
        return cur.fetchall()

def reset_serial_sequence(conn, table_name, id_column="id"):
    """기능: 테이블 비우고 시퀀스 ID를 1부터 다시 시작"""
    with conn.cursor() as cur:
        # 해당 테이블의 시퀀스 이름을 동적으로 조회
        cur.execute("SELECT pg_get_serial_sequence(%s, %s);", (table_name, id_column))
        seq_row = cur.fetchone()
        seq_name = seq_row[0] if seq_row else None
        if seq_name:
            cur.execute(f"ALTER SEQUENCE {seq_name} RESTART WITH 1;")

def clear_history_and_reset():
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM history;")
        reset_serial_sequence(conn, 'history', 'id')
        conn.commit()

def clear_sci_history_and_reset():
    with psycopg2.connect(**DB_CONFIG) as conn:
        with conn.cursor() as cur:
            cur.execute("DELETE FROM sci_history;")
        reset_serial_sequence(conn, 'sci_history', 'id')
        conn.commit()

# ===== 기능: 라우팅 =====
@app.route("/", methods=["GET"])
def index():
    """기능: 메인 화면(일반/공학 이력 동시 표시)"""
    try:
        rows_basic = fetch_history()
    except Exception as e:
        rows_basic = []
        flash(f"일반 이력 조회 오류: {e}")
    try:
        rows_sci = fetch_sci_history()
    except Exception as e:
        rows_sci = []
        flash(f"공학 이력 조회 오류: {e}")
    return render_template("index.html", rows_basic=rows_basic, rows_sci=rows_sci)

@app.route("/calc", methods=["POST"])
def calc():
    """기능: 계산 처리(모드에 따라 다른 엔진 + 다른 테이블에 저장)"""
    expr = (request.form.get("expression") or "").strip()
    mode = request.form.get("mode", "basic")

    if not expr:
        flash("수식을 입력하세요.")
        return redirect(url_for("index"))

    try:
        if mode == "basic":
            result = calculate_expression(expr)
            add_to_history(expr, result)        # 일반 결과 저장
        elif mode == "sci":
            result = calculate_scientific(expr)
            add_to_sci_history(expr, result)    # 공학 결과 저장(별도 테이블)
        else:
            raise ValueError("잘못된 모드")
        flash(f"결과: {result:.6f}")
    except Exception as e:
        flash(f"오류: {e}")

    return redirect(url_for("index"))

@app.route("/history/clear", methods=["POST"])
def history_clear():
    """기능: 일반 이력 전체 삭제 + ID 리셋"""
    try:
        clear_history_and_reset()
        flash("일반 계산기 이력이 삭제되고 ID가 초기화되었습니다.")
    except Exception as e:
        flash(f"삭제 오류: {e}")
    return redirect(url_for("index"))

@app.route("/sci_history/clear", methods=["POST"])
def sci_history_clear():
    """기능: 공학 이력 전체 삭제 + ID 리셋"""
    try:
        clear_sci_history_and_reset()
        flash("공학 계산기 이력이 삭제되고 ID가 초기화되었습니다.")
    except Exception as e:
        flash(f"삭제 오류: {e}")
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True)
