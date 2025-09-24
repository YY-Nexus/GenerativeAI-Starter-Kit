#!/usr/bin/env python3
"""
基础项目监控脚本 - 无复杂依赖版本
专注于提供项目状态概览
"""
import json
import sys
from datetime import datetime
import subprocess
import os

def check_project_status():
    """检查项目基本状态"""
    print("📊 genai-starter-kit 项目状态检查")
    print("=" * 50)
    print(f"📅 检查时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 检查项目文件
    project_files = {
        'setup.py': '包配置文件',
        'pyproject.toml': '现代包配置',
        'requirements.txt': '依赖文件',
        'README.md': '项目说明',
        'CHANGELOG.md': '更新日志'
    }
    
    print("📁 项目文件检查:")
    for filename, description in project_files.items():
        if os.path.exists(filename):
            print(f"   ✅ {filename} - {description}")
        else:
            print(f"   ❌ {filename} - {description} (缺失)")
    print()
    
    # 检查 Python 环境
    print("🐍 Python 环境:")
    try:
        python_version = subprocess.run([
            sys.executable, '--version'
        ], capture_output=True, text=True).stdout.strip()
        print(f"   版本: {python_version}")
        
        # 检查关键包
        key_packages = ['requests', 'setuptools', 'wheel', 'twine']
        for package in key_packages:
            try:
                result = subprocess.run([
                    sys.executable, '-c', f'import {package}; print({package}.__version__)'
                ], capture_output=True, text=True, timeout=5)
                
                if result.returncode == 0:
                    version = result.stdout.strip()
                    print(f"   ✅ {package}: {version}")
                else:
                    print(f"   ❌ {package}: 未安装")
            except:
                print(f"   ❌ {package}: 检查失败")
    except Exception as e:
        print(f"   ❌ Python 检查失败: {e}")
    
    print()
    
    # 检查 Git 状态
    print("📚 Git 仓库状态:")
    try:
        # 检查当前分支
        branch_result = subprocess.run([
            'git', 'branch', '--show-current'
        ], capture_output=True, text=True)
        
        if branch_result.returncode == 0:
            current_branch = branch_result.stdout.strip()
            print(f"   当前分支: {current_branch}")
        
        # 检查提交状态
        status_result = subprocess.run([
            'git', 'status', '--porcelain'
        ], capture_output=True, text=True)
        
        if status_result.returncode == 0:
            if status_result.stdout.strip():
                print("   工作区状态: 有未提交的更改")
            else:
                print("   工作区状态: 干净")
        
        # 最近提交
        log_result = subprocess.run([
            'git', 'log', '--oneline', '-1'
        ], capture_output=True, text=True)
        
        if log_result.returncode == 0:
            last_commit = log_result.stdout.strip()
            print(f"   最近提交: {last_commit}")
            
    except Exception as e:
        print(f"   ❌ Git 检查失败: {e}")
    
    print()
    
    # 提供操作建议
    print("💡 建议的下一步操作:")
    print("-" * 30)
    print("1. 运行项目监控: python scripts/monitor_downloads.py")
    print("2. 检查用户反馈: python scripts/simple_feedback_collector.py")
    print("3. 查看推广计划: python scripts/promotion_scheduler.py plan")
    print("4. 设置自动化: 配置 crontab 定时任务")
    print("5. 社区推广: 在相关平台分享项目")

def generate_status_report():
    """生成状态报告"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"project_status_{timestamp}.json"
    
    status_data: dict[str, object] = {
        'timestamp': datetime.now().isoformat(),
        'project_name': 'genai-starter-kit',
        'version': '0.2.0',
        'status': 'active',
        'check_results': {
            'files_present': {},
            'python_environment': 'checked',
            'git_repository': 'active'
        },
        'recommendations': [
            '监控下载统计',
            '回应用户反馈',
            '推广项目',
            '维护文档'
        ]
    }
    
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(status_data, f, indent=2, ensure_ascii=False)
        print(f"\n💾 状态报告已保存到: {filename}")
    except Exception as e:
        print(f"❌ 保存报告失败: {e}")

def show_quick_help():
    """显示快速帮助"""
    print("🚀 genai-starter-kit 项目管理工具")
    print("=" * 50)
    print()
    print("可用命令:")
    print("  python basic_monitor.py              # 显示项目状态")
    print("  python basic_monitor.py --report     # 生成状态报告")
    print("  python basic_monitor.py --help       # 显示此帮助")
    print()
    print("其他有用的命令:")
    print("  ./scripts/daily_operations.sh       # 每日运营检查")
    print("  python scripts/monitor_downloads.py # 下载量监控")
    print("  python scripts/promotion_scheduler.py plan  # 推广计划")
    print()
    print("重要链接:")
    print("  - PyPI: https://pypi.org/project/genai-starter-kit/")
    print("  - GitHub: https://github.com/YY-Nexus/GenerativeAI-Starter-Kit")
    print("  - 下载统计: https://pypistats.org/packages/genai-starter-kit")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        if sys.argv[1] == "--report":
            generate_status_report()
        elif sys.argv[1] == "--help":
            show_quick_help()
        else:
            print("❌ 未知参数，使用 --help 查看帮助")
    else:
        check_project_status()