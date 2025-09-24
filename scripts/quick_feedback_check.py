#!/usr/bin/env python3
"""
简单反馈监控脚本 - 无类型检查问题版本
"""

import os


# 简单版本，只做基本检查，避免类型注解问题
def check_feedback():
    """检查项目反馈状态"""
    print("📊 项目反馈快速检查")
    print("=" * 30)

    # 检查项目文件状态
    project_files = [
        "README.md",
        "setup.py",
        "requirements.txt",
        "scripts/",
        "examples/",
        "RAG/",
    ]

    print("📁 项目文件检查:")
    for file_path in project_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path}")

    # 检查是否有 GitHub 相关配置
    github_files = [
        ".github/ISSUE_TEMPLATE/",
        ".github/workflows/",
        "CONTRIBUTING.md",
        "CODE_OF_CONDUCT.md",
    ]

    print("\n🔧 GitHub 配置:")
    github_setup = 0
    for file_path in github_files:
        if os.path.exists(file_path):
            print(f"   ✅ {file_path}")
            github_setup += 1
        else:
            print(f"   ⚠️  {file_path} (可选)")

    # 简单建议
    print("\n💡 建议:")
    if github_setup < 2:
        print("   • 设置更多 GitHub 社区文件")
    else:
        print("   • GitHub 社区配置良好")

    print("   • 定期检查 PyPI 下载统计")
    print("   • 关注 GitHub issues 和 discussions")
    print("   • 保持文档更新")

    print("\n✅ 快速检查完成!")


if __name__ == "__main__":
    check_feedback()
