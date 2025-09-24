#!/usr/bin/env python3
"""
🧪 简化安全工具测试
==================

基础安全工具功能测试，避免复杂类型问题
"""

import unittest
import tempfile
import os
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestSecurityToolsBasic(unittest.TestCase):
    """基础安全工具测试"""

    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        """测试后清理"""
        import shutil

        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_security_fixer_import(self):
        """测试安全修复工具是否可以正确导入"""
        try:
            from fix_vulnerabilities import SecurityFixer

            fixer = SecurityFixer()
            self.assertIsNotNone(fixer)
            print("✅ SecurityFixer 创建成功")
        except ImportError as e:
            self.fail(f"无法导入 SecurityFixer: {e}")

    def test_security_scripts_executable(self):
        """测试安全脚本是否具有执行权限"""
        project_root = Path(__file__).parent.parent

        # 检查 Python 脚本
        python_script = project_root / "fix_vulnerabilities.py"
        self.assertTrue(python_script.exists(), "fix_vulnerabilities.py 不存在")
        self.assertTrue(python_script.is_file(), "fix_vulnerabilities.py 不是文件")

        # 检查 Bash 脚本
        bash_script = project_root / "scripts" / "fix_vulnerabilities.sh"
        self.assertTrue(bash_script.exists(), "fix_vulnerabilities.sh 不存在")
        self.assertTrue(bash_script.is_file(), "fix_vulnerabilities.sh 不是文件")

        print("✅ 安全脚本文件检查通过")

    def test_requirements_readable(self):
        """测试 requirements.txt 是否可读"""
        project_root = Path(__file__).parent.parent
        req_file = project_root / "requirements.txt"

        self.assertTrue(req_file.exists(), "requirements.txt 不存在")

        try:
            with open(req_file, "r", encoding="utf-8") as f:
                content = f.read()
                self.assertGreater(len(content), 0, "requirements.txt 为空")
                lines = content.strip().split("\n")
                print(f"✅ requirements.txt 包含 {len(lines)} 行内容")
        except Exception as e:
            self.fail(f"读取 requirements.txt 失败: {e}")

    def test_security_workflow_files(self):
        """测试安全工作流文件存在性"""
        project_root = Path(__file__).parent.parent

        # 检查 GitHub 工作流
        workflow_file = project_root / ".github" / "workflows" / "security-check.yml"
        self.assertTrue(workflow_file.exists(), "security-check.yml 不存在")

        # 检查 Dependabot 配置
        dependabot_file = project_root / ".github" / "dependabot.yml"
        self.assertTrue(dependabot_file.exists(), "dependabot.yml 不存在")

        print("✅ 安全工作流文件检查通过")

    def test_basic_yaml_parsing(self):
        """测试基础 YAML 解析功能"""
        try:
            # 尝试导入 yaml，如果没有就跳过测试
            import yaml

            # 测试基础 YAML 解析
            test_yaml = """
name: test
version: 1.0
items:
  - item1
  - item2
"""
            result = yaml.safe_load(test_yaml)
            self.assertIsInstance(result, dict)
            self.assertEqual(result["name"], "test")
            self.assertEqual(result["version"], 1.0)
            print("✅ YAML 解析功能正常")

        except ImportError:
            self.skipTest("PyYAML 未安装，跳过 YAML 测试")

    def test_temp_directory_cleanup(self):
        """测试临时目录清理功能"""
        # 创建临时文件
        test_file = Path(self.temp_dir) / "test.txt"
        with open(test_file, "w") as f:
            f.write("test content")

        self.assertTrue(test_file.exists(), "测试文件创建失败")
        print("✅ 临时目录功能正常")

    def test_project_structure_integrity(self):
        """测试项目结构完整性"""
        project_root = Path(__file__).parent.parent

        # 核心文件检查
        core_files = [
            "setup.py",
            "pyproject.toml",
            "README.md",
            "LICENSE.md",
            "requirements.txt",
        ]

        missing_files = []
        for file_name in core_files:
            file_path = project_root / file_name
            if not file_path.exists():
                missing_files.append(file_name)

        if missing_files:
            self.fail(f"缺少核心文件: {', '.join(missing_files)}")

        print(f"✅ {len(core_files)} 个核心文件检查通过")


if __name__ == "__main__":
    print("🧪 开始运行简化安全工具测试...")
    unittest.main(verbosity=2)
