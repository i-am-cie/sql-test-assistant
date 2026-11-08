#!/usr/bin/env python3
"""
sql-test-assistant: Local AI SQL testing using Ollama.

Usage:
    python sql_tester.py --quality "用户表手机号唯一性检查"
    python sql_tester.py --test "登录存储过程测试"
    python sql_tester.py --analyze "SELECT * FROM orders WHERE ..."
"""

import argparse
import ollama

MODEL = "qwen2.5:7b"


def generate_data_quality_sql(requirement: str) -> str:
    """Generate data quality check SQL."""
    prompt = f"""你是一个资深数据库测试专家。请为以下数据质量需求生成检查SQL语句。

需求：
{requirement}

请生成以下类型的检查SQL：
1. 唯一性检查（重复数据）
2. 非空检查（空值字段）
3. 格式检查（手机号、邮箱、日期格式）
4. 范围检查（年龄、金额等数值范围）
5. 参照完整性（外键关联有效性）

每个检查用注释说明用途，用MySQL语法。
请输出可直接执行的SQL语句。
"""
    
    resp = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
    return resp["message"]["content"]


def generate_test_cases(description: str) -> str:
    """Generate SQL test cases for stored procedures or business logic."""
    prompt = f"""你是一个资深数据库测试工程师。请为以下数据库逻辑生成测试用例。

描述：
{description}

请生成：
1. 正常场景测试SQL
2. 边界值测试（空值、最大值、最小值）
3. 异常场景测试（非法输入、权限不足）
4. 并发场景测试（如适用）

每个测试用例包含：
- 用例编号和名称
- 测试步骤（SQL语句）
- 预期结果（应该返回什么或状态变化）
- 优先级（P0/P1/P2）

用清晰的Markdown格式输出。
"""
    
    resp = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
    return resp["message"]["content"]


def analyze_sql_performance(sql: str) -> str:
    """Analyze SQL performance and suggest optimizations."""
    prompt = f"""你是一个SQL性能优化专家。请分析以下SQL语句的性能问题。

SQL：
```sql
{sql}
```

请分析：
1. 全表扫描风险
2. 索引使用情况
3. JOIN顺序问题
4. 子查询优化空间
5. 可能的锁表风险

给出具体的优化建议和优化后的SQL语句。
用中文回答。
"""
    
    resp = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
    return resp["message"]["content"]


def review_table_schema(table_desc: str) -> str:
    """Review table schema design."""
    prompt = f"""你是一个数据库架构师。请审查以下表结构设计。

表结构：
{table_desc}

请检查：
1. 字段类型是否合理
2. 主键设计是否合理
3. 索引是否缺失
4. 是否有冗余字段
5. 命名规范是否统一
6. 是否需要添加约束（唯一、非空、默认值）

给出具体的改进建议和DDL语句。
"""
    
    resp = ollama.chat(model=MODEL, messages=[{"role": "user", "content": prompt}])
    return resp["message"]["content"]


def main():
    parser = argparse.ArgumentParser(description="SQL Test Assistant")
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--quality", type=str, help="数据质量检查需求，生成检查SQL")
    group.add_argument("--test", type=str, help="数据库逻辑描述，生成测试用例")
    group.add_argument("--analyze", type=str, help="SQL语句，分析性能问题")
    group.add_argument("--schema", type=str, help="表结构描述，审查设计")
    
    args = parser.parse_args()
    
    if args.quality:
        print("生成数据质量检查SQL中...\n")
        print(generate_data_quality_sql(args.quality))
    elif args.test:
        print("生成测试用例中...\n")
        print(generate_test_cases(args.test))
    elif args.analyze:
        print("分析SQL性能中...\n")
        print(analyze_sql_performance(args.analyze))
    elif args.schema:
        print("审查表结构中...\n")
        print(review_table_schema(args.schema))


if __name__ == "__main__":
    main()
