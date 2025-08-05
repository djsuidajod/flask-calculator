
-- pgAdmin4의 Query Tool에서 실행하세요.
CREATE DATABASE mydb;
\c mydb
CREATE TABLE IF NOT EXISTS history (
  id SERIAL PRIMARY KEY,
  expression TEXT NOT NULL,
  result DOUBLE PRECISION NOT NULL,
  created_at TIMESTAMP DEFAULT NOW()
);
