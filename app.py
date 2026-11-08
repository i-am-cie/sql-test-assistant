#!/usr/bin/env python3
"""
sql-test-assistant Web UI (Flask)
"""

from flask import Flask, render_template_string, request, jsonify
from sql_tester import generate_data_quality_sql, generate_test_cases, analyze_sql_performance, review_table_schema

app = Flask(__name__)

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SQL Test Assistant</title>
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            min-height: 100vh;
            padding: 20px;
        }
        .container { max-width: 1100px; margin: 0 auto; }
        h1 { color: white; text-align: center; margin-bottom: 30px; font-size: 2.5rem; }
        .card {
            background: white;
            border-radius: 16px;
            padding: 30px;
            box-shadow: 0 20px 60px rgba(0,0,0,0.2);
            margin-bottom: 20px;
        }
        .tabs { display: flex; gap: 10px; margin-bottom: 20px; flex-wrap: wrap; }
        .tab {
            padding: 12px 20px;
            border-radius: 8px;
            cursor: pointer;
            background: #f0f0f0;
            border: none;
            font-size: 0.95rem;
            transition: all 0.3s;
        }
        .tab.active { background: #f5576c; color: white; }
        textarea {
            width: 100%;
            min-height: 120px;
            padding: 15px;
            border: 2px solid #e0e0e0;
            border-radius: 8px;
            font-size: 14px;
            font-family: 'Courier New', monospace;
            resize: vertical;
            margin-bottom: 15px;
        }
        textarea:focus { outline: none; border-color: #f5576c; }
        button {
            background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
            color: white;
            border: none;
            padding: 12px 30px;
            border-radius: 8px;
            font-size: 1rem;
            cursor: pointer;
            transition: transform 0.2s;
        }
        button:hover { transform: translateY(-2px); }
        button:disabled { opacity: 0.6; cursor: not-allowed; }
        .result {
            margin-top: 20px;
            padding: 20px;
            background: #f8f9fa;
            border-radius: 8px;
            white-space: pre-wrap;
            display: none;
            line-height: 1.6;
            font-size: 14px;
        }
        .result.show { display: block; }
        .loading { text-align: center; display: none; padding: 20px; }
        .loading.show { display: block; }
        .spinner {
            border: 4px solid #f3f3f3;
            border-top: 4px solid #f5576c;
            border-radius: 50%;
            width: 40px;
            height: 40px;
            animation: spin 1s linear infinite;
            margin: 0 auto 10px;
        }
        @keyframes spin { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }
        .tab-content { display: none; }
        .tab-content.active { display: block; }
    </style>
</head>
<body>
    <div class="container">
        <h1>🗄️ SQL Test Assistant</h1>
        
        <div class="card">
            <div class="tabs">
                <button class="tab active" onclick="switchTab('quality')">数据质量检查</button>
                <button class="tab" onclick="switchTab('test')">测试用例生成</button>
                <button class="tab" onclick="switchTab('analyze')">性能分析</button>
                <button class="tab" onclick="switchTab('schema')">表结构审查</button>
            </div>

            <div id="tab-quality" class="tab-content active">
                <textarea id="quality-input" placeholder="描述数据质量检查需求...
例如：用户表users，需要检查手机号唯一性、邮箱格式、注册时间不为空"></textarea>
                <button onclick="generate('quality')">生成检查SQL</button>
            </div>

            <div id="tab-test" class="tab-content">
                <textarea id="test-input" placeholder="描述数据库逻辑...
例如：用户登录存储过程，验证连续5次失败锁定账号30分钟"></textarea>
                <button onclick="generate('test')">生成测试用例</button>
            </div>

            <div id="tab-analyze" class="tab-content">
                <textarea id="analyze-input" placeholder="粘贴SQL语句...
SELECT * FROM orders WHERE user_id IN (SELECT id FROM users WHERE age > 18)"></textarea>
                <button onclick="generate('analyze')">分析性能</button>
            </div>

            <div id="tab-schema" class="tab-content">
                <textarea id="schema-input" placeholder="粘贴表结构...
CREATE TABLE users (
  id INT PRIMARY KEY,
  username VARCHAR(50),
  email VARCHAR(100),
  age INT
);"></textarea>
                <button onclick="generate('schema')">审查表结构</button>
            </div>

            <div class="loading" id="loading">
                <div class="spinner"></div>
                <p>AI 正在分析中...</p>
            </div>

            <div class="result" id="result"></div>
        </div>
    </div>

    <script>
        let currentTab = 'quality';
        
        function switchTab(tab) {
            currentTab = tab;
            document.querySelectorAll('.tab').forEach((t, i) => {
                t.classList.remove('active');
            });
            event.target.classList.add('active');
            
            document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
            document.getElementById('tab-' + tab).classList.add('active');
        }
        
        async function generate(type) {
            const inputMap = {
                quality: document.getElementById('quality-input').value,
                test: document.getElementById('test-input').value,
                analyze: document.getElementById('analyze-input').value,
                schema: document.getElementById('schema-input').value
            };
            
            const input = inputMap[type];
            if (!input.trim()) {
                alert('请输入内容');
                return;
            }
            
            document.getElementById('loading').classList.add('show');
            document.getElementById('result').classList.remove('show');
            
            const response = await fetch('/api/generate', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({type, input})
            });
            
            const data = await response.json();
            
            document.getElementById('loading').classList.remove('show');
            document.getElementById('result').textContent = data.result;
            document.getElementById('result').classList.add('show');
        }
    </script>
</body>
</html>
"""


@app.route('/')
def index():
    return render_template_string(HTML_TEMPLATE)


@app.route('/api/generate', methods=['POST'])
def api_generate():
    data = request.json
    gen_type = data.get('type')
    user_input = data.get('input', '')
    
    if gen_type == 'quality':
        result = generate_data_quality_sql(user_input)
    elif gen_type == 'test':
        result = generate_test_cases(user_input)
    elif gen_type == 'analyze':
        result = analyze_sql_performance(user_input)
    elif gen_type == 'schema':
        result = review_table_schema(user_input)
    else:
        result = '未知的类型'
    
    return jsonify({'result': result})


if __name__ == '__main__':
    print("🗄️  SQL Test Assistant 启动中...")
    print("📖 访问 http://localhost:5003")
    app.run(debug=True, port=5003)
