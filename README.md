# SQL Test Assistant

> 本地AI SQL测试助手，基于 Ollama 大模型，完全离线运行，无需 API Key。

## ✨ 功能特性

- **生成测试SQL**：输入业务逻辑，自动生成测试查询语句
- **数据质量检查**：自动生成数据完整性、一致性、唯一性检查SQL
- **测试用例生成**：针对存储过程、触发器生成边界测试用例
- **慢查询分析**：AI分析SQL执行计划，给出优化建议
- **表结构审查**：审查表设计是否合理，索引是否缺失
- **完全本地**：所有数据都在你的电脑上

## 🚀 快速开始

### 前置要求

1. 安装 [Ollama](https://ollama.com/)
2. 拉取模型：
   ```bash
   ollama pull qwen2.5:7b
   ```

### 安装依赖

```bash
pip install -r requirements.txt
```

### 启动 Web 界面

```bash
python app.py
```

打开浏览器访问 http://localhost:5003

### 命令行模式

```bash
# 生成数据质量检查SQL
python sql_tester.py --quality "用户表users，需要检查手机号唯一性、邮箱格式、注册时间不为空"

# 生成测试用例SQL
python sql_tester.py --test "用户登录存储过程，验证连续5次失败锁定账号"

# 分析慢查询
python sql_tester.py --analyze "SELECT * FROM orders WHERE user_id IN (SELECT id FROM users WHERE age > 18)"
```

## 📦 项目结构

```
sql-test-assistant/
├── app.py              # Flask Web 界面
├── sql_tester.py       # 核心SQL测试逻辑
├── requirements.txt    # Python 依赖
└── README.md
```

## 🛠️ 技术栈

- **后端**：Python + Flask
- **LLM**：Ollama (Qwen2.5)
- **前端**：HTML + 原生 JS

## 📝 License

MIT