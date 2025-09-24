#!/usr/bin/env python3
"""
超简化反馈监控 - 零类型错误版本
"""

import os


def main():
    print("📊 GenerativeAI-Starter-Kit 项目状态")
    print("=" * 50)

    # 基本文件检查
    files_to_check = [
        "README.md",
        "setup.py",
        "requirements.txt",
        "scripts/",
        "examples/",
        "RAG/",
    ]

    print("📁 项目文件:")
    file_count = 0
    for f in files_to_check:
        if os.path.exists(f):
            print(f"   ✅ {f}")
            file_count = file_count + 1
        else:
            print(f"   ❌ {f}")

    # 社区文件检查
    community_files = [
        ".github/ISSUE_TEMPLATE/",
        "CONTRIBUTING.md",
        "CODE_OF_CONDUCT.md",
    ]

    print("\n🔧 社区文件:")
    community_count = 0
    for f in community_files:
        if os.path.exists(f):
            print(f"   ✅ {f}")
            community_count = community_count + 1
        else:
            print(f"   ⚠️  {f}")

    # 简单建议
    print("\n💡 建议:")
    if file_count == len(files_to_check):
        print("   • 项目文件完整 ✅")
    else:
        print("   • 补齐缺失的项目文件")

    if community_count >= 2:
        print("   • 社区配置良好 ✅")
    else:
        print("   • 建议完善社区文件")

    print("   • 定期检查用户反馈")
    print("   • 关注 GitHub issues")
    print("   • 感谢贡献者")

    print("\n✅ 状态检查完成")


if __name__ == "__main__":
    main()
