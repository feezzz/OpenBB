#!/usr/bin/env python3
"""
加密货币数据分析演示程序 - Gate.io API 版本
============================================

这个程序使用 Gate.io API 获取真实的加密货币数据，专注于核心功能：
- 使用 Gate.io API 获取 BTC 和 ETH 历史价格数据
- 创建专业的价格对比图表
- 显示最新价格信息和技术分析

主要特性：
- 优先使用 Gate.io API 作为数据源
- 支持多种数据源备用方案
- 完整的中文注释和错误处理
- 专业的金融图表展示

作者: 加密货币分析演示项目
日期: 2024年
"""

import sys
import os
from datetime import datetime, timedelta

# 添加当前目录到路径，以便导入 gateio_api 模块
sys.path.insert(0, os.path.dirname(__file__))

# 添加 OpenBB 路径（备用数据源）
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'openbb_platform'))

try:
    # 导入必要的库
    import pandas as pd
    import matplotlib.pyplot as plt
    import matplotlib.dates as mdates
    import numpy as np

    # 导入 Gate.io API 模块
    from gateio_api import GateIOAPI

    # 尝试导入 OpenBB 作为备用数据源
    try:
        from openbb import obb
        openbb_available = True
        print("✅ OpenBB 备用数据源可用")
    except ImportError:
        openbb_available = False
        print("⚠️  OpenBB 备用数据源不可用")

    print("✅ 所有必要依赖项导入成功")

except ImportError as e:
    print(f"❌ 导入失败: {e}")
    print("请确保安装了必要的包: pip install pandas matplotlib numpy requests")
    sys.exit(1)


def get_crypto_data():
    """
    获取加密货币数据

    优先使用 Gate.io API，如果失败则尝试备用数据源

    Returns:
        tuple: (btc_df, eth_df) 包含比特币和以太坊数据的 DataFrame，失败时返回 (None, None)
    """
    print("📊 正在获取加密货币数据...")

    # 计算日期范围（最近3个月）
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)

    start_str = start_date.strftime("%Y-%m-%d")
    end_str = end_date.strftime("%Y-%m-%d")

    print(f"📅 数据期间: {start_str} 到 {end_str}")

    # 方法1: 优先尝试 Gate.io API
    try:
        print("🚀 尝试使用 Gate.io API（优先数据源）...")

        # 创建 Gate.io API 客户端
        gateio_api = GateIOAPI()

        # 测试连接
        if not gateio_api.test_connection():
            raise Exception("Gate.io API 连接测试失败")

        # 获取比特币历史数据
        print("🔄 从 Gate.io 获取比特币数据...")
        btc_df = gateio_api.get_historical_data(
            symbol='BTC_USDT',
            interval='1d',
            start_date=start_str,
            end_date=end_str
        )

        # 获取以太坊历史数据
        print("🔄 从 Gate.io 获取以太坊数据...")
        eth_df = gateio_api.get_historical_data(
            symbol='ETH_USDT',
            interval='1d',
            start_date=start_str,
            end_date=end_str
        )

        # 检查数据有效性
        if len(btc_df) > 0 and len(eth_df) > 0:
            print(f"✅ Gate.io API 数据获取成功:")
            print(f"   BTC: {len(btc_df)} 个数据点")
            print(f"   ETH: {len(eth_df)} 个数据点")

            # 获取最新价格信息
            try:
                btc_ticker = gateio_api.get_ticker('BTC_USDT')
                eth_ticker = gateio_api.get_ticker('ETH_USDT')
                print(f"   BTC 当前价格: ${btc_ticker['price']:,.2f}")
                print(f"   ETH 当前价格: ${eth_ticker['price']:,.2f}")
            except Exception as e:
                print(f"⚠️  获取实时价格失败: {e}")

            return btc_df, eth_df
        else:
            raise Exception("Gate.io API 返回空数据")

    except Exception as e:
        print(f"⚠️  Gate.io API 失败: {e}")
        print("🔄 尝试备用数据源...")

    # 方法2: 备用数据源 - OpenBB
    if openbb_available:
        try:
            print("🔄 尝试使用 OpenBB 备用数据源...")

            # 尝试多个 OpenBB 提供商
            providers = ["yfinance", "fmp"]

            for provider in providers:
                try:
                    print(f"🔄 尝试 OpenBB {provider} 提供商...")

                    # 获取比特币数据
                    btc_data = obb.crypto.price.historical(
                        symbol="BTC-USD" if provider == "yfinance" else "BTCUSD",
                        start_date=start_str,
                        end_date=end_str,
                        provider=provider
                    )

                    # 获取以太坊数据
                    eth_data = obb.crypto.price.historical(
                        symbol="ETH-USD" if provider == "yfinance" else "ETHUSD",
                        start_date=start_str,
                        end_date=end_str,
                        provider=provider
                    )

                    # 转换为 DataFrame
                    btc_df = btc_data.to_dataframe()
                    eth_df = eth_data.to_dataframe()

                    # 检查数据有效性
                    if len(btc_df) > 0 and len(eth_df) > 0:
                        print(f"✅ OpenBB {provider} 数据获取成功:")
                        print(f"   BTC: {len(btc_df)} 个数据点")
                        print(f"   ETH: {len(eth_df)} 个数据点")
                        return btc_df, eth_df
                    else:
                        print(f"⚠️  {provider} 返回空数据，尝试下一个提供商...")
                        continue

                except Exception as e:
                    print(f"⚠️  OpenBB {provider} 提供商失败: {e}")
                    continue

        except Exception as e:
            print(f"⚠️  OpenBB 备用数据源失败: {e}")

    # 所有数据源都失败
    print("❌ 所有数据源都失败，无法获取数据")
    print("💡 建议:")
    print("   1. 检查网络连接")
    print("   2. 稍后重试")
    print("   3. 运行离线版本: python crypto_demo_offline.py")

    return None, None


