# SQL Test Assistant

A local SQL testing workbench that asks an [Ollama](https://ollama.com/)-served LLM for data-quality checks, test cases, performance advice and schema reviews — fully offline, no API key.

![Python](https://img.shields.io/badge/Python-3.9%2B-3776AB?logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green)
![LLM](https://img.shields.io/badge/LLM-Ollama-black)
![Offline](https://img.shields.io/badge/Offline-100%25-success)

## What it does

- **Data-quality SQL**: describe constraints such as uniqueness, nullability, format or range and get commented MySQL check queries (uniqueness, non-null, format, range, referential integrity).
- **Test cases for DB logic**: describe a stored procedure or business rule and get normal, boundary, exception and concurrency test cases with SQL steps and P0/P1/P2 priorities.
- **SQL performance review**: paste a query and get a written analysis of full-scan risk, index usage, JOIN order, subquery rewrites and locking risk, plus suggested rewrites.
- **Table-schema review**: paste a `CREATE TABLE` and get advice on column types, primary keys, missing indexes, redundancy, naming and constraints.
- **Local only**: your schemas and SQL stay on your machine; only your local Ollama instance sees them.

## Requirements

- [Ollama](https://ollama.com/) installed and running locally.
- A chat model, default `qwen2.5:7b` (see [Configuration](#configuration)). Any instruction-following model should work, e.g. `qwen2.5:3b` on small machines.
- Python 3.9 or newer.
- No database is required: the tool generates SQL text and does **not** connect to or execute anything.

## Install

```bash
git clone https://github.com/i-am-cie/sql-test-assistant.git
cd sql-test-assistant
pip install -r requirements.txt
```

## Run

```bash
python app.py
```

Then open <http://localhost:5003> in your browser. The Flask development server listens on port `5003`.

## Usage

1. Make sure Ollama is running and the model is pulled: `ollama pull qwen2.5:7b`.
2. Open <http://localhost:5003>.
3. Pick one of the four tabs:
   - **数据质量检查 / Data quality** — describe the checks you need, click **生成检查SQL**.
   - **测试用例生成 / Test cases** — describe the DB logic, click **生成测试用例**.
   - **性能分析 / Performance** — paste a SQL statement, click **分析性能**.
   - **表结构审查 / Schema review** — paste a table definition, click **审查表结构**.
4. Read the generated Markdown in the result panel. Copy the SQL you want to keep — there is no file export.
5. The same four modes are available from the command line:

```bash
python sql_tester.py --quality "用户表 users，检查手机号唯一性、邮箱格式、注册时间非空"
python sql_tester.py --test "用户登录存储过程，连续 5 次失败锁定账号 30 分钟"
python sql_tester.py --analyze "SELECT * FROM orders WHERE user_id IN (SELECT id FROM users WHERE age > 18)"
python sql_tester.py --schema "CREATE TABLE users (id INT PRIMARY KEY, email VARCHAR(100));"
```

## Configuration

There is no configuration file; settings live in the source:

| Setting | Where | Default | Meaning |
| --- | --- | --- | --- |
| Model | `MODEL` in `sql_tester.py` | `qwen2.5:7b` | Ollama model used for every prompt. |
| Ollama endpoint | `OLLAMA_HOST` environment variable | `http://127.0.0.1:11434` | Read automatically by the `ollama` Python client; set it if Ollama runs elsewhere. |
| Web port | `app.run(..., port=5003)` in `app.py` | `5003` | Port of the Flask development server. |
| Dialect | Prompt text (`MySQL语法`) in `sql_tester.py` | MySQL | Data-quality prompts ask the model for MySQL syntax; adjust the prompt for other engines. |

```bash
# example: remote Ollama instance
export OLLAMA_HOST=http://192.168.1.20:11434   # Windows PowerShell: $env:OLLAMA_HOST="..."
```

## How it works

1. The page posts `{type, input}` to `POST /api/generate`.
2. `app.py` maps `type` (`quality` / `test` / `analyze` / `schema`) to the matching function in `sql_tester.py`.
3. Each function fills a Chinese prompt that states the checks or analysis dimensions to cover and calls `ollama.chat(model=MODEL, ...)`.
4. The model's Markdown (SQL snippets, tables, recommendations) is returned unchanged and displayed as plain text.

Nothing is parsed, linted or validated; there is no database connection and no execution of the generated SQL.

## Limitations

- **No database access.** The tool cannot inspect real tables, run `EXPLAIN`, or confirm that generated SQL is valid for your engine.
- **Model quality varies.** Generated SQL may be syntactically wrong, use MySQL-only syntax, or reference columns that do not exist; always review it against your schema.
- **Hallucination risk.** The performance analysis is speculative because the model never sees execution plans or statistics.
- **Default dialect is MySQL** in the data-quality prompt; other engines may need prompt tweaks.
- **Text only, no export.** Results are shown in the page and lost on refresh; copy them manually.
- **Not a migration/schema-change tool.** It only produces advice and example DDL; it never applies changes.
- **Single user, no authentication.** The Flask app runs with `debug=True` and is intended for `localhost` only.
- **Chinese prompts.** Prompts are in Chinese, so output is usually Chinese.

## License

MIT © 2026 i-am-cie — see [LICENSE](LICENSE).

## 中文说明

这是一个本地 AI SQL 测试助手：通过本机 Ollama 大模型，根据自然语言需求生成数据质量检查 SQL、数据库逻辑测试用例，对 SQL 语句做性能分析与优化建议，并审查表结构设计。支持网页四种模式，也提供命令行 `--quality / --test / --analyze / --schema`。所有数据都在本机，无需 API Key，也不需要连接数据库——工具只生成 SQL 文本，不会执行。使用前安装 Ollama 并拉取 `qwen2.5:7b`，然后 `pip install -r requirements.txt`、`python app.py`，浏览器打开 http://localhost:5003。生成的 SQL 需人工核对后再执行。
