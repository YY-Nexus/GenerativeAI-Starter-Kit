# 🚀 发布指南

## ✅ 本地发布流程

```bash
python3.11 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
pip install bump-my-version twine
bump-my-version patch
python setup.py sdist bdist_wheel
twine upload dist/*
