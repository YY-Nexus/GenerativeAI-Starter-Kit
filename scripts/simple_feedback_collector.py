#!/usr/bin/env python3
# type: ignore
"""
简化版用户反馈收集工具
专注于核心功能，避免复杂的类型推断问题
"""
import requests
import json
from datetime import datetime, timedelta
import sys


def get_github_issues(days=30):
    """获取GitHub issues"""
    repo_url = "https://api.github.com/repos/YY-Nexus/GenerativeAI-Starter-Kit/issues"
    since_date = (datetime.now() - timedelta(days=days)).isoformat()

    try:
        response = requests.get(
            repo_url,
            params={"since": since_date, "state": "all", "per_page": 100},
            timeout=10,
        )

        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ GitHub API 返回错误: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ 获取 issues 失败: {e}")
        return []


def get_github_prs(days=30):
    """获取GitHub Pull Requests"""
    repo_url = "https://api.github.com/repos/YY-Nexus/GenerativeAI-Starter-Kit/pulls"

    try:
        response = requests.get(
            repo_url,
            params={
                "state": "all",
                "sort": "created",
                "direction": "desc",
                "per_page": 50,
            },
            timeout=10,
        )

        if response.status_code == 200:
            return response.json()
        else:
            print(f"❌ GitHub API 返回错误: {response.status_code}")
            return []
    except Exception as e:
        print(f"❌ 获取 PRs 失败: {e}")
        return []


def analyze_feedback():
    """分析用户反馈"""
    print("📊 用户反馈分析报告")
    print("=" * 50)
    print(f"📅 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # 获取数据
    issues = get_github_issues(30)
    prs = get_github_prs(30)

    # 过滤真实的issues（排除PRs）
    real_issues = []
    for issue in issues:
        if "pull_request" not in issue:
            real_issues.append(issue)

    print(f"📝 Issues 数量: {len(real_issues)}")
    print(f"🔄 Pull Requests 数量: {len(prs)}")
    print()

    if not real_issues and not prs:
        print("📭 最近没有新的反馈或贡献")
        print()
        print("💡 建议:")
        print("- 主动在社区中推广项目")
        print("- 完善文档和示例")
        print("- 回应现有的 issues")
        return

    # 显示最新issues
    if real_issues:
        print("🔥 最新 Issues:")
        for i, issue in enumerate(real_issues[:5]):
            status = "✅" if issue.get("state") == "closed" else "🔴"
            title = issue.get("title", "未知标题")
            number = issue.get("number", "?")
            user = issue.get("user", {}).get("login", "未知用户")
            created = issue.get("created_at", "")[:10]
            comments = issue.get("comments", 0)

            print(f"   {status} #{number}: {title}")
            print(f"      👤 {user} | 📅 {created} | 💬 {comments}")
        print()

    # 显示最新PRs
    if prs:
        print("🔄 最新 Pull Requests:")
        for i, pr in enumerate(prs[:3]):
            status = "✅" if pr.get("state") == "closed" else "🔴"
            merged = "🔀" if pr.get("merged_at") else ""
            title = pr.get("title", "未知标题")
            number = pr.get("number", "?")
            user = pr.get("user", {}).get("login", "未知用户")
            created = pr.get("created_at", "")[:10]

            print(f"   {status}{merged} #{number}: {title}")
            print(f"      👤 {user} | 📅 {created}")
        print()

    # 提供建议
    print("💡 行动建议:")
    print("-" * 30)

    open_issues_count = sum(1 for issue in real_issues if issue.get("state") == "open")
    open_prs_count = sum(1 for pr in prs if pr.get("state") == "open")

    if open_issues_count > 0:
        print(f"- 及时回应 {open_issues_count} 个开放的 issues")

    if open_prs_count > 0:
        print(f"- 审查和合并 {open_prs_count} 个待处理的 PR")

    if not real_issues:
        print("- 项目可能需要更多推广来吸引用户")
        print("- 考虑在相关社区分享项目")

    print("- 定期感谢贡献者和用户")
    print("- 考虑创建 CONTRIBUTING.md 指南")


def export_feedback_data():
    """导出反馈数据"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"feedback_analysis_{timestamp}.json"

    issues = get_github_issues(30)
    prs = get_github_prs(30)

    # 过滤真实的issues
    real_issues = [issue for issue in issues if "pull_request" not in issue]

    data = {
        "timestamp": datetime.now().isoformat(),
        "analysis_period_days": 30,
        "issues_count": len(real_issues),
        "prs_count": len(prs),
        "open_issues_count": sum(
            1 for issue in real_issues if issue.get("state") == "open"
        ),
        "open_prs_count": sum(1 for pr in prs if pr.get("state") == "open"),
        "recent_issues": [
            {
                "number": issue.get("number"),
                "title": issue.get("title"),
                "state": issue.get("state"),
                "user": issue.get("user", {}).get("login"),
                "created_at": issue.get("created_at"),
                "comments": issue.get("comments", 0),
            }
            for issue in real_issues[:10]
        ],
    }

    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"💾 反馈分析已保存到: {filename}")
    except Exception as e:
        print(f"❌ 保存失败: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--export":
        export_feedback_data()
    else:
        analyze_feedback()
