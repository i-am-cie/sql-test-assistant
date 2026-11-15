"""
sql_tester.py 的单元测试。

ollama 调用通过 unittest.mock 打桩，测试不发起真实模型请求，
也不依赖 ollama Python 包是否安装（见 conftest.py）。
覆盖：模型调用契约、四种 SQL 模式的 prompt 拼装、命令行分发。
"""

import sys
from unittest.mock import MagicMock, patch

import sql_tester as st


def _fake_ollama(content: str) -> MagicMock:
    return MagicMock(return_value={"message": {"content": content}})


def _captured_prompt(mock_chat: MagicMock) -> str:
    return mock_chat.call_args.kwargs["messages"][0]["content"]


# ---------- 模型调用契约 + prompt 拼装 ----------

def test_quality_sql_prompt_includes_requirement():
    requirement = "用户表手机号唯一性检查"
    mock_chat = _fake_ollama("质量检查SQL")
    with patch.object(st.ollama, "chat", mock_chat):
        result = st.generate_data_quality_sql(requirement)

    assert result == "质量检查SQL"
    prompt = _captured_prompt(mock_chat)
    assert requirement in prompt
    assert "唯一性检查" in prompt


def test_test_cases_prompt_includes_description():
    description = "登录存储过程，连续5次失败锁定账号30分钟"
    mock_chat = _fake_ollama("数据库测试用例")
    with patch.object(st.ollama, "chat", mock_chat):
        result = st.generate_test_cases(description)

    assert result == "数据库测试用例"
    prompt = _captured_prompt(mock_chat)
    assert description in prompt
    assert "边界值测试" in prompt
    assert "优先级" in prompt


def test_analyze_prompt_includes_sql():
    sql = "SELECT * FROM orders WHERE user_id IN (SELECT id FROM users)"
    mock_chat = _fake_ollama("性能分析结论")
    with patch.object(st.ollama, "chat", mock_chat):
        result = st.analyze_sql_performance(sql)

    assert result == "性能分析结论"
    prompt = _captured_prompt(mock_chat)
    assert sql in prompt
    assert "全表扫描风险" in prompt


def test_schema_prompt_includes_table_desc():
    table_desc = "CREATE TABLE users (id INT PRIMARY KEY, email VARCHAR(100));"
    mock_chat = _fake_ollama("表结构审查结论")
    with patch.object(st.ollama, "chat", mock_chat):
        result = st.review_table_schema(table_desc)

    assert result == "表结构审查结论"
    prompt = _captured_prompt(mock_chat)
    assert table_desc in prompt
    assert "主键设计" in prompt


def test_each_call_uses_configured_model():
    mock_chat = _fake_ollama("ok")
    with patch.object(st.ollama, "chat", mock_chat):
        st.generate_data_quality_sql("手机号唯一性")
    assert mock_chat.call_args.kwargs["model"] == st.MODEL


# ---------- main() 命令行分发 ----------

def test_main_quality_flag_calls_data_quality_sql():
    with patch.object(st, "generate_data_quality_sql") as mock_fn, \
         patch.object(sys, "argv", ["sql_tester.py", "--quality", "手机号唯一性"]):
        st.main()
    mock_fn.assert_called_once_with("手机号唯一性")


def test_main_test_flag_calls_generate_test_cases():
    with patch.object(st, "generate_test_cases") as mock_fn, \
         patch.object(sys, "argv", ["sql_tester.py", "--test", "登录存储过程"]):
        st.main()
    mock_fn.assert_called_once_with("登录存储过程")


def test_main_analyze_flag_calls_performance_analysis():
    with patch.object(st, "analyze_sql_performance") as mock_fn, \
         patch.object(sys, "argv", ["sql_tester.py", "--analyze", "SELECT 1"]):
        st.main()
    mock_fn.assert_called_once_with("SELECT 1")


def test_main_schema_flag_calls_review_table_schema():
    with patch.object(st, "review_table_schema") as mock_fn, \
         patch.object(sys, "argv", ["sql_tester.py", "--schema", "CREATE TABLE users (id INT)"]):
        st.main()
    mock_fn.assert_called_once_with("CREATE TABLE users (id INT)")
