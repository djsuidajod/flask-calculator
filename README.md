# 🖩 Flask Calculator (Basic & Scientific)

A **web-based calculator** built with **Python Flask** and **PostgreSQL**, supporting both basic arithmetic and advanced scientific functions.  
Each mode stores results in a separate database table for easy management.

---

## 📑 Table of Contents
1. [✨ Features](#-features)
2. [🗄 Database Structure](#-database-structure)
3. [🚀 Installation & Usage](#-installation--usage)
4. [📷 Screenshots](#-screenshots)
5. [📄 License](#-license)

---

## ✨ Features

### 🔹 Basic Calculator
- ➕ ➖ ✖ ➗ Arithmetic operations (`+`, `-`, `*`, `/`)
- ➿ Parentheses support
- 🛡 Safe parsing without using `eval()`
- 💾 Saves results to `history` table

### 🔹 Scientific Calculator
- 📐 Powered by Python `math` module
- 🧮 Functions: `sin`, `cos`, `tan`, `log`, `sqrt`, `pow`, `pi`, `e`, etc.
- 🛡 Executes only whitelisted functions
- 💾 Saves results to `sci_history` table

### 🔹 Common Features
- 📜 View calculation history for each mode
- ♻ Clear history (delete data & reset ID sequence)
- 🔄 Dynamic placeholder & mode label updates

---

## 🗄 Database Structure

**`history` Table** (Basic Calculator)  
| Column      | Type              | Description          |
|-------------|-------------------|----------------------|
| id          | SERIAL PRIMARY KEY| Record ID            |
| expression  | TEXT              | Input expression     |
| result      | DOUBLE PRECISION  | Calculation result   |
| created_at  | TIMESTAMP         | Record creation time |

**`sci_history` Table** (Scientific Calculator)  
| Column      | Type              | Description          |
|-------------|-------------------|----------------------|
| id          | SERIAL PRIMARY KEY| Record ID            |
| expression  | TEXT              | Input expression     |
| result      | DOUBLE PRECISION  | Calculation result   |
| created_at  | TIMESTAMP         | Record creation time |

---

## 🚀 Installation & Usage

1. **Clone the repository**
```bash
git clone https://github.com/djsuidajod/flask-calculator.git
cd flask-calculator
