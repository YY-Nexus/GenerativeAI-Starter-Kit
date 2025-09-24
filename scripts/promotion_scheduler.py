#!/usr/bin/env python3
"""
推广活动调度器
制定和管理社区推广计划
"""
from datetime import datetime, timedelta
import calendar
import json


class PromotionScheduler:
    def __init__(self):
        self.platforms = {
            "reddit": {
                "days": ["周一", "周四"],
                "subreddits": [
                    "r/MachineLearning",
                    "r/Python",
                    "r/ArtificialIntelligence",
                ],
                "content_types": ["技术分享", "案例研究", "教程"],
            },
            "zhihu": {
                "days": ["周二", "周五"],
                "topics": ["机器学习", "Python开发", "人工智能"],
                "content_types": ["技术文章", "经验分享", "Q&A回答"],
            },
            "juejin": {
                "days": ["周三", "周六"],
                "categories": ["人工智能", "Python", "开源项目"],
                "content_types": ["技术博客", "项目介绍", "开发心得"],
            },
            "twitter": {"days": ["每日"], "content_types": ["技术小贴士", "更新公告", "用户案例"]},
            "github": {"days": ["周日"], "activities": ["README更新", "文档完善", "Issues回复"]},
        }

        self.content_calendar = {
            "技术介绍": "每月第1周",
            "教程系列": "每月第2周",
            "案例分享": "每月第3周",
            "社区互动": "每月第4周",
        }

    def get_chinese_weekday(self, english_day):
        """转换英文星期到中文"""
        mapping = {
            "Monday": "周一",
            "Tuesday": "周二",
            "Wednesday": "周三",
            "Thursday": "周四",
            "Friday": "周五",
            "Saturday": "周六",
            "Sunday": "周日",
        }
        return mapping.get(english_day, english_day)

    def get_daily_activities(self, weekday):
        """获取指定星期的推广活动"""
        activities = []
        for platform, config in self.platforms.items():
            if weekday in config["days"] or "每日" in config["days"]:
                activities.append(f"{platform} 内容发布")
        return activities

    def generate_monthly_plan(self, year=None, month=None):
        """生成月度推广计划"""
        if not year or not month:
            today = datetime.now()
            year, month = today.year, today.month

        print(f"📅 {year}年{month}月推广计划")
        print("=" * 50)

        # 获取该月的所有日期
        cal = calendar.monthcalendar(year, month)
        week_num = 1

        for week in cal:
            print(f"\n📍 第{week_num}周:")
            week_num += 1

            for day in week:
                if day == 0:  # 空日期
                    continue

                date = datetime(year, month, day)
                weekday = date.strftime("%A")
                weekday_zh = self.get_chinese_weekday(weekday)

                activities = self.get_daily_activities(weekday_zh)
                if activities:
                    print(
                        f"  {month}/{day:02d} ({weekday_zh}): {', '.join(activities)}"
                    )

        # 周度内容主题
        print("\n🎯 本月内容主题规划:")
        for week_num, (theme, timing) in enumerate(self.content_calendar.items(), 1):
            print(f"  第{week_num}周: {theme} ({timing})")

        print(f"\n📊 统计:")
        total_posts = self._calculate_monthly_posts(year, month)
        print(f"  预计发布内容: {total_posts} 条")
        print(f"  覆盖平台: {len(self.platforms)} 个")

    def _calculate_monthly_posts(self, year, month):
        """计算月度发布内容总数"""
        cal = calendar.monthcalendar(year, month)
        total_posts = 0

        for week in cal:
            for day in week:
                if day == 0:
                    continue

                date = datetime(year, month, day)
                weekday_zh = self.get_chinese_weekday(date.strftime("%A"))
                activities = self.get_daily_activities(weekday_zh)
                total_posts += len(activities)

        return total_posts

    def generate_content_ideas(self):
        """生成内容创意"""
        content_ideas = {
            "reddit": [
                "genai-starter-kit: 简化生成式AI开发的Python工具包",
                "如何用10行代码构建RAG应用",
                "开源AI工具包的设计理念分享",
                "多模态AI应用开发最佳实践",
            ],
            "zhihu": ["从零开始的生成式AI开发指南", "RAG应用的工程化实践", "开源项目维护经验分享", "AI工具包的架构设计思考"],
            "juejin": [
                "genai-starter-kit源码解析",
                "Python包发布到PyPI的完整流程",
                "生成式AI应用的性能优化",
                "开源项目的社区建设",
            ],
            "twitter": [
                "🚀 genai-starter-kit v0.2.0 发布！",
                "💡 每日AI开发小贴士",
                "🔥 用户成功案例分享",
                "📈 项目更新和路线图",
            ],
        }

        print("💡 内容创意库:")
        print("=" * 40)

        for platform, ideas in content_ideas.items():
            print(f"\n📱 {platform.title()}:")
            for i, idea in enumerate(ideas, 1):
                print(f"  {i}. {idea}")

    def track_promotion_metrics(self):
        """追踪推广指标"""
        metrics_template = {
            "date": datetime.now().strftime("%Y-%m-%d"),
            "github": {
                "stars": 0,
                "forks": 0,
                "watchers": 0,
                "new_issues": 0,
                "new_prs": 0,
            },
            "pypi": {
                "downloads_daily": 0,
                "downloads_weekly": 0,
                "downloads_monthly": 0,
            },
            "social_media": {
                "reddit_posts": 0,
                "reddit_upvotes": 0,
                "zhihu_articles": 0,
                "zhihu_views": 0,
                "twitter_posts": 0,
                "twitter_engagement": 0,
            },
            "website": {"page_views": 0, "unique_visitors": 0, "bounce_rate": 0},
        }

        print("📊 推广效果追踪模板:")
        print(json.dumps(metrics_template, indent=2, ensure_ascii=False))

        # 保存模板
        filename = f"promotion_metrics_template.json"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(metrics_template, f, indent=2, ensure_ascii=False)
            print(f"\n💾 指标模板已保存到: {filename}")
        except Exception as e:
            print(f"❌ 保存失败: {e}")

    def generate_weekly_report(self):
        """生成周度推广报告"""
        today = datetime.now()
        week_start = today - timedelta(days=today.weekday())
        week_end = week_start + timedelta(days=6)

        print(
            f"📊 推广周报 ({week_start.strftime('%Y-%m-%d')} - {week_end.strftime('%Y-%m-%d')})"
        )
        print("=" * 60)

        # 本周完成的推广活动
        print("✅ 本周完成的推广活动:")
        for i in range(7):
            day = week_start + timedelta(days=i)
            weekday_zh = self.get_chinese_weekday(day.strftime("%A"))
            activities = self.get_daily_activities(weekday_zh)

            if activities:
                print(
                    f"  {day.strftime('%m-%d')} ({weekday_zh}): {', '.join(activities)}"
                )

        print("\n📈 效果评估 (需要手动填入数据):")
        print("  - GitHub Stars 增长: ___ (+___)")
        print("  - PyPI 下载量: ___ (周环比: ___)")
        print("  - 社交媒体互动: ___ (点赞/评论/分享)")
        print("  - 新用户反馈: ___ 条")

        print("\n💡 下周计划:")
        next_week_start = week_end + timedelta(days=1)
        next_week_end = next_week_start + timedelta(days=6)

        print(
            f"  时间: {next_week_start.strftime('%Y-%m-%d')} - {next_week_end.strftime('%Y-%m-%d')}"
        )

        for i in range(7):
            day = next_week_start + timedelta(days=i)
            weekday_zh = self.get_chinese_weekday(day.strftime("%A"))
            activities = self.get_daily_activities(weekday_zh)

            if activities:
                print(
                    f"  {day.strftime('%m-%d')} ({weekday_zh}): {', '.join(activities)}"
                )

    def create_promotion_checklist(self):
        """创建推广检查清单"""
        checklist = {
            "daily_tasks": [
                "检查GitHub issues和PR",
                "回应社区评论和问题",
                "发布Twitter/微博内容",
                "监控项目统计数据",
            ],
            "weekly_tasks": ["发布技术博客文章", "参与相关社区讨论", "更新项目文档", "分析用户反馈趋势"],
            "monthly_tasks": ["制定下月推广计划", "生成月度数据报告", "评估推广效果", "调整推广策略"],
            "content_preparation": ["准备技术文章草稿", "制作演示视频/图片", "整理用户案例", "更新FAQ文档"],
        }

        print("📋 推广工作检查清单:")
        print("=" * 40)

        for category, tasks in checklist.items():
            print(f"\n{category.replace('_', ' ').title()}:")
            for task in tasks:
                print(f"  ☐ {task}")

        # 保存清单
        filename = "promotion_checklist.json"
        try:
            with open(filename, "w", encoding="utf-8") as f:
                json.dump(checklist, f, indent=2, ensure_ascii=False)
            print(f"\n💾 检查清单已保存到: {filename}")
        except Exception as e:
            print(f"❌ 保存失败: {e}")


