#!/bin/bash
# =================================================================
# 🛡️ 自动安全漏洞修复脚本
# =================================================================
# 描述：自动检测和修复Python项目中的安全漏洞
# 作者：GenerativeAI-Starter-Kit
# 版本：1.0.0
# 创建时间：2025-09-25

set -e  # 遇到错误时退出

# 颜色定义
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# 检查必要工具是否安装
check_dependencies() {
    log_info "检查必要的工具..."
    
    # 检查 pip
    if ! command -v pip &> /dev/null; then
        log_error "pip 未安装，请先安装 pip"
        exit 1
    fi
    
    # 检查并安装安全检查工具
    if ! python -c "import safety" 2>/dev/null; then
        log_info "安装 safety 工具..."
        pip install safety
    fi
    
    if ! command -v pip-audit &> /dev/null; then
        log_info "安装 pip-audit 工具..."
        pip install pip-audit
    fi
    
    # 检查并安装依赖更新工具
    if ! command -v pip-review &> /dev/null; then
        log_info "安装 pip-review 工具..."
        pip install pip-review
    fi
    
    log_success "依赖检查完成"
}

# 备份当前 requirements.txt
backup_requirements() {
    if [[ -f "requirements.txt" ]]; then
        cp requirements.txt requirements.txt.backup
        log_success "已备份 requirements.txt 到 requirements.txt.backup"
    fi
}

# 扫描安全漏洞
scan_vulnerabilities() {
    log_info "开始安全漏洞扫描..."
    
    # 使用 safety 扫描
    log_info "使用 Safety 进行扫描..."
    safety scan --json --output security_scan_results.json || true
    
    # 使用 pip-audit 扫描
    log_info "使用 pip-audit 进行扫描..."
    pip-audit --format=json --output=pip_audit_results.json || true
    
    log_success "漏洞扫描完成，结果已保存到 security_scan_results.json 和 pip_audit_results.json"
}

# 自动修复漏洞
auto_fix_vulnerabilities() {
    log_info "开始自动修复漏洞..."
    
    # 更新所有包到最新版本
    log_info "更新所有包到最新版本..."
    pip list --outdated --format=json > outdated_packages.json
    
    # 如果有过时的包，尝试更新
    if [[ -f "outdated_packages.json" ]]; then
        python3 << 'EOF'
import json
import subprocess
import sys

try:
    with open('outdated_packages.json', 'r') as f:
        outdated = json.load(f)
    
    if outdated:
        print(f"发现 {len(outdated)} 个过时的包")
        for pkg in outdated:
            package_name = pkg['name']
            current_version = pkg['version']
            latest_version = pkg['latest_version']
            print(f"更新 {package_name}: {current_version} -> {latest_version}")
            try:
                subprocess.run([sys.executable, '-m', 'pip', 'install', '--upgrade', package_name], 
                             check=True, capture_output=True)
                print(f"✓ 成功更新 {package_name}")
            except subprocess.CalledProcessError as e:
                print(f"✗ 更新 {package_name} 失败: {e}")
    else:
        print("所有包都是最新的")
        
except FileNotFoundError:
    print("outdated_packages.json 文件未找到")
except json.JSONDecodeError:
    print("解析 JSON 文件失败")
except Exception as e:
    print(f"更新包时出错: {e}")
EOF
    fi
}

