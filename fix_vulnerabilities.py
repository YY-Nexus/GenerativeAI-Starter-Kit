#!/usr/bin/env python3
"""
🛡️ 自动安全漏洞修复工具
=======================

这个脚本提供了一个自动化的方式来检测和修复 Python 项目中的安全漏洞。

功能：
- 扫描已安装包的安全漏洞
- 自动更新有漏洞的包到安全版本
- 更新 requirements.txt 文件
- 生成详细的安全报告

使用方法：
    python fix_vulnerabilities.py [--auto-fix] [--report-only]
    
参数：
    --auto-fix    : 自动修复发现的漏洞
    --report-only : 仅生成报告，不进行修复
"""

import argparse
import json
import subprocess
import sys
import re
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Any
import shutil


class SecurityFixer:
    """安全漏洞修复器"""
    
    def __init__(self, project_root: str = "."):
        self.project_root = Path(project_root).resolve()
        self.backup_file_paths: List[Path] = []
        
    def log_info(self, message: str):
        """输出信息日志"""
        print(f"\033[34m[INFO]\033[0m {message}")
        
    def log_success(self, message: str):
        """输出成功日志"""
        print(f"\033[32m[SUCCESS]\033[0m {message}")
        
    def log_warning(self, message: str):
        """输出警告日志"""
        print(f"\033[33m[WARNING]\033[0m {message}")
        
    def log_error(self, message: str):
        """输出错误日志"""
        print(f"\033[31m[ERROR]\033[0m {message}")
        
    def check_tools(self) -> bool:
        """检查必要工具是否安装"""
        self.log_info("检查安全扫描工具...")
        
        tools_to_install: List[str] = []
        
        # 检查 safety
        try:
            import safety  # type: ignore
        except ImportError:
            tools_to_install.append("safety")
            
        # 检查 pip-audit
        if not shutil.which("pip-audit"):
            tools_to_install.append("pip-audit")
            
        # 安装缺失的工具
        if tools_to_install:
            self.log_info(f"安装缺失的工具: {', '.join(tools_to_install)}")
            try:
                subprocess.run([
                    sys.executable, "-m", "pip", "install"
                ] + tools_to_install, check=True, capture_output=True)
                self.log_success("安全工具安装完成")
            except subprocess.CalledProcessError as e:
                self.log_error(f"工具安装失败: {e}")
                return False
                
        return True
        
    def backup_files(self):
        """备份重要文件"""
        self.log_info("备份项目文件...")
        
        files_to_backup = ["requirements.txt", "pyproject.toml", "setup.py"]
        
        for file_name in files_to_backup:
            file_path = self.project_root / file_name
            if file_path.exists():
                backup_path = file_path.with_suffix(file_path.suffix + ".backup")
                shutil.copy2(file_path, backup_path)
                self.backup_file_paths.append(backup_path)
                self.log_success(f"已备份 {file_name} 到 {backup_path.name}")
                
    def scan_with_safety(self) -> Dict[str, Any]:
        """使用 Safety 扫描漏洞"""
        self.log_info("使用 Safety 扫描安全漏洞...")
        
        try:
            result = subprocess.run([
                sys.executable, "-m", "safety", "scan", "--json"
            ], capture_output=True, text=True, timeout=120)
            
            if result.stdout:
                # 保存扫描结果
                output_file = self.project_root / "safety_scan_results.json"
                with open(output_file, "w") as f:
                    f.write(result.stdout)
                    
                try:
                    return json.loads(result.stdout)
                except json.JSONDecodeError:
                    self.log_warning("Safety 输出格式解析失败，使用文本格式")
                    return {"raw_output": result.stdout}
            else:
                self.log_info("Safety 扫描完成，未发现漏洞")
                return {"vulnerabilities": []}
                
        except subprocess.TimeoutExpired:
            self.log_error("Safety 扫描超时")
            return {}
        except subprocess.CalledProcessError as e:
            self.log_error(f"Safety 扫描失败: {e}")
            return {}
            
    def scan_with_pip_audit(self) -> Dict[str, Any]:
        """使用 pip-audit 扫描漏洞"""
        self.log_info("使用 pip-audit 扫描安全漏洞...")
        
        try:
            result = subprocess.run([
                "pip-audit", "--format=json"
            ], capture_output=True, text=True, timeout=120)
            
            if result.stdout:
                # 保存扫描结果
                output_file = self.project_root / "pip_audit_results.json"
                with open(output_file, "w") as f:
                    f.write(result.stdout)
                    
                return json.loads(result.stdout)
            else:
                self.log_info("pip-audit 扫描完成，未发现漏洞")
                return {"dependencies": []}
                
        except subprocess.TimeoutExpired:
            self.log_error("pip-audit 扫描超时")
            return {}
        except subprocess.CalledProcessError as e:
            if "No known vulnerabilities found" in str(e):
                self.log_info("pip-audit 扫描完成，未发现漏洞")
                return {"dependencies": []}
            self.log_error(f"pip-audit 扫描失败: {e}")
            return {}
        except json.JSONDecodeError as e:
            self.log_warning(f"pip-audit 输出解析失败: {e}")
            return {}
            
    def get_outdated_packages(self) -> List[Dict[str, Any]]:
        """获取过时的包列表"""
        self.log_info("检查过时的包...")
        
        try:
            result = subprocess.run([
                sys.executable, "-m", "pip", "list", "--outdated", "--format=json"
            ], capture_output=True, text=True, check=True)
            
            return json.loads(result.stdout)
        except (subprocess.CalledProcessError, json.JSONDecodeError) as e:
            self.log_warning(f"获取过时包列表失败: {e}")
            return []
            
    def update_package(self, package_name: str, target_version: Optional[str] = None) -> bool:
        """更新指定包"""
        try:
            if target_version:
                cmd = [sys.executable, "-m", "pip", "install", f"{package_name}=={target_version}"]
                self.log_info(f"更新 {package_name} 到版本 {target_version}")
            else:
                cmd = [sys.executable, "-m", "pip", "install", "--upgrade", package_name]
                self.log_info(f"更新 {package_name} 到最新版本")
                
            subprocess.run(cmd, capture_output=True, text=True, check=True)
            self.log_success(f"成功更新 {package_name}")
            return True
            
        except subprocess.CalledProcessError as e:
            self.log_error(f"更新 {package_name} 失败: {e.stderr}")
            return False
            
    def fix_vulnerabilities(self, safety_results: Dict[str, Any], pip_audit_results: Dict[str, Any]) -> Dict[str, List[str]]:
        """修复发现的漏洞"""
        self.log_info("开始修复安全漏洞...")
        
        fixed_packages: List[str] = []
        failed_packages: List[str] = []
        
        # 处理 Safety 发现的漏洞
        if "vulnerabilities" in safety_results:
            for vuln in safety_results["vulnerabilities"]:
                if isinstance(vuln, dict) and "package_name" in vuln:
                    package_name = str(vuln["package_name"])  # type: ignore
                    # 尝试更新到最新版本
                    if self.update_package(package_name):
                        fixed_packages.append(package_name)
                    else:
                        failed_packages.append(package_name)
                        
        # 处理 pip-audit 发现的漏洞
        if "dependencies" in pip_audit_results:
            for dep in pip_audit_results["dependencies"]:
                if isinstance(dep, dict) and "name" in dep:
                    package_name = str(dep["name"])  # type: ignore
                    # 如果有推荐的安全版本，使用它
                    target_version: Optional[str] = None
                    if "vulnerabilities" in dep:
                        for vuln in dep["vulnerabilities"]:  # type: ignore
                            if isinstance(vuln, dict) and "fix_versions" in vuln and vuln["fix_versions"]:
                                target_version = str(vuln["fix_versions"][0])  # type: ignore
                                break
                                
                    if self.update_package(package_name, target_version):
                        if package_name not in fixed_packages:
                            fixed_packages.append(package_name)
                    else:
                        if package_name not in failed_packages:
                            failed_packages.append(package_name)
                            
        # 更新所有过时的包（作为额外的安全措施）
        outdated_packages = self.get_outdated_packages()
        for pkg in outdated_packages:
            package_name = pkg["name"]
            if package_name not in fixed_packages and package_name not in failed_packages:
                if self.update_package(package_name):
                    fixed_packages.append(package_name)
                    
        return {
            "fixed": fixed_packages,
            "failed": failed_packages
        }
        
    def update_requirements_txt(self):
        """更新 requirements.txt 文件"""
        requirements_file = self.project_root / "requirements.txt"
        if not requirements_file.exists():
            self.log_warning("requirements.txt 文件不存在")
            return
            
        self.log_info("更新 requirements.txt...")
        
        try:
            # 读取当前内容
            with open(requirements_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                
            updated_lines: List[str] = []
            
            for line in lines:
                line = line.strip()
                
                # 跳过注释和空行
                if line.startswith("#") or not line:
                    updated_lines.append(line)
                    continue
                    
                # 解析包名
                match = re.match(r"^([a-zA-Z0-9_-]+)", line)
                if match:
                    package_name = match.group(1)
                    
                    # 获取当前安装的版本
                    try:
                        result = subprocess.run([
                            sys.executable, "-m", "pip", "show", package_name
                        ], capture_output=True, text=True, check=True)
                        
                        for show_line in result.stdout.split("\n"):
                            if show_line.startswith("Version:"):
                                version = show_line.split(":", 1)[1].strip()
                                # 使用 >= 约束允许未来的安全更新
                                updated_line = f"{package_name}>={version}"
                                # 保留原有注释
                                if "#" in line:
                                    comment = line[line.index("#"):]
                                    updated_line += f"  {comment}"
                                updated_lines.append(updated_line)
                                break
                        else:
                            # 如果没有找到版本信息，保持原行不变
                            updated_lines.append(line)
                            
                    except subprocess.CalledProcessError:
                        # 如果包没有安装，保持原行不变
                        updated_lines.append(line)
                else:
                    updated_lines.append(line)
                    
            # 写入更新后的内容
            with open(requirements_file, "w", encoding="utf-8") as f:
                f.write("\n".join(updated_lines))
                
            self.log_success("requirements.txt 已更新")
            
        except Exception as e:
            self.log_error(f"更新 requirements.txt 失败: {e}")
            
    def generate_report(self, safety_results: Dict[str, Any], pip_audit_results: Dict[str, Any], fix_results: Dict[str, List[str]]):
        """生成安全报告"""
        self.log_info("生成安全报告...")
        
        report_file = self.project_root / "security_report.md"
        
        with open(report_file, "w", encoding="utf-8") as f:
            f.write("# 🛡️ 安全漏洞修复报告\n\n")
            f.write(f"**生成时间**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
            
            # 扫描工具信息
            f.write("## 🔍 扫描工具\n\n")
            f.write("- ✅ **Safety** - Python 包安全漏洞扫描器\n")
            f.write("- ✅ **pip-audit** - PyPI 包安全审计工具\n\n")
            
            # 修复结果
            f.write("## 🔧 修复结果\n\n")
            if fix_results:
                if fix_results["fixed"]:
                    f.write("### ✅ 成功修复的包\n\n")
                    for pkg in fix_results["fixed"]:
                        f.write(f"- {pkg}\n")
                    f.write("\n")
                    
                if fix_results["failed"]:
                    f.write("### ❌ 修复失败的包\n\n")
                    for pkg in fix_results["failed"]:
                        f.write(f"- {pkg}\n")
                    f.write("\n")
                    
                if not fix_results["fixed"] and not fix_results["failed"]:
                    f.write("✅ 没有发现需要修复的安全漏洞\n\n")
            
            # Safety 结果
            f.write("## 📊 Safety 扫描结果\n\n")
            if safety_results:
                f.write("```json\n")
                f.write(json.dumps(safety_results, indent=2, ensure_ascii=False))
                f.write("\n```\n\n")
            else:
                f.write("无可用的 Safety 扫描结果\n\n")
                
            # pip-audit 结果
            f.write("## 📊 pip-audit 扫描结果\n\n")
            if pip_audit_results:
                f.write("```json\n")
                f.write(json.dumps(pip_audit_results, indent=2, ensure_ascii=False))
                f.write("\n```\n\n")
            else:
                f.write("无可用的 pip-audit 扫描结果\n\n")
                
            # 备份文件信息
            f.write("## 📁 备份文件\n\n")
            if self.backup_file_paths:
                for backup_file in self.backup_file_paths:
                    f.write(f"- `{backup_file.name}`\n")
                f.write("\n")
                f.write("如果需要恢复，可以使用以下命令：\n")
                f.write("```bash\n")
                f.write("cp requirements.txt.backup requirements.txt\n")
                f.write("pip install -r requirements.txt\n")
                f.write("```\n\n")
            
            # 建议
            f.write("## 💡 安全建议\n\n")
            f.write("1. **定期扫描**: 建议每周运行一次安全扫描\n")
            f.write("2. **自动化更新**: 考虑使用 GitHub Dependabot 自动更新依赖\n")
            f.write("3. **虚拟环境**: 使用虚拟环境隔离项目依赖\n")
            f.write("4. **监控通告**: 关注 GitHub Security Advisories 和 PyPI 安全通告\n")
            f.write("5. **版本锁定**: 在生产环境中使用精确的版本号\n\n")
            
        self.log_success(f"安全报告已生成: {report_file}")


def main():
    parser = argparse.ArgumentParser(
        description="自动检测和修复 Python 项目中的安全漏洞",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__
    )
    
    parser.add_argument(
        "--auto-fix",
        action="store_true",
        help="自动修复发现的漏洞"
    )
    
    parser.add_argument(
        "--report-only",
        action="store_true", 
        help="仅生成报告，不进行修复"
    )
    
    parser.add_argument(
        "--project-root",
        default=".",
        help="项目根目录路径（默认: 当前目录）"
    )
    
    args = parser.parse_args()
    
    # 创建修复器实例
    fixer = SecurityFixer(args.project_root)
    
    print("=" * 70)
    print("🛡️  Python 安全漏洞自动修复工具")
    print("=" * 70)
    
    # 检查工具
    if not fixer.check_tools():
        sys.exit(1)
        
    # 备份文件
    fixer.backup_files()
    
    # 扫描漏洞
    safety_results = fixer.scan_with_safety()
    pip_audit_results = fixer.scan_with_pip_audit()
    
    fix_results = {}
    
    # 根据参数决定是否修复
    if args.report_only:
        fixer.log_info("仅生成报告模式，跳过自动修复")
    elif args.auto_fix:
        fix_results = fixer.fix_vulnerabilities(safety_results, pip_audit_results)
        fixer.update_requirements_txt()
    else:
        # 交互模式
        print("\n发现以下安全扫描结果:")
        if safety_results and "vulnerabilities" in safety_results:
            print(f"- Safety: {len(safety_results['vulnerabilities'])} 个潜在问题")
        if pip_audit_results and "dependencies" in pip_audit_results:
            print(f"- pip-audit: {len(pip_audit_results['dependencies'])} 个依赖项")
            
        if input("\n是否要自动修复这些问题? (y/N): ").lower() == 'y':
            fix_results = fixer.fix_vulnerabilities(safety_results, pip_audit_results)
            fixer.update_requirements_txt()
    
    # 生成报告
    fixer.generate_report(safety_results, pip_audit_results, fix_results)
    
    print("=" * 70)
    print("🎉 安全检查和修复完成!")
    print("=" * 70)
    print("\n📋 生成的文件:")
    print("  - security_report.md           # 详细安全报告")
    print("  - safety_scan_results.json     # Safety 扫描原始结果")  
    print("  - pip_audit_results.json       # pip-audit 扫描原始结果")
    if fixer.backup_file_paths:
        print("  - *.backup                     # 原始文件备份")
    print("\n建议查看 security_report.md 了解详细信息。")


if __name__ == "__main__":
    main()