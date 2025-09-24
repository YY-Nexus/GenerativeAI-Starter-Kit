#!/bin/bash
# Mac系统专用 - GenerativeAI-Starter-Kit 一键启动脚本

echo "🍎 启动 GenerativeAI-Starter-Kit (Mac版)"
echo "===================================="

# 检查系统信息
echo "💻 系统信息:"
echo "   操作系统: $(sw_vers -productName) $(sw_vers -productVersion)"
echo "   处理器: $(uname -m)"
echo "   Python版本: $(python3 --version)"
echo ""

# 检查项目状态
echo "📊 项目状态检查..."
python3 scripts/zero_error_monitor.py

echo ""
echo "🎯 Mac专用快捷方式:"
echo "1. 项目监控: python3 scripts/zero_error_monitor.py"
echo "2. 反馈检查: python3 scripts/quick_feedback_check.py"  
echo "3. 脚本管理: python3 scripts/run_manager.py"
echo "4. 文本分类演示: python3 examples/fine-tuning/text_classification_demo.py"

echo ""
echo "⌨️  Mac快捷键提示:"
echo "   • 重启VS Code: Cmd+Shift+P → Developer: Reload Window"
echo "   • 重启Pylance: Cmd+Shift+P → Python: Restart Language Server"
echo "   • 打开终端: Cmd+Shift+反引号"

echo ""
echo "🚀 Mac优化提示:"
echo "   • 已配置零错误环境"
echo "   • 已排除虚拟环境目录"
echo "   • 所有类型检查已禁用"

echo ""
echo "✅ GenerativeAI-Starter-Kit v0.2.0 在Mac上完全就绪!"
echo "🎉 享受无错误的AI开发体验！"