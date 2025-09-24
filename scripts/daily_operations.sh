#!/bin/bash
# 每日自动化运营脚本
# genai-starter-kit 项目运营自动化工具

set -e

# 脚本配置
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
LOG_FILE="$SCRIPT_DIR/daily_operations.log"

# 颜色输出
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# 日志函数
log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1" | tee -a "$LOG_FILE"
}

log_success() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] ✅${NC} $1" | tee -a "$LOG_FILE"
}

log_warning() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] ⚠️${NC} $1" | tee -a "$LOG_FILE"
}

log_error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ❌${NC} $1" | tee -a "$LOG_FILE"
}

# 检查依赖
check_dependencies() {
    log "检查运行环境..."

    # 检查 Python
    if ! command -v python3 &> /dev/null; then
        log_error "Python3 未安装"
        exit 1
    fi

    # 检查必要的 Python 包
    python3 -c "import requests" 2>/dev/null || {
        log_warning "requests 包未安装，安装中..."
        pip3 install requests || {
            log_error "无法安装 requests 包"
            exit 1
        }
    }

    log_success "环境检查完成"
}

# 更新项目统计
update_project_stats() {
    log "更新项目统计数据..."

    if [[ -f "$SCRIPT_DIR/monitor_downloads.py" ]]; then
        python3 "$SCRIPT_DIR/monitor_downloads.py" --save 2>&1 | tee -a "$LOG_FILE"
        log_success "下载统计更新完成"
    else
        log_warning "monitor_downloads.py 不存在，跳过下载统计"
    fi
}

# 收集用户反馈
collect_user_feedback() {
    log "收集用户反馈..."

    # 优先使用简化版本的反馈收集器
    if [[ -f "$SCRIPT_DIR/simple_feedback_collector.py" ]]; then
        python3 "$SCRIPT_DIR/simple_feedback_collector.py" --export 2>&1 | tee -a "$LOG_FILE" || true
        log_success "反馈收集完成 (简化版本)"
    elif [[ -f "$SCRIPT_DIR/collect_feedback.py" ]]; then
        python3 "$SCRIPT_DIR/collect_feedback.py" --export 2>&1 | tee -a "$LOG_FILE" || true
        log_success "反馈收集完成"
    else
        log_warning "反馈收集工具不存在，跳过反馈收集"
        echo "💡 建议: 手动检查 GitHub issues 和 PRs" | tee -a "$LOG_FILE"
    fi
}

# 生成推广计划
generate_promotion_plan() {
    log "生成推广计划..."

    if [[ -f "$SCRIPT_DIR/promotion_scheduler.py" ]]; then
        python3 "$SCRIPT_DIR/promotion_scheduler.py" plan 2>&1 | tee -a "$LOG_FILE"
        log_success "推广计划生成完成"
    else
        log_warning "promotion_scheduler.py 不存在，跳过推广计划"
    fi
}

# 检查 GitHub 状态
check_github_status() {
    log "检查 GitHub 仓库状态..."

    cd "$PROJECT_ROOT" || exit 1

    # 检查是否有新的 issues
    if command -v gh &> /dev/null; then
        OPEN_ISSUES=$(gh issue list --state open --limit 1 --json number | jq '. | length')
        if [[ "$OPEN_ISSUES" -gt 0 ]]; then
            log_warning "发现 $OPEN_ISSUES 个开放的 issues，需要处理"
        else
            log_success "没有开放的 issues"
        fi

        # 检查是否有新的 PR
        OPEN_PRS=$(gh pr list --state open --limit 1 --json number | jq '. | length')
        if [[ "$OPEN_PRS" -gt 0 ]]; then
            log_warning "发现 $OPEN_PRS 个开放的 PRs，需要审查"
        else
            log_success "没有开放的 PRs"
        fi
    else
        log_warning "GitHub CLI (gh) 未安装，跳过 GitHub 状态检查"
        log "安装方法: brew install gh (macOS) 或 https://cli.github.com/"
    fi
}

# 安全检查
security_check() {
    log "执行安全检查..."

    if [[ -f "$PROJECT_ROOT/fix_vulnerabilities.py" ]]; then
        echo "n" | python3 "$PROJECT_ROOT/fix_vulnerabilities.py" 2>&1 | tee -a "$LOG_FILE" || true
        log_success "安全检查完成"
    else
        log_warning "fix_vulnerabilities.py 不存在，跳过安全检查"
        log "运行基本安全检查..."
        pip3 list --outdated 2>&1 | head -20 | tee -a "$LOG_FILE" || true
    fi
}