def create_simple_chart(btc_df, eth_df):
    """
    创建简单的价格对比图表

    Args:
        btc_df: 比特币价格数据 DataFrame
        eth_df: 以太坊价格数据 DataFrame

    Returns:
        bool: 图表创建是否成功
    """
    print("📊 正在创建专业金融图表...")

    try:
        # 设置中文字体支持
        plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS']
        plt.rcParams['axes.unicode_minus'] = False

        # 创建双子图布局
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(14, 10))
        fig.suptitle('BTC vs ETH 价格分析 - 基于 Gate.io 数据', fontsize=16, fontweight='bold')

        # 获取最新价格数据
        btc_latest = btc_df['close'].iloc[-1]
        eth_latest = eth_df['close'].iloc[-1]

        # 计算24小时价格变化百分比
        btc_change = (btc_latest - btc_df['close'].iloc[-2]) / btc_df['close'].iloc[-2] * 100
        eth_change = (eth_latest - eth_df['close'].iloc[-2]) / eth_df['close'].iloc[-2] * 100

        # === 图表1: 绝对价格走势对比 ===
        # 绘制主要价格线
        ax1.plot(btc_df.index, btc_df['close'],
                label=f'BTC (${btc_latest:,.0f}, {btc_change:+.1f}%)',
                color='#f7931a', linewidth=2.5, alpha=0.9)
        ax1.plot(eth_df.index, eth_df['close'],
                label=f'ETH (${eth_latest:,.0f}, {eth_change:+.1f}%)',
                color='#627eea', linewidth=2.5, alpha=0.9)

        # 计算并绘制移动平均线
        btc_ma20 = btc_df['close'].rolling(20).mean()
        eth_ma20 = eth_df['close'].rolling(20).mean()
        btc_ma50 = btc_df['close'].rolling(50).mean()
        eth_ma50 = eth_df['close'].rolling(50).mean()

        # 20日移动平均线
        ax1.plot(btc_df.index, btc_ma20,
                color='#f7931a', alpha=0.6, linestyle='--', linewidth=1.5, label='BTC MA(20)')
        ax1.plot(eth_df.index, eth_ma20,
                color='#627eea', alpha=0.6, linestyle='--', linewidth=1.5, label='ETH MA(20)')

        # 50日移动平均线（如果数据足够）
        if len(btc_df) >= 50:
            ax1.plot(btc_df.index, btc_ma50,
                    color='#f7931a', alpha=0.4, linestyle=':', linewidth=1.5, label='BTC MA(50)')
            ax1.plot(eth_df.index, eth_ma50,
                    color='#627eea', alpha=0.4, linestyle=':', linewidth=1.5, label='ETH MA(50)')

        # 设置图表1属性
        ax1.set_title('价格走势对比 (绝对价格)', fontweight='bold', fontsize=12)
        ax1.set_ylabel('价格 (USDT)', fontsize=11)
        ax1.legend(loc='upper left', fontsize=9)
        ax1.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)

        # === 图表2: 标准化收益率对比 ===
        # 计算标准化收益率（以期初价格为基准）
        btc_normalized = (btc_df['close'] / btc_df['close'].iloc[0] - 1) * 100
        eth_normalized = (eth_df['close'] / eth_df['close'].iloc[0] - 1) * 100

        # 绘制标准化收益率线
        ax2.plot(btc_df.index, btc_normalized,
                label=f'BTC 累计收益 ({btc_normalized.iloc[-1]:+.1f}%)',
                color='#f7931a', linewidth=2.5, alpha=0.9)
        ax2.plot(eth_df.index, eth_normalized,
                label=f'ETH 累计收益 ({eth_normalized.iloc[-1]:+.1f}%)',
                color='#627eea', linewidth=2.5, alpha=0.9)

        # 添加零基准线
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.5, linewidth=1)

        # 添加收益区间着色
        ax2.fill_between(btc_df.index, 0, btc_normalized,
                        where=(btc_normalized >= 0), color='#f7931a', alpha=0.1, interpolate=True)
        ax2.fill_between(btc_df.index, 0, btc_normalized,
                        where=(btc_normalized < 0), color='red', alpha=0.1, interpolate=True)

        # 设置图表2属性
        ax2.set_title('标准化收益率对比 (期初价格 = 0%)', fontweight='bold', fontsize=12)
        ax2.set_ylabel('累计收益率 (%)', fontsize=11)
        ax2.set_xlabel('日期', fontsize=11)
        ax2.legend(loc='upper left', fontsize=9)
        ax2.grid(True, alpha=0.3, linestyle='-', linewidth=0.5)

        # === 格式化日期轴 ===
        for ax in [ax1, ax2]:
            # 设置日期格式
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
            ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))

            # 旋转日期标签以避免重叠
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45, ha='right')

            # 设置坐标轴样式
            ax.tick_params(axis='both', which='major', labelsize=9)
            ax.spines['top'].set_visible(False)
            ax.spines['right'].set_visible(False)

        # 调整布局以避免重叠
        plt.tight_layout()

        # 添加数据来源标注
        fig.text(0.02, 0.02, f'数据来源: Gate.io API | 生成时间: {datetime.now().strftime("%Y-%m-%d %H:%M")}',
                fontsize=8, alpha=0.7)

        print("✅ 专业金融图表创建完成")
        return True

    except Exception as e:
        print(f"❌ 图表创建失败: {e}")
        import traceback
        traceback.print_exc()
        return False


