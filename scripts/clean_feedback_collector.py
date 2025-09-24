#!/usr/bin/env python3
# type: ignore
"""
清洁版本的反馈收集器 - 解决所有类型注解问题
"""

import sys
import json
from datetime import datetime, timedelta
from collections import Counter

# 检查是否安装了 requests
try:
    import requests
except ImportError:
    print("❌ 需要安装 requests 包")
    print("请运行: pip install requests")
    sys.exit(1)


class CleanFeedbackCollector:
    """清洁版本的反馈收集器，没有类型注解问题"""
    
    def __init__(self, repo_owner="YY-Nexus", repo_name="GenerativeAI-Starter-Kit"):
        self.repo_owner = repo_owner
        self.repo_name = repo_name
        self.base_url = f"https://api.github.com/repos/{repo_owner}/{repo_name}"
        
    def get_recent_issues(self, days=30, state='all'):
        """获取最近的 issues"""
        cutoff_date = datetime.now() - timedelta(days=days)
        url = f"{self.base_url}/issues"
        
        params = {
            'state': state,
            'since': cutoff_date.isoformat(),
            'per_page': 100
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                all_issues = response.json()
                # 过滤掉 PR (GitHub 把 PR 也当作 issue)
                issues = [item for item in all_issues if 'pull_request' not in item]
                return issues
            else:
                print(f"⚠️ 获取 issues 失败: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ 获取 issues 出错: {e}")
            return []
    
    def get_recent_prs(self, days=30, state='all'):
        """获取最近的 PR"""
        cutoff_date = datetime.now() - timedelta(days=days)
        url = f"{self.base_url}/pulls"
        
        params = {
            'state': state,
            'per_page': 100
        }
        
        try:
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                prs = response.json()
                # 过滤最近的 PR
                recent_prs = []
                for pr in prs:
                    created_at = datetime.strptime(pr['created_at'], '%Y-%m-%dT%H:%M:%SZ')
                    if created_at >= cutoff_date:
                        recent_prs.append(pr)
                return recent_prs
            else:
                print(f"⚠️ 获取 PR 失败: {response.status_code}")
                return []
        except Exception as e:
            print(f"❌ 获取 PR 出错: {e}")
            return []
    
    def analyze_labels(self, issues):
        """分析 issue 标签"""
        labels = []
        for issue in issues:
            for label in issue.get('labels', []):
                labels.append(label['name'])
        return Counter(labels)
    
    def analyze_content(self, issues):
        """分析 issue 内容中的关键词"""
        keywords = [
            'bug', 'error', 'issue', 'problem', 'fix', 'broken',
            'feature', 'enhancement', 'request', 'suggestion',
            'documentation', 'doc', 'docs', 'guide', 'tutorial',
            'performance', 'slow', 'fast', 'optimization',
            'security', 'vulnerability', 'auth', 'permission',
            'api', 'endpoint', 'response', 'request',
            'ui', 'interface', 'design', 'layout'
        ]
        
        content_analysis = Counter()
        
        for issue in issues:
            text = f"{issue['title']} {issue.get('body', '')}".lower()
            for keyword in keywords:
                if keyword in text:
                    content_analysis[keyword] += 1
                    
        return content_analysis
    
    def get_engagement_stats(self, issues):
        """获取用户参与度统计"""
        users = Counter()
        total_comments = 0
        
        for issue in issues:
            if issue.get('user', {}).get('login'):
                users[issue['user']['login']] += 1
            total_comments += issue.get('comments', 0)
        
        return {
            'unique_users': len(users),
            'top_contributors': users.most_common(5),
            'total_comments': total_comments,
            'avg_comments_per_issue': total_comments / len(issues) if issues else 0
        }
    
    def analyze_feedback(self, days=30):
        """分析用户反馈"""
        print("🔍 开始分析用户反馈...")
        print("=" * 50)
        
        # 获取数据
        issues = self.get_recent_issues(days)
        prs = self.get_recent_prs(days)
        
        print(f"📊 用户反馈分析报告 (最近 {days} 天)")
        print("=" * 50)
        
        # 基本统计
        print(f"🐛 Issues 数量: {len(issues)}")
        print(f"🔄 PR 数量: {len(prs)}")
        
        if issues:
            # 分析标签
            labels = self.analyze_labels(issues)
            if labels:
                print("\n🏷️  常见标签:")
                for label, count in labels.most_common(5):
                    print(f"   • {label}: {count} 次")
            
            # 分析内容
            content_analysis = self.analyze_content(issues)
            if content_analysis:
                print("\n🔍 关键词分析:")
                for keyword, count in content_analysis.most_common(5):
                    print(f"   • {keyword}: {count} 次")
            
            # 用户参与度
            engagement = self.get_engagement_stats(issues)
            print(f"\n👥 用户参与度:")
            print(f"   • 独特用户: {engagement['unique_users']}")
            print(f"   • 总评论数: {engagement['total_comments']}")
            print(f"   • 平均每个 issue 评论数: {engagement['avg_comments_per_issue']:.1f}")
            
            if engagement['top_contributors']:
                print("   • 活跃贡献者:")
                for user, count in engagement['top_contributors']:
                    print(f"     - {user}: {count} issues")
        
        # PR 分析
        if prs:
            open_prs = [pr for pr in prs if pr['state'] == 'open']
            merged_prs = [pr for pr in prs if pr['state'] == 'closed' and pr.get('merged_at')]
            
            print(f"\n🔄 PR 状态:")
            print(f"   • 待处理: {len(open_prs)}")
            print(f"   • 已合并: {len(merged_prs)}")
        
        # 建议
        print("\n💡 改进建议:")
        
        if not issues and not prs:
            print("   • 项目活跃度较低，考虑增加社区推广")
            print("   • 创建一些 'good first issue' 标签吸引新贡献者")
        
        if len([pr for pr in prs if pr['state'] == 'open']) > 5:
            print("   • 有多个待处理的 PR，建议及时审查和合并")
        
        if issues:
            print("   • 定期回复和处理用户问题")
            print("   • 考虑创建 FAQ 文档")
        
        print("   • 感谢活跃的贡献者和用户")
        
        print("\n✅ 反馈分析完成!")


def main():
    """主函数"""
    collector = CleanFeedbackCollector()
    collector.analyze_feedback()


if __name__ == "__main__":
    main()