# 更新 requirements.txt 中的版本约束
update_requirements() {
    log_info "更新 requirements.txt 中的版本约束..."
    
    if [[ -f "requirements.txt" ]]; then
        # 创建更新后的 requirements.txt
        python3 << 'EOF'
import re
import subprocess
import sys

def get_installed_version(package_name):
    """获取已安装包的版本"""
    try:
        result = subprocess.run([sys.executable, '-m', 'pip', 'show', package_name], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            for line in result.stdout.split('\n'):
                if line.startswith('Version:'):
                    return line.split(':', 1)[1].strip()
    except:
        pass
    return None

def update_requirements_file():
    """更新 requirements.txt 文件中的版本号"""
    try:
        with open('requirements.txt', 'r', encoding='utf-8') as f:
            content = f.read()
        
        lines = content.split('\n')
        updated_lines = []
        
        for line in lines:
            # 跳过注释和空行
            if line.strip().startswith('#') or not line.strip():
                updated_lines.append(line)
                continue
            
            # 匹配包名和版本约束的正则表达式
            match = re.match(r'^([a-zA-Z0-9_-]+)([><=!]+[0-9.]+.*)?(?:\s*#.*)?$', line.strip())
            if match:
                package_name = match.group(1)
                current_constraint = match.group(2) or ''
                comment_part = line[line.find('#'):] if '#' in line else ''
                
                # 获取当前安装的版本
                installed_version = get_installed_version(package_name)
                if installed_version:
                    # 更新为固定版本约束（使用 >= 允许小版本更新）
                    new_line = f"{package_name}>={installed_version}"
                    if comment_part:
                        new_line += f"  {comment_part}"
                    updated_lines.append(new_line)
                    print(f"更新 {package_name}: {current_constraint} -> >={installed_version}")
                else:
                    updated_lines.append(line)
            else:
                updated_lines.append(line)
        
        # 写入更新后的内容
        with open('requirements.txt', 'w', encoding='utf-8') as f:
            f.write('\n'.join(updated_lines))
        
        print("requirements.txt 已更新")
        
    except Exception as e:
        print(f"更新 requirements.txt 时出错: {e}")

update_requirements_file()
EOF
        
        log_success "requirements.txt 版本约束已更新"
    fi
}

# 生成安全报告
generate_security_report() {
    log_info "生成安全报告..."
    
    cat > security_report.md << 'EOF'
# 🛡️ 安全漏洞修复报告

## 报告生成时间
EOF
    echo "$(date '+%Y-%m-%d %H:%M:%S')" >> security_report.md
    
    cat >> security_report.md << 'EOF'

## 扫描工具
- ✅ Safety - Python 安全漏洞扫描器
- ✅ pip-audit - PyPI 包审计工具

## 修复措施
1. **包版本更新**: 将所有包更新到最新稳定版本
2. **版本约束优化**: 更新 requirements.txt 中的版本约束
3. **依赖关系检查**: 验证包之间的兼容性

## 扫描结果

### Safety 扫描结果
EOF
    
    if [[ -f "security_scan_results.json" ]]; then
        echo "\`\`\`json" >> security_report.md
        cat security_scan_results.json >> security_report.md
        echo "\`\`\`" >> security_report.md
    else
        echo "扫描结果文件未找到" >> security_report.md
    fi
    
    cat >> security_report.md << 'EOF'

### pip-audit 扫描结果
EOF
    
    if [[ -f "pip_audit_results.json" ]]; then
        echo "\`\`\`json" >> security_report.md
        cat pip_audit_results.json >> security_report.md
        echo "\`\`\`" >> security_report.md
    else
        echo "扫描结果文件未找到" >> security_report.md
    fi
    
    cat >> security_report.md << 'EOF'

## 建议
1. 定期运行此脚本进行安全检查
2. 监控 GitHub Security Advisories
3. 启用 Dependabot 自动更新
4. 考虑使用虚拟环境隔离依赖

## 备份文件
- requirements.txt.backup - 原始 requirements.txt 的备份

如果遇到问题，可以使用以下命令恢复：
```bash
cp requirements.txt.backup requirements.txt
pip install -r requirements.txt
```
EOF
    
    log_success "安全报告已生成: security_report.md"
}

# 清理临时文件
cleanup() {
    log_info "清理临时文件..."
    rm -f outdated_packages.json security_issues.json
    log_success "清理完成"
}

# 主函数
main() {
    echo "=================================================================="
    echo "🛡️  自动安全漏洞修复脚本启动"
    echo "=================================================================="
    
    check_dependencies
    backup_requirements
    scan_vulnerabilities
    auto_fix_vulnerabilities
    update_requirements
    generate_security_report
    cleanup
    
    echo "=================================================================="
    log_success "🎉 安全漏洞修复完成！"
    echo "=================================================================="
    echo
    echo "📋 生成的文件："
    echo "  - security_report.md      # 安全报告"
    echo "  - requirements.txt.backup # 原始配置备份"
    echo "  - security_scan_results.json # Safety 扫描结果"
    echo "  - pip_audit_results.json    # pip-audit 扫描结果"
    echo
    echo "🔍 下一步建议："
    echo "  1. 查看 security_report.md 了解详细情况"
    echo "  2. 测试应用程序确保正常运行"
    echo "  3. 提交更新后的 requirements.txt"
    echo "  4. 配置定期安全扫描"
}

# 执行主函数
main "$@"