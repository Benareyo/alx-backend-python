# ALX Backend Python 

Welcome to the **ALX Backend Python** repository! 🚀

This repository contains solutions for milestone backend Python projects in the ALX Software Engineering program, with a focus on decorators, generators, context managers, and async operations using SQLite.

---

## 🔍 Project Overview

### 🔧 Python Decorators Project (`python-decorators-0x01`)

Custom Python decorators used to enhance database operations:

* ✅ `@log_queries`: Logs SQL queries before executing.
* ✅ `@with_db_connection`: Manages opening/closing DB connections.
* ✅ `@transactional`: Commits/rolls back DB operations safely.
* ✅ `@retry_on_failure`: Retries transient DB errors.
* ✅ `@cache_query`: Avoids redundant DB calls by caching query results.

📁 Tasks: 

| Task | Description            | File                      |
| ---- | ---------------------- | ------------------------- |
| 0    | Log queries            | `0-log_queries.py`        |
| 1    | Handle DB connection   | `1-with_db_connection.py` |
| 2    | Transaction management | `2-transactional.py`      |
| 3    | Retry on failure       | `3-retry_on_failure.py`   |
| 4    | Query caching          | `4-cache_query.py`        |

---

### 🔁 Python Generators Project (`python-generators-0x00`)

Memory-efficient data processing using generators:

* Stream user data row-by-row
* Batch users
* Lazy pagination
* Yield user ages and compute average without using SQL AVG

---

### ⚙️ Context Managers & Async DB (`python-context-async-perations-0x02`)

Advanced resource handling and concurrency:

* Custom class-based context managers
* Async queries using `aiosqlite` + `asyncio`

📁 Tasks:

| Task | Description                          | File                      |
| ---- | ------------------------------------ | ------------------------- |
| 0    | `DatabaseConnection` context manager | `0-databaseconnection.py` |
| 1    | Reusable query manager with params   | `1-execute.py`            |
| 2    | Concurrent async queries             | `3-concurrent.py`         |
| 3    | Manual QA Review                     | *Folder only*             |

---

## 🛠️ Requirements

* Python 3.8+
* `sqlite3` (default in Python)
* `aiosqlite` (for async tasks)
* Git + GitHub

---

## ▶️ How to Run

```bash
# Setup DB (if needed)
python python-decorators-0x01/init_db.py

# Run any task
python python-decorators-0x01/0-log_queries.py
```

---

## 👤 Author

**Betel Yohannes**
🎓 ALX SE Student
🔗 [LinkedIn](https://www.linkedin.com/in/betel-yohannes-24aa04320/)

---

## 🤝 Contributions

This is a personal learning repo, but suggestions are welcome!
