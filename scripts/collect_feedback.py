#!/usr/bin/env python3
# type: ignore
"""
用户反馈收集和分析工具
分析 GitHub issues, discussions 等用户反馈
"""
import requests
import json
from datetime import datetime, timedelta
from collections import Counter
import sys


class FeedbackCollector:
    def __init__(self, repo_owner="YY-Nexus", repo_name="GenerativeAI-Starter-Kit"):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"

    def get_recent_issues(self, days=30, state="all"):
        """获取最近的 issues"""
        since_date = (datetime.now() - timedelta(days=days)).isoformat()
        url = f"{self.base_url}/issues"
        params = {
            "since": since_date,
            "state": state,
            "sort": "created",
            "direction": "desc",
            "per_page": 100,
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                issues = response.json()
                # 过滤掉 pull requests
                return [issue for issue in issues if "pull_request" not in issue]
            else:
                print(f"❌ GitHub API 返回状态码: {response.status_code}")
        except Exception as e:
            print(f"❌ 获取 issues 失败: {e}")

        return []

    def get_recent_prs(self, days=30, state="all"):
        """获取最近的 Pull Requests"""
        since_date = (datetime.now() - timedelta(days=days)).isoformat()
        url = f"{self.base_url}/pulls"
        params = {
            "state": state,
            "sort": "created",
            "direction": "desc",
            "per_page": 50,
        }

        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                prs = response.json()
                # 过滤最近创建的
                recent_prs = []
                for pr in prs:
                    created_at = datetime.fromisoformat(
                        pr["created_at"].replace("Z", "+00:00")
                    )
                    if created_at >= datetime.now(created_at.tzinfo) - timedelta(
                        days=days
                    ):
                        recent_prs.append(pr)
                return recent_prs
        except Exception as e:
            print(f"❌ 获取 PRs 失败: {e}")

        return []

    def analyze_issue_labels(self, issues):
        """分析 issue 标签分布"""
        labels = []
        for issue in issues:
            for label in issue.get("labels", []):
                labels.append(label["name"])

        return Counter(labels)

    def analyze_issue_content(self, issues):
        """分析 issue 内容，识别常见问题"""
        keywords = {
            "bug": ["bug", "error", "issue", "problem", "fail", "错误", "问题", "故障"],
            "feature": ["feature", "enhancement", "request", "功能", "增强", "请求"],
            "docs": [
                "documentation",
                "readme",
                "example",
                "tutorial",
                "文档",
                "示例",
                "教程",
            ],
            "performance": ["slow", "fast", "performance", "speed", "性能", "速度", "慢"],
            "installation": [
                "install",
                "setup",
                "dependency",
                "requirements",
                "安装",
                "依赖",
            ],
        }

        content_analysis = Counter()

        for issue in issues:
            text = f"{issue['title']} {issue.get('body', '')}".lower()

            for category, words in keywords.items():
                for word in words:
                    if word in text:
                        content_analysis[category] += 1
                        break  # 每个issue只计算一次该类别

        return content_analysis

    def get_user_engagement(self, issues):
        """分析用户参与度"""
        users = Counter()
        total_comments = 0

        for issue in issues:
            # 统计创建者
            users[issue["user"]["login"]] += 1
            # 统计评论数
            total_comments += issue.get("comments", 0)

        return {
            "unique_users": len(users),
            "top_contributors": users.most_common(5),
            "total_comments": total_comments,
            "avg_comments_per_issue": total_comments / len(issues) if issues else 0,
        }

    def analyze_feedback(self, days=30):
        """综合分析用户反馈"""
        print(f"📊 用户反馈分析报告 (最近 {days} 天)")
        print("=" * 60)
        print(f"📅 分析时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print()

        # 获取数据
        issues = self.get_recent_issues(days)
        prs = self.get_recent_prs(days)
        content_analysis = Counter()  # 初始化 content_analysis

        if not issues and not prs:
            print("📭 最近没有新的反馈或贡献")
            print()
            print("💡 建议:")
            print("- 主动在社区中推广项目")
            print("- 完善文档和示例")
            print("- 回应现有的 issues")
            self.provide_recommendations(issues, prs, content_analysis)
            return

        print(f"📝 Issues 数量: {len(issues)}")
        print(f"🔄 Pull Requests 数量: {len(prs)}")
        print()

        if issues:
            # 标签分析
            label_counts = self.analyze_issue_labels(issues)
            if label_counts:
                print("🏷️  Issue 标签分布:")
                for label, count in label_counts.most_common():
                    print(f"   {label}: {count}")
                print()

            # 内容分析
            content_analysis = self.analyze_issue_content(issues)
            if content_analysis:
                print("🔍 问题类型分析:")
                for category, count in content_analysis.most_common():
                    print(f"   {category}: {count} 个相关 issues")
                print()

            # 用户参与分析
            engagement = self.get_user_engagement(issues)
            print("👥 用户参与度:")
            print(f"   独立用户数: {engagement['unique_users']}")
            print(f"   总评论数: {engagement['total_comments']}")
            print(f"   平均每个issue评论数: {engagement['avg_comments_per_issue']:.1f}")

            if engagement["top_contributors"]:
                print("   活跃贡献者:")
                for user, count in engagement["top_contributors"]:
                    print(f"     {user}: {count} issues")
            print()

        # 最新反馈
        print("🔥 最新 Issues:")
        if issues:
            for issue in issues[:5]:
                status_emoji = "✅" if issue["state"] == "closed" else "🔴"
                print(f"   {status_emoji} #{issue['number']}: {issue['title']}")
                print(
                    f"      👤 {issue['user']['login']} | 📅 {issue['created_at'][:10]} | 💬 {issue.get('comments', 0)}"
                )
        else:
            print("   暂无最近的 Issues")

        if prs:
            print()
            print("🔄 最新 Pull Requests:")
            for pr in prs[:3]:
                status_emoji = "✅" if pr["state"] == "closed" else "🔴"
                merged_emoji = "🔀" if pr.get("merged_at") else ""
                print(f"   {status_emoji}{merged_emoji} #{pr['number']}: {pr['title']}")
                print(f"      👤 {pr['user']['login']} | 📅 {pr['created_at'][:10]}")

        print()
        self.provide_recommendations(issues, prs, content_analysis)

    def provide_recommendations(self, issues, prs, content_analysis):
        """基于分析结果提供建议"""
        print("💡 行动建议:")
        print("-" * 30)

        if not issues and not prs:
            print("- 项目可能需要更多推广来吸引用户")
            print("- 考虑在相关社区分享项目")
            return

        # 基于问题类型提供建议
        if content_analysis:
            top_issue = content_analysis.most_common(1)[0] if content_analysis else None

            if top_issue:
                category, count = top_issue
                if category == "bug":
                    print(f"- 优先修复 bug ({count} 个相关issues)")
                    print("- 考虑增加自动化测试")
                elif category == "feature":
                    print(f"- 评估功能请求的优先级 ({count} 个请求)")
                    print("- 创建功能路线图")
                elif category == "docs":
                    print(f"- 完善文档和示例 ({count} 个相关issues)")
                    print("- 增加更多使用教程")
                elif category == "installation":
                    print(f"- 简化安装过程 ({count} 个安装问题)")
                    print("- 更新安装文档")

        # 通用建议
        open_issues = [i for i in issues if i["state"] == "open"]
        if open_issues:
            print(f"- 及时回应 {len(open_issues)} 个开放的 issues")

        recent_prs = [p for p in prs if p["state"] == "open"]
        if recent_prs:
            print(f"- 审查和合并 {len(recent_prs)} 个待处理的 PR")

        print("- 定期感谢贡献者和用户")
        print("- 考虑创建 CONTRIBUTING.md 指南")

    def export_feedback_summary(self, filename=None):
        """导出反馈摘要到文件"""
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"feedback_analysis_{timestamp}.json"

        issues = self.get_recent_issues(30)
        prs = self.get_recent_prs(30)

        summary = {
            "timestamp": datetime.now().isoformat(),
            "analysis_period_days": 30,
            "issues_count": len(issues),
            "prs_count": len(prs),
            "label_distribution": dict(self.analyze_issue_labels(issues)),
            "content_analysis": dict(self.analyze_issue_content(issues)),
            "user_engagement": self.get_user_engagement(issues) if issues else {},
            "recent_issues": [
                {
                    "number": issue["number"],
                    "title": issue["title"],
                    "state": issue["state"],
                    "user": issue["user"]["login"],
                    "created_at": issue["created_at"],
                    "comments": issue.get("comments", 0),
                }
                for issue in issues[:10]
            ],
        }

        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(summary, f, indent=2, ensure_ascii=False)
            print(f"💾 反馈分析已保存到: {filename}")
        except Exception as e:
            print(f"❌ 保存失败: {e}")


if __name__ == "__main__":
    collector = FeedbackCollector()

    if len(sys.argv) > 1:
        if sys.argv[1] == "--export":
            collector.export_feedback_summary()
        elif sys.argv[1] == "--days" and len(sys.argv) > 2:
            try:
                days = int(sys.argv[2])
                collector.analyze_feedback(days)
            except ValueError:
                print("❌ 天数必须是整数")
        else:
            print("用法:")
            print("  python collect_feedback.py              # 默认分析最近30天")
            print("  python collect_feedback.py --days 7     # 分析最近7天")
            print("  python collect_feedback.py --export     # 导出分析结果")
    else:
        collector.analyze_feedback()