def print_summary(btc_df, eth_df):
    """
    打印详细的数据分析摘要

    Args:
        btc_df: 比特币价格数据 DataFrame
        eth_df: 以太坊价格数据 DataFrame
    """
    print("\n" + "="*70)
    print("📊 加密货币市场数据分析摘要 - 基于 Gate.io 实时数据")
    print("="*70)

    try:
        # === 比特币 (BTC) 详细分析 ===
        btc_latest = btc_df.iloc[-1]
        btc_change = (btc_latest['close'] - btc_df['close'].iloc[-2]) / btc_df['close'].iloc[-2] * 100

        # 计算比特币技术指标
        btc_high_period = btc_df['high'].max()
        btc_low_period = btc_df['low'].min()
        btc_avg_volume = btc_df['volume'].mean()
        btc_volatility = btc_df['close'].pct_change().std() * np.sqrt(365) * 100  # 年化波动率

        print(f"🟠 比特币 (BTC) 市场分析:")
        print(f"   💰 当前价格: ${btc_latest['close']:,.2f} USDT")
        print(f"   📈 24小时变化: {btc_change:+.2f}%")
        print(f"   📊 24小时最高: ${btc_latest['high']:,.2f} USDT")
        print(f"   📉 24小时最低: ${btc_latest['low']:,.2f} USDT")
        print(f"   📦 24小时成交量: {btc_latest['volume']:,.0f} BTC")
        print(f"   🎯 期间最高价: ${btc_high_period:,.2f} USDT")
        print(f"   🎯 期间最低价: ${btc_low_period:,.2f} USDT")
        print(f"   📊 平均日成交量: {btc_avg_volume:,.0f} BTC")
        print(f"   📈 年化波动率: {btc_volatility:.1f}%")

        # === 以太坊 (ETH) 详细分析 ===
        eth_latest = eth_df.iloc[-1]
        eth_change = (eth_latest['close'] - eth_df['close'].iloc[-2]) / eth_df['close'].iloc[-2] * 100

        # 计算以太坊技术指标
        eth_high_period = eth_df['high'].max()
        eth_low_period = eth_df['low'].min()
        eth_avg_volume = eth_df['volume'].mean()
        eth_volatility = eth_df['close'].pct_change().std() * np.sqrt(365) * 100  # 年化波动率

        print(f"\n🔵 以太坊 (ETH) 市场分析:")
        print(f"   💰 当前价格: ${eth_latest['close']:,.2f} USDT")
        print(f"   📈 24小时变化: {eth_change:+.2f}%")
        print(f"   📊 24小时最高: ${eth_latest['high']:,.2f} USDT")
        print(f"   📉 24小时最低: ${eth_latest['low']:,.2f} USDT")
        print(f"   📦 24小时成交量: {eth_latest['volume']:,.0f} ETH")
        print(f"   🎯 期间最高价: ${eth_high_period:,.2f} USDT")
        print(f"   🎯 期间最低价: ${eth_low_period:,.2f} USDT")
        print(f"   📊 平均日成交量: {eth_avg_volume:,.0f} ETH")
        print(f"   📈 年化波动率: {eth_volatility:.1f}%")

        # === 市场关系分析 ===
        print(f"\n📊 市场关系与技术分析:")

        # 计算价格相关性
        btc_returns = btc_df['close'].pct_change().dropna()
        eth_returns = eth_df['close'].pct_change().dropna()
        correlation = btc_returns.corr(eth_returns)

        print(f"   🔗 BTC-ETH 价格相关性: {correlation:.3f}")

        # 相关性解释
        if correlation > 0.7:
            correlation_desc = "强正相关 - 两者价格走势高度一致"
        elif correlation > 0.3:
            correlation_desc = "中等正相关 - 两者价格走势较为一致"
        elif correlation > -0.3:
            correlation_desc = "弱相关 - 两者价格走势相对独立"
        else:
            correlation_desc = "负相关 - 两者价格走势相反"

        print(f"   📈 相关性解释: {correlation_desc}")

        # 计算累计收益率
        btc_total_return = (btc_latest['close'] / btc_df['close'].iloc[0] - 1) * 100
        eth_total_return = (eth_latest['close'] / eth_df['close'].iloc[0] - 1) * 100

        print(f"   📊 BTC 期间累计收益: {btc_total_return:+.2f}%")
        print(f"   📊 ETH 期间累计收益: {eth_total_return:+.2f}%")

        # 表现对比
        if btc_total_return > eth_total_return:
            better_performer = "BTC 表现更佳"
        elif eth_total_return > btc_total_return:
            better_performer = "ETH 表现更佳"
        else:
            better_performer = "两者表现相当"

        print(f"   🏆 期间表现对比: {better_performer}")

        # === 数据统计信息 ===
        print(f"\n📋 数据统计信息:")
        print(f"   📅 数据期间: {btc_df.index[0].strftime('%Y-%m-%d')} 至 {btc_df.index[-1].strftime('%Y-%m-%d')}")
        print(f"   � 数据点数量: {len(btc_df)} 天")
        print(f"   🔄 最后更新: {btc_latest.name.strftime('%Y-%m-%d %H:%M') if hasattr(btc_latest.name, 'strftime') else btc_latest.name}")
        print(f"   🌐 数据来源: Gate.io API")

        print("="*70)

    except Exception as e:
        print(f"❌ 数据摘要生成失败: {e}")
        import traceback
        traceback.print_exc()


