#!/usr/bin/env python3
"""
🧪 基础安全工具测试
==================

简化的安全工具测试，避免复杂依赖
"""

import unittest
import tempfile
import os
import sys
from pathlib import Path

# 添加项目根目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

class TestBasicSecurity(unittest.TestCase):
    """基础安全测试"""

    def setUp(self):
        """测试前准备"""
        self.temp_dir = tempfile.mkdtemp()
        
    def tearDown(self):
        """测试后清理"""
        import shutil
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_import_security_tools(self):
        """测试是否可以正确导入安全工具"""
        try:
            from fix_vulnerabilities import SecurityFixer
            self.assertIsNotNone(SecurityFixer)
            print("✅ SecurityFixer 导入成功")
        except ImportError as e:
            self.fail(f"无法导入 SecurityFixer: {e}")

    def test_requirements_file_exists(self):
        """测试 requirements.txt 文件是否存在"""
        req_path = Path(__file__).parent.parent / "requirements.txt"
        self.assertTrue(req_path.exists(), "requirements.txt 文件不存在")
        
        # 检查文件内容不为空
        with open(req_path) as f:
            content = f.read().strip()
            self.assertTrue(len(content) > 0, "requirements.txt 文件为空")
            print(f"✅ requirements.txt 包含 {len(content.splitlines())} 行依赖")

    def test_security_scripts_exist(self):
        """测试安全脚本是否存在"""
        project_root = Path(__file__).parent.parent
        
        # 检查 Python 脚本
        python_script = project_root / "fix_vulnerabilities.py"
        self.assertTrue(python_script.exists(), "fix_vulnerabilities.py 不存在")
        
        # 检查 Bash 脚本
        bash_script = project_root / "scripts" / "fix_vulnerabilities.sh"
        self.assertTrue(bash_script.exists(), "fix_vulnerabilities.sh 不存在")
        
        print("✅ 安全脚本文件都存在")

    def test_github_workflows_exist(self):
        """测试 GitHub 工作流文件是否存在"""
        project_root = Path(__file__).parent.parent
        
        # 检查工作流目录
        workflow_dir = project_root / ".github" / "workflows"
        self.assertTrue(workflow_dir.exists(), "GitHub workflows 目录不存在")
        
        # 检查安全检查工作流
        security_workflow = workflow_dir / "security-check.yml"
        self.assertTrue(security_workflow.exists(), "security-check.yml 不存在")
        
        print("✅ GitHub 工作流文件存在")

    def test_dependabot_config_exists(self):
        """测试 Dependabot 配置是否存在"""
        project_root = Path(__file__).parent.parent
        dependabot_config = project_root / ".github" / "dependabot.yml"
        self.assertTrue(dependabot_config.exists(), "dependabot.yml 不存在")
        print("✅ Dependabot 配置文件存在")

    def test_project_structure(self):
        """测试项目结构完整性"""
        project_root = Path(__file__).parent.parent
        
        # 必需的目录
        required_dirs = [
            "scripts",
            "tests", 
            ".github/workflows",
            "docs",
            "RAG",
            "examples"
        ]
        
        for dir_path in required_dirs:
            full_path = project_root / dir_path
            self.assertTrue(full_path.exists(), f"必需目录 {dir_path} 不存在")
        
        print("✅ 项目结构完整")

if __name__ == "__main__":
    print("🧪 开始运行基础安全工具测试...")
    unittest.main(verbosity=2)