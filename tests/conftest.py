"""Pytest 共享配置：把项目根目录加入导入路径，并在未安装 ollama 包时注入占位模块。"""

import sys
import types
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# 未安装 ollama Python 包时注入占位模块；测试用例通过 unittest.mock 替换 ollama.chat。
if "ollama" not in sys.modules:
    fake_ollama = types.ModuleType("ollama")
    fake_ollama.chat = lambda **kwargs: {"message": {"content": ""}}
    sys.modules["ollama"] = fake_ollama
