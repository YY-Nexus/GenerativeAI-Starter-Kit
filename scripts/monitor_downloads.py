#!/usr/bin/env python3
# type: ignore
"""
PyPI 下载量监控脚本
监控 genai-starter-kit 包的下载统计和使用情况
"""
import requests
import json
from datetime import datetime, timedelta
import sys
import os


def get_pypi_info():
    """获取 PyPI 包基本信息"""
    package_name = "genai-starter-kit"
    url = f"https://pypi.org/pypi/{package_name}/json"

    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                "name": data["info"]["name"],
                "version": data["info"]["version"],
                "summary": data["info"]["summary"],
                "upload_time": data["info"].get("upload_time", "未知"),
                "author": data["info"].get("author", "未知"),
                "license": data["info"].get("license", "未知"),
                "keywords": data["info"].get("keywords", ""),
                "home_page": data["info"].get("home_page", ""),
                "download_url": data["info"].get("download_url", ""),
                "project_urls": data["info"].get("project_urls", {}),
                "releases_count": len(data["releases"]),
            }
    except Exception as e:
        print(f"❌ 获取 PyPI 信息失败: {e}")

    return None


def get_github_stats():
    """获取 GitHub 仓库统计"""
    repo_url = "https://api.github.com/repos/YY-Nexus/GenerativeAI-Starter-Kit"

    try:
        response = requests.get(repo_url, timeout=10)
        if response.status_code == 200:
            data = response.json()
            return {
                "stars": data["stargazers_count"],
                "forks": data["forks_count"],
                "watchers": data["subscribers_count"],
                "open_issues": data["open_issues_count"],
                "size": data["size"],
                "language": data["language"],
                "created_at": data["created_at"],
                "updated_at": data["updated_at"],
                "pushed_at": data["pushed_at"],
            }
    except Exception as e:
        print(f"❌ 获取 GitHub 统计失败: {e}")

    return None


def get_pypistats():
    """尝试获取下载统计（需要 pypistats 包）"""
    try:
        import subprocess

        result = subprocess.run(
            [
                sys.executable,
                "-c",
                'import pypistats; print(pypistats.recent("genai-starter-kit", format="json"))',
            ],
            capture_output=True,
            text=True,
            timeout=30,
        )

        if result.returncode == 0:
            try:
                return json.loads(result.stdout)
            except json.JSONDecodeError:
                pass
    except Exception as e:
        print(f"💡 提示: 安装 pypistats 获取详细下载统计: pip install pypistats")

    return None


def create_monitoring_dashboard():
    """创建监控仪表板"""
    print("🔍 genai-starter-kit 包监控报告")
    print("=" * 60)
    print(f"📅 报告生成时间: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    # PyPI 信息
    pypi_info = get_pypi_info()
    if pypi_info:
        print("📦 PyPI 包信息")
        print("-" * 30)
        print(f"📦 包名: {pypi_info['name']}")
        print(f"🔢 当前版本: {pypi_info['version']}")
        print(f"📝 描述: {pypi_info['summary']}")
        print(f"👤 作者: {pypi_info['author']}")
        print(f"📄 许可证: {pypi_info['license']}")
        print(f"📅 最后更新: {pypi_info['upload_time']}")
        print(f"🔢 版本总数: {pypi_info['releases_count']}")

        if pypi_info["keywords"]:
            print(f"🏷️  关键词: {pypi_info['keywords']}")

        print(f"🔗 项目主页: {pypi_info['home_page']}")
        print()

    # GitHub 统计
    github_stats = get_github_stats()
    if github_stats:
        print("⭐ GitHub 仓库统计")
        print("-" * 30)
        print(f"⭐ Stars: {github_stats['stars']}")
        print(f"🍴 Forks: {github_stats['forks']}")
        print(f"👀 Watchers: {github_stats['watchers']}")
        print(f"🐛 开放 Issues: {github_stats['open_issues']}")
        print(f"💾 仓库大小: {github_stats['size']} KB")
        print(f"💻 主要语言: {github_stats['language']}")
        print(f"📅 创建时间: {github_stats['created_at'][:10]}")
        print(f"🔄 最近更新: {github_stats['updated_at'][:10]}")
        print(f"📤 最近推送: {github_stats['pushed_at'][:10]}")
        print()

    # 下载统计
    download_stats = get_pypistats()
    if download_stats:
        print("📊 下载统计")
        print("-" * 30)
        if isinstance(download_stats, dict) and "data" in download_stats:
            total_downloads = sum(item["downloads"] for item in download_stats["data"])
            print(f"📥 最近下载量: {total_downloads}")
        print()

    # 有用的链接
    print("🔗 有用的监控链接")
    print("-" * 30)
    print("PyPI 页面: https://pypi.org/project/genai-starter-kit/")
    print("下载统计: https://pypistats.org/packages/genai-starter-kit")
    print("GitHub 仓库: https://github.com/YY-Nexus/GenerativeAI-Starter-Kit")
    print("Libraries.io: https://libraries.io/pypi/genai-starter-kit")
    print()

    # 建议
    print("💡 监控建议")
    print("-" * 30)
    print("1. 每日检查 GitHub issues 和 PR")
    print("2. 每周查看下载趋势")
    print("3. 监控用户反馈和评价")
    print("4. 关注竞品和相关项目")
    print("5. 定期更新包版本")


def save_monitoring_data():
    """保存监控数据到文件"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"monitoring_data_{timestamp}.json"

    data = {
        "timestamp": datetime.now().isoformat(),
        "pypi_info": get_pypi_info(),
        "github_stats": get_github_stats(),
        "download_stats": get_pypistats(),
    }

    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
        print(f"💾 监控数据已保存到: {filename}")
    except Exception as e:
        print(f"❌ 保存数据失败: {e}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--save":
        save_monitoring_data()
    else:
        create_monitoring_dashboard()