def main():
    """主函数"""
    scheduler = PromotionScheduler()

    print("🚀 genai-starter-kit 推广管理系统")
    print("=" * 50)

    while True:
        print("\n请选择操作:")
        print("1. 生成月度推广计划")
        print("2. 查看内容创意库")
        print("3. 生成周度推广报告")
        print("4. 创建推广检查清单")
        print("5. 设置推广指标追踪")
        print("0. 退出")

        choice = input("\n输入选择 (0-5): ").strip()

        if choice == "1":
            year_month = input("请输入年月 (格式: YYYY-MM, 回车使用当前月): ").strip()
            if year_month:
                try:
                    year, month = map(int, year_month.split("-"))
                    scheduler.generate_monthly_plan(year, month)
                except ValueError:
                    print("❌ 格式错误，请使用 YYYY-MM 格式")
            else:
                scheduler.generate_monthly_plan()

        elif choice == "2":
            scheduler.generate_content_ideas()

        elif choice == "3":
            scheduler.generate_weekly_report()

        elif choice == "4":
            scheduler.create_promotion_checklist()

        elif choice == "5":
            scheduler.track_promotion_metrics()

        elif choice == "0":
            print("👋 感谢使用推广管理系统！")
            break

        else:
            print("❌ 无效选择，请重试")


if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        scheduler = PromotionScheduler()

        if sys.argv[1] == "plan":
            scheduler.generate_monthly_plan()
        elif sys.argv[1] == "ideas":
            scheduler.generate_content_ideas()
        elif sys.argv[1] == "report":
            scheduler.generate_weekly_report()
        elif sys.argv[1] == "checklist":
            scheduler.create_promotion_checklist()
        elif sys.argv[1] == "metrics":
            scheduler.track_promotion_metrics()
        else:
            print("可用命令: plan, ideas, report, checklist, metrics")
    else:
        main()