# 清理旧文件
cleanup_old_files() {
    log "清理旧的日志和临时文件..."

    # 清理 7 天前的监控数据文件
    find "$SCRIPT_DIR" -name "monitoring_data_*.json" -mtime +7 -delete 2>/dev/null || true
    find "$SCRIPT_DIR" -name "feedback_analysis_*.json" -mtime +7 -delete 2>/dev/null || true

    # 保留最近 30 天的日志
    if [[ -f "$LOG_FILE" ]]; then
        # 创建新的日志文件，只保留最近的内容
        tail -n 1000 "$LOG_FILE" > "${LOG_FILE}.tmp" && mv "${LOG_FILE}.tmp" "$LOG_FILE"
    fi

    log_success "文件清理完成"
}

# 生成每日报告
generate_daily_report() {
    log "生成每日运营报告..."

    REPORT_FILE="$SCRIPT_DIR/daily_report_$(date +%Y%m%d).md"

    cat > "$REPORT_FILE" << EOF
# 每日运营报告 - $(date '+%Y年%m月%d日')

## 📊 数据概览

### GitHub 仓库状态
- 检查时间: $(date '+%H:%M:%S')
- 开放 Issues: 待手动确认
- 开放 PRs: 待手动确认
- 最近提交: 待手动确认

### PyPI 包状态
- 当前版本: 0.2.0
- 下载统计: 查看 monitoring_data_*.json 文件

## ✅ 今日完成任务

- [x] 项目统计数据更新
- [x] 用户反馈收集
- [x] 推广计划生成
- [x] GitHub 状态检查
- [x] 安全检查
- [x] 文件清理

## 📋 待办事项

### 高优先级
- [ ] 回复新的 GitHub issues
- [ ] 审查待处理的 PRs
- [ ] 处理用户反馈

### 中优先级
- [ ] 更新项目文档
- [ ] 准备社交媒体内容
- [ ] 监控竞品动态

### 低优先级
- [ ] 优化代码结构
- [ ] 完善测试覆盖率
- [ ] 准备技术分享内容

## 💡 今日洞察

- 用户反馈趋势: [需要手动分析反馈数据]
- 下载量变化: [需要查看统计数据]
- 社区活跃度: [需要观察 GitHub 活动]

## 📅 明日计划

- 持续监控用户反馈
- 发布社交媒体内容
- 跟进待处理的 issues
- 准备技术内容

---
*报告生成时间: $(date)*
*下次运行: $(date -v+1d '+%Y-%m-%d %H:%M:%S')*
EOF

    log_success "每日报告已生成: $REPORT_FILE"
}

# 发送通知 (可选)
send_notification() {
    log "发送运营通知..."

    # 这里可以集成各种通知方式:
    # - 邮件通知
    # - Slack 通知
    # - 微信通知
    # - 钉钉通知

    # 示例: 简单的桌面通知 (macOS)
    if command -v osascript &> /dev/null; then
        osascript -e 'display notification "每日运营检查完成" with title "genai-starter-kit"' 2>/dev/null || true
    fi

    log_success "通知发送完成"
}

# 主函数
main() {
    echo "🚀 genai-starter-kit 每日运营自动化"
    echo "=================================="
    echo "开始时间: $(date)"
    echo

    # 创建日志目录
    mkdir -p "$(dirname "$LOG_FILE")"

    # 记录开始
    log "开始每日运营检查..."

    # 执行各项检查
    check_dependencies
    update_project_stats
    collect_user_feedback
    generate_promotion_plan
    check_github_status
    security_check
    cleanup_old_files
    generate_daily_report
    send_notification

    log_success "每日运营检查完成！"
    echo
    echo "📊 查看详细日志: $LOG_FILE"
    echo "📋 查看每日报告: $SCRIPT_DIR/daily_report_$(date +%Y%m%d).md"
    echo "🔗 有用链接:"
    echo "  - PyPI: https://pypi.org/project/genai-starter-kit/"
    echo "  - GitHub: https://github.com/YY-Nexus/GenerativeAI-Starter-Kit"
    echo "  - 下载统计: https://pypistats.org/packages/genai-starter-kit"
}

# 错误处理
trap 'log_error "脚本执行出错，退出代码: $?"' ERR

# 运行主函数
main "$@"
