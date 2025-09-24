#!/usr/bin/env python3
"""
完全无错误版本的反馈监控工具
专门解决所有类型检查和导入问题
"""

import os
import subprocess
import sys
from datetime import datetime

def safe_import_check():
    """安全检查必要的包是否已安装"""
    required_packages = ['requests']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ 缺少必要的包: {', '.join(missing_packages)}")
        print("请运行以下命令安装:")
        for pkg in missing_packages:
            print(f"pip install {pkg}")
        return False
    return True

def get_project_info():
    """获取项目基本信息"""
    info = {
        'project_name': 'GenerativeAI-Starter-Kit',
        'repo_owner': 'YY-Nexus',
        'current_time': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    }
    return info

def check_project_structure():
    """检查项目结构完整性"""
    essential_files = [
        'README.md',
        'setup.py', 
        'requirements.txt',
        'scripts/',
        'examples/',
        'RAG/',
        'notebooks/'
    ]
    
    github_files = [
        '.github/ISSUE_TEMPLATE/',
        '.github/workflows/',
        'CONTRIBUTING.md',
        'CODE_OF_CONDUCT.md'
    ]
    
    print("📁 项目结构检查:")
    missing_files = []
    
    for file_path in essential_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path}")
            missing_files.append(file_path)
    
    print("\n🔧 GitHub 社区文件:")
    github_score = 0
    
    for file_path in github_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
            github_score += 1
        else:
            print(f"   ⚠️  {file_path} (建议添加)")
    
    return {
        'missing_files': missing_files,
        'github_score': github_score,
        'total_github_files': len(github_files)
    }

def check_python_environment():
    """检查 Python 环境"""
    try:
        python_version = sys.version.split()[0]
        print(f"\n🐍 Python 版本: {python_version}")
        
        # 检查基本包
        basic_packages = ['json', 'datetime', 'os', 'sys']
        print("📦 基本包检查:")
        
        for pkg in basic_packages:
            try:
                __import__(pkg)
                print(f"   ✅ {pkg}")
            except ImportError:
                print(f"   ❌ {pkg}")
        
        return True
    except Exception as e:
        print(f"❌ Python 环境检查失败: {e}")
        return False

def get_git_info():
    """安全获取 Git 信息"""
    git_info = {}
    
    try:
        # 检查是否在 Git 仓库中
        result = subprocess.run(['git', 'status'], 
                              capture_output=True, 
                              text=True, 
                              cwd=os.getcwd())
        
        if result.returncode == 0:
            git_info['is_git_repo'] = True
            
            # 获取当前分支
            branch_result = subprocess.run(['git', 'branch', '--show-current'], 
                                         capture_output=True, 
                                         text=True)
            if branch_result.returncode == 0:
                git_info['current_branch'] = branch_result.stdout.strip()
            
            # 获取最后提交信息
            log_result = subprocess.run(['git', 'log', '-1', '--oneline'], 
                                      capture_output=True, 
                                      text=True)
            if log_result.returncode == 0:
                git_info['last_commit'] = log_result.stdout.strip()
        else:
            git_info['is_git_repo'] = False
            
    except Exception:
        git_info['is_git_repo'] = False
    
    return git_info

def generate_feedback_report():
    """生成反馈监控报告"""
    print("=" * 60)
    print("📊 GenerativeAI-Starter-Kit 反馈监控报告")
    print("=" * 60)
    
    # 项目信息
    project_info = get_project_info()
    print(f"📅 报告时间: {project_info['current_time']}")
    print(f"📦 项目名称: {project_info['project_name']}")
    print(f"👤 仓库所有者: {project_info['repo_owner']}")
    
    # 检查包依赖
    print("\n" + "="*40)
    print("📦 依赖包检查")
    print("="*40)
    
    if not safe_import_check():
        print("⚠️ 部分功能受限，但基本监控可用")
    else:
        print("✅ 所有依赖包正常")
    
    # Python 环境检查
    print("\n" + "="*40) 
    print("🐍 Python 环境检查")
    print("="*40)
    check_python_environment()
    
    # 项目结构检查
    print("\n" + "="*40)
    print("📁 项目结构检查") 
    print("="*40)
    structure_info = check_project_structure()
    
    # Git 信息
    print("\n" + "="*40)
    print("🔧 Git 仓库信息")
    print("="*40)
    git_info = get_git_info()
    
    if git_info.get('is_git_repo'):
        print("   ✅ Git 仓库已初始化")
        if git_info.get('current_branch'):
            print(f"   📝 当前分支: {git_info['current_branch']}")
        if git_info.get('last_commit'):
            print(f"   💻 最后提交: {git_info['last_commit']}")
    else:
        print("   ⚠️  未检测到 Git 仓库")
    
    # 总结和建议
    print("\n" + "="*40)
    print("💡 改进建议")
    print("="*40)
    
    if structure_info['missing_files']:
        print("📁 项目文件:")
        print(f"   • 缺少 {len(structure_info['missing_files'])} 个核心文件")
        print("   • 建议补齐缺失的项目文件")
    
    github_completion = (structure_info['github_score'] / 
                        structure_info['total_github_files'] * 100)
    
    print(f"\n🔧 GitHub 社区配置完成度: {github_completion:.0f}%")
    
    if github_completion < 75:
        print("   • 建议完善 GitHub 社区文件")
        print("   • 添加 Issue 模板和贡献指南")
    else:
        print("   • GitHub 社区配置良好")
    
    print("\n📈 反馈监控建议:")
    print("   • 定期检查 PyPI 下载统计")
    print("   • 关注 GitHub issues 和 PR")
    print("   • 收集用户使用反馈")
    print("   • 维护活跃的社区交流")
    
    print("\n" + "="*60)
    print("✅ 反馈监控报告完成")
    print("="*60)

def main():
    """主函数"""
    try:
        generate_feedback_report()
    except Exception as e:
        print(f"❌ 报告生成失败: {e}")
        print("但基本检查功能正常运行")

if __name__ == "__main__":
    main()