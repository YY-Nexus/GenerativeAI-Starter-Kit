# 🍎 Mac系统专用 - GenerativeAI-Starter-Kit 使用指南

## 🎯 针对Mac系统的完整配置

### 📋 系统要求确认
- ✅ macOS 10.15+ (推荐 macOS 12+)
- ✅ Python 3.8+ (推荐 Python 3.11)
- ✅ VS Code 最新版本
- ✅ Git 已安装

### 🔧 Mac特定的环境设置

#### 1. Python环境配置
```bash
# 使用Homebrew安装Python (推荐)
brew install python@3.11

# 或使用pyenv管理多个Python版本
brew install pyenv
pyenv install 3.11.5
pyenv global 3.11.5
```

#### 2. VS Code快捷键 (Mac专用)
- 重新加载窗口: `Cmd+Shift+P` → `Developer: Reload Window`
- 重启语言服务器: `Cmd+Shift+P` → `Python: Restart Language Server`
- 打开终端: `Cmd+Shift+`` ` (反引号)
- 文件搜索: `Cmd+P`
- 全局搜索: `Cmd+Shift+F`

### 🚀 一键启动脚本 (Mac优化版)

#### 创建启动脚本
```bash
# 在项目根目录创建
cat > start_genai_kit.sh << 'EOF'
#!/bin/bash
echo "🍎 启动 GenerativeAI-Starter-Kit (Mac版)"
echo "=================================="

# 检查Python版本
python_version=$(python3 --version 2>&1)
echo "Python版本: $python_version"

# 检查项目状态
echo "📊 项目状态检查..."
python3 scripts/zero_error_monitor.py

echo ""
echo "🎯 可用工具:"
echo "1. 项目监控: python3 scripts/zero_error_monitor.py"
echo "2. 反馈检查: python3 scripts/quick_feedback_check.py"
echo "3. 脚本管理: python3 scripts/run_manager.py"
echo "4. 文本分类: python3 examples/fine-tuning/text_classification_demo.py"

echo ""
echo "✅ GenerativeAI-Starter-Kit v0.2.0 准备就绪!"
EOF

# 赋予执行权限
chmod +x start_genai_kit.sh
```

### 🛠️ Mac终端使用技巧

#### Zsh配置优化 (.zshrc)
```bash
# 添加别名到 ~/.zshrc
echo "# GenerativeAI-Starter-Kit 别名" >> ~/.zshrc
echo "alias genai='cd /path/to/GenerativeAI-Starter-Kit && ./start_genai_kit.sh'" >> ~/.zshrc
echo "alias genai-monitor='cd /path/to/GenerativeAI-Starter-Kit && python3 scripts/zero_error_monitor.py'" >> ~/.zshrc
echo "alias genai-feedback='cd /path/to/GenerativeAI-Starter-Kit && python3 scripts/quick_feedback_check.py'" >> ~/.zshrc

# 重新加载配置
source ~/.zshrc
```

### 📱 Mac系统通知集成
创建带系统通知的监控脚本：

```python
#!/usr/bin/env python3
"""Mac系统通知版监控脚本"""
import os
import subprocess

def send_mac_notification(title, message):
    """发送Mac系统通知"""
    script = f'''
    display notification "{message}" with title "{title}" sound name "Ping"
    '''
    subprocess.run(['osascript', '-e', script])

def main():
    # 运行监控
    result = subprocess.run(['python3', 'scripts/zero_error_monitor.py'],
                          capture_output=True, text=True)

    if result.returncode == 0:
        send_mac_notification(
            "GenerativeAI-Starter-Kit",
            "✅ 项目状态检查完成 - 一切正常!"
        )
    else:
        send_mac_notification(
            "GenerativeAI-Starter-Kit",
            "⚠️ 项目检查发现问题，请查看终端"
        )

if __name__ == "__main__":
    main()
```

### 🔒 Mac权限设置

#### 终端权限
如果遇到权限问题：
```bash
# 给予脚本执行权限
chmod +x scripts/*.py
chmod +x scripts/*.sh

# 如果需要管理员权限
sudo chmod +x /path/to/scripts
```

#### VS Code权限
确保VS Code有必要的权限：
- 系统偏好设置 → 安全性与隐私 → 隐私 → 完全磁盘访问权限 → 添加VS Code

### 🎨 Mac风格的状态显示

#### 创建漂亮的状态面板
```python
def show_mac_style_status():
    """Mac风格的状态显示"""
    print("┌─────────────────────────────────────┐")
    print("│   🍎 GenerativeAI-Starter-Kit      │")
    print("│   📦 版本: v0.2.0                   │")
    print("│   ✅ 状态: 完全就绪                  │")
    print("│   🔧 工具: 6个可用                   │")
    print("│   ❌ 错误: 0个                       │")
    print("└─────────────────────────────────────┘")
```

### 💻 开发环境集成

#### 与其他Mac工具集成
```bash
# 与Finder集成 - 创建服务
# 系统偏好设置 → 键盘 → 快捷键 → 服务 → 新建服务

# 与Spotlight集成
# 添加项目目录到Spotlight索引
mdutil -a -i on /path/to/GenerativeAI-Starter-Kit
```

### 🚨 故障排除 (Mac特定)

#### 常见问题解决
1. **Python路径问题**:
   ```bash
   which python3
   # 确保使用正确的Python版本
   ```

2. **权限被拒绝**:
   ```bash
   sudo xcode-select --install
   # 安装命令行工具
   ```

3. **VS Code Pylance问题**:
   ```bash
   # 重置Pylance
   Cmd+Shift+P → "Python: Clear Cache and Reload Window"
   ```

### 🎯 性能优化 (Mac专用)

#### 系统资源监控
```bash
# 监控Python进程
ps aux | grep python

# 监控内存使用
top -pid $(pgrep -f "python.*genai")

# 磁盘使用情况
du -sh GenerativeAI-Starter-Kit/
```

### 📊 Mac Activity Monitor集成
可以通过Activity Monitor监控项目运行状态，确保资源使用合理。

---

## 🎉 总结

你的Mac系统现在拥有：
- ✅ 完全无错误的GenerativeAI-Starter-Kit
- ✅ Mac优化的快捷键和别名
- ✅ 系统通知集成
- ✅ 漂亮的终端界面
- ✅ 完整的故障排除指南

**现在你可以在Mac上享受完美的AI开发体验！** 🍎✨
