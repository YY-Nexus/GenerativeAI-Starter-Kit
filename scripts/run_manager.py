#!/usr/bin/env python3
"""
一键脚本管理器 - 统一管理所有后续运营工具
完全无类型检查问题
"""

import os
import sys

def show_menu():
    """显示功能菜单"""
    print("🚀 GenerativeAI-Starter-Kit 后续运营工具")
    print("=" * 50)
    print("1. 快速项目状态检查 (推荐)")
    print("2. 详细反馈分析 (需要 requests)")
    print("3. 下载统计监控 (需要 requests)")  
    print("4. 推广计划制定")
    print("5. 简化反馈收集")
    print("6. 零错误状态监控")
    print("0. 退出")
    print("=" * 50)

def run_script(script_name):
    """运行指定脚本"""
    script_path = f"scripts/{script_name}"
    if os.path.exists(script_path):
        print(f"\n🔧 运行 {script_name}...")
        print("-" * 30)
        os.system(f"python {script_path}")
        print("-" * 30)
        print("✅ 运行完成\n")
    else:
        print(f"❌ 脚本 {script_name} 不存在")

def main():
    """主程序"""
    while True:
        show_menu()
        try:
            choice = input("请选择功能 (0-6): ").strip()
            
            if choice == "0":
                print("👋 再见！")
                break
            elif choice == "1":
                run_script("quick_feedback_check.py")
            elif choice == "2":
                run_script("collect_feedback.py")
            elif choice == "3":
                run_script("monitor_downloads.py")
            elif choice == "4":
                run_script("promotion_scheduler.py")
            elif choice == "5":
                run_script("simple_feedback_collector.py")
            elif choice == "6":
                run_script("zero_error_monitor.py")
            else:
                print("❌ 无效选择，请输入 0-6")
                
        except KeyboardInterrupt:
            print("\n\n👋 程序已退出")
            break
        except Exception as e:
            print(f"❌ 出错了: {e}")
            
        input("\n按回车键继续...")

if __name__ == "__main__":
    main()