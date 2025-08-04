#!/usr/bin/env python3
"""
OpenBB 加密货币演示程序启动器
============================

这个脚本提供了一个交互式菜单来选择运行不同版本的演示程序。

作者: OpenBB 演示
日期: 2024年
"""

import sys
import os
import subprocess

def print_banner():
    """打印程序横幅"""
    print("=" * 60)
    print("🚀 OpenBB 加密货币数据分析演示程序启动器")
    print("=" * 60)
    print()

def print_menu():
    """打印菜单选项"""
    print("请选择要运行的演示程序:")
    print()
    print("1. 🎯 离线版 (快速体验) - 使用模拟数据，展示完整功能")
    print("   - ✅ 无需网络连接")
    print("   - ✅ 无需API密钥")
    print("   - ✅ 包含完整的技术分析功能")
    print("   - ✅ 4个专业分析图表")
    print()
    print("2. 🚀 Gate.io API 版 (推荐) - 获取真实数据，专业分析")
    print("   - ✅ 使用 Gate.io 实时数据")
    print("   - ✅ 无需API密钥注册")
    print("   - ✅ 2个专业金融图表")
    print("   - ⚠️  需要网络连接")
    print()
    print("3. 🔧 完整版 - 多数据源，高级功能")
    print("   - ⚠️  需要网络连接")
    print("   - ⚠️  可能需要API密钥")
    print("   - ✅ 4个高级分析图表")
    print("   - ✅ 完整技术指标")
    print()
    print("4. 📖 查看说明文档")
    print("5. 🚪 退出")
    print()

def run_program(script_name):
    """运行指定的程序"""
    try:
        print(f"🔄 正在启动 {script_name}...")
        print("-" * 40)
        
        # 检查文件是否存在
        if not os.path.exists(script_name):
            print(f"❌ 错误: 找不到文件 {script_name}")
            return False
        
        # 运行程序
        result = subprocess.run([sys.executable, script_name], 
                              cwd=os.getcwd(),
                              capture_output=False)
        
        print("-" * 40)
        if result.returncode == 0:
            print(f"✅ {script_name} 执行完成")
        else:
            print(f"⚠️  {script_name} 执行结束 (返回码: {result.returncode})")
        
        return True
        
    except KeyboardInterrupt:
        print("\n⚠️  程序被用户中断")
        return True
    except Exception as e:
        print(f"❌ 运行 {script_name} 时出错: {e}")
        return False

def show_documentation():
    """显示文档内容"""
    doc_file = "README_CRYPTO_DEMO.md"
    
    if os.path.exists(doc_file):
        print("📖 OpenBB 加密货币演示程序说明文档")
        print("=" * 50)
        
        try:
            with open(doc_file, 'r', encoding='utf-8') as f:
                content = f.read()
                # 只显示前50行，避免输出过长
                lines = content.split('\n')[:50]
                print('\n'.join(lines))
                
                if len(content.split('\n')) > 50:
                    print("\n... (文档内容较长，请查看完整的 README_CRYPTO_DEMO.md 文件)")
                    
        except Exception as e:
            print(f"❌ 读取文档失败: {e}")
    else:
        print("❌ 找不到说明文档文件")
    
    print("\n" + "=" * 50)

def check_dependencies():
    """检查依赖项"""
    print("🔍 检查依赖项...")
    
    required_packages = ['pandas', 'matplotlib', 'numpy']
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"  ✅ {package}")
        except ImportError:
            missing_packages.append(package)
            print(f"  ❌ {package}")
    
    if missing_packages:
        print(f"\n⚠️  缺少必要的包: {', '.join(missing_packages)}")
        print("请运行: pip install pandas matplotlib numpy")
        return False
    
    print("✅ 所有依赖项检查通过")
    return True

def main():
    """主程序"""
    print_banner()
    
    # 检查依赖项
    if not check_dependencies():
        print("\n❌ 依赖项检查失败，程序退出")
        return False
    
    print()
    
    while True:
        print_menu()
        
        try:
            choice = input("请输入选项 (1-5): ").strip()
            
            if choice == '1':
                print("\n🎯 启动离线版演示程序...")
                print("📊 使用模拟数据展示完整分析功能")
                run_program("crypto_demo_offline.py")

            elif choice == '2':
                print("\n🚀 启动 Gate.io API 版演示程序...")
                print("📊 使用 Gate.io 实时数据进行专业分析")
                print("✅ 无需注册 API 密钥，直接获取真实市场数据")
                confirm = input("是否继续? (Y/n): ").strip().lower()
                if confirm in ['', 'y', 'yes']:
                    run_program("crypto_demo_simple.py")
                else:
                    print("已取消")

            elif choice == '3':
                print("\n🔧 启动完整版演示程序...")
                print("⚠️  注意: 此版本需要网络连接，可能需要额外的API密钥")
                confirm = input("是否继续? (y/N): ").strip().lower()
                if confirm in ['y', 'yes']:
                    run_program("crypto_demo.py")
                else:
                    print("已取消")
                    
            elif choice == '4':
                print()
                show_documentation()
                
            elif choice == '5':
                print("\n👋 感谢使用 OpenBB 加密货币演示程序!")
                break
                
            else:
                print("❌ 无效选项，请输入 1-5")
            
            print()
            input("按 Enter 键继续...")
            print()
            
        except KeyboardInterrupt:
            print("\n\n👋 程序被用户中断，再见!")
            break
        except Exception as e:
            print(f"\n❌ 发生错误: {e}")
            print("请重试...")
    
    return True

if __name__ == "__main__":
    try:
        success = main()
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"\n❌ 程序启动失败: {e}")
        sys.exit(1)