def main():
    """
    主程序入口

    执行完整的加密货币数据分析流程：
    1. 获取 Gate.io API 数据
    2. 生成详细分析摘要
    3. 创建专业图表
    4. 保存和显示结果

    Returns:
        bool: 程序执行是否成功
    """
    print("🚀 加密货币数据分析演示程序 - Gate.io API 版本")
    print("=" * 65)
    print("📊 本程序使用 Gate.io API 获取实时加密货币数据进行专业分析")
    print("🎯 分析目标: BTC (比特币) 和 ETH (以太坊) 价格走势对比")
    print("=" * 65)

    try:
        # === 步骤1: 数据获取 ===
        print("\n📊 步骤 1: 获取加密货币市场数据")
        print("-" * 40)

        btc_df, eth_df = get_crypto_data()
        if btc_df is None or eth_df is None:
            print("❌ 无法获取数据，程序退出")
            print("\n💡 建议解决方案:")
            print("   1. 检查网络连接")
            print("   2. 稍后重试")
            print("   3. 运行离线版本: python crypto_demo_offline.py")
            return False

        # === 步骤2: 数据分析 ===
        print("\n📋 步骤 2: 生成市场分析摘要")
        print("-" * 40)

        print_summary(btc_df, eth_df)

        # === 步骤3: 图表创建 ===
        print("\n📊 步骤 3: 创建专业金融图表")
        print("-" * 40)

        if create_simple_chart(btc_df, eth_df):
            # === 步骤4: 保存图表 ===
            print("\n💾 步骤 4: 保存分析结果")
            print("-" * 40)

            try:
                # 生成带时间戳的文件名
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = f"crypto_gateio_analysis_{timestamp}.png"

                plt.savefig(filename, dpi=300, bbox_inches='tight',
                           facecolor='white', edgecolor='none')
                print(f"✅ 高分辨率图表已保存为: {filename}")

                # 同时保存一个通用名称的副本
                plt.savefig("crypto_gateio_analysis.png", dpi=300, bbox_inches='tight',
                           facecolor='white', edgecolor='none')
                print("✅ 图表副本已保存为: crypto_gateio_analysis.png")

            except Exception as e:
                print(f"⚠️  图表保存失败: {e}")

            # === 步骤5: 显示图表 ===
            print("\n🖼️  步骤 5: 显示交互式图表")
            print("-" * 40)
            print("📌 图表功能说明:")
            print("   • 可以缩放和平移查看细节")
            print("   • 鼠标悬停查看数据点")
            print("   • 使用工具栏保存或调整图表")
            print("\n💡 提示: 关闭图表窗口以结束程序")

            # 显示交互式图表
            plt.show()
        else:
            print("❌ 图表创建失败，但数据分析已完成")
            return False

        # === 程序完成 ===
        print("\n" + "=" * 65)
        print("🎉 程序执行完成! 感谢使用加密货币数据分析工具")
        print("=" * 65)
        print("📊 本次分析基于 Gate.io 实时数据")
        print("💡 如需更多功能，请尝试完整版: python crypto_demo.py")
        print("🔄 如需离线演示，请运行: python crypto_demo_offline.py")

        return True

    except Exception as e:
        print(f"\n❌ 程序执行过程中发生错误: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    """程序入口点"""
    try:
        # 执行主程序
        success = main()

        # 根据执行结果设置退出码
        sys.exit(0 if success else 1)

    except KeyboardInterrupt:
        # 用户中断程序（Ctrl+C）
        print("\n⚠️  程序被用户中断")
        print("👋 感谢使用，再见!")
        sys.exit(1)

    except Exception as e:
        # 未预期的错误
        print(f"\n❌ 程序启动失败: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
