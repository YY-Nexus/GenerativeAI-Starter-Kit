import pkg_resources
from typing import Dict, List

# 更新为当前实际版本
EXPECTED: Dict[str, str] = {
    "torch": "2.8.0",  # 已更新
    "transformers": "4.56.2",  # 已更新
    # "sentence-transformers": "2.2.2",  # 已从项目中移除
    # "langchain": "0.3.26",  # 已从项目中移除
    "numpy": "2.3.3",  # 核心数值计算库
    "fastapi": "0.117.1",  # Web API 框架
}


def check_versions():
    """检查关键依赖的版本是否符合要求"""
    print("🔍 检查关键依赖版本...\n")

    success_count = 0
    total_count = len(EXPECTED)

    for pkg, expected_min in EXPECTED.items():
        try:
            installed = pkg_resources.get_distribution(pkg).version
            # 检查版本是否大于等于期望的最低版本
            if _version_compare(installed, expected_min) >= 0:
                print(f"✅ {pkg:<20} 版本 OK: {installed} (>= {expected_min})")
                success_count += 1
            else:
                print(f"❌ {pkg:<20} 版本过低: {installed} (期望 >= {expected_min})")
        except pkg_resources.DistributionNotFound:
            print(f"⚠️  {pkg:<20} 未安装")
        except Exception as e:
            print(f"❌ {pkg:<20} 检查失败: {e}")

    print(f"\n📊 检查结果: {success_count}/{total_count} 依赖符合要求")

    if success_count < total_count:
        print("⚠️  建议运行: python fix_vulnerabilities.py --auto-fix")
        return False
    else:
        print("✨ 所有关键依赖都符合要求！")
        return True


def _version_compare(v1: str, v2: str) -> int:
    """简单的版本比较函数"""

    def normalize(v: str) -> List[int]:
        return [int(x) for x in v.split(".") if x.isdigit()]

    v1_parts = normalize(v1)
    v2_parts = normalize(v2)

    # 补齐到相同长度
    max_len = max(len(v1_parts), len(v2_parts))
    v1_parts.extend([0] * (max_len - len(v1_parts)))
    v2_parts.extend([0] * (max_len - len(v2_parts)))

    if v1_parts > v2_parts:
        return 1
    elif v1_parts < v2_parts:
        return -1
    else:
        return 0


if __name__ == "__main__":
    check_versions()
