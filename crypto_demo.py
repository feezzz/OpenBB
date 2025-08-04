#!/usr/bin/env python3
"""
OpenBB 加密货币数据分析演示程序
=================================

这个程序演示如何使用 OpenBB 平台获取和分析加密货币数据，
包括价格走势对比、技术指标分析和交互式图表展示。

作者: OpenBB 演示
日期: 2024年
"""

import sys
import os
import warnings
from datetime import datetime, timedelta
from typing import Optional, Tuple, Dict, Any

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.patches import Rectangle
import numpy as np

# 添加 OpenBB 路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'openbb_platform'))

# 抑制警告
warnings.filterwarnings('ignore')

try:
    from openbb import obb
    print("✅ OpenBB 导入成功")
except ImportError as e:
    print(f"❌ OpenBB 导入失败: {e}")
    print("请确保您在 OpenBB 项目目录中运行此脚本")
    sys.exit(1)


class CryptoAnalyzer:
    """加密货币数据分析器"""
    
    def __init__(self):
        """初始化分析器"""
        self.btc_data = None
        self.eth_data = None
        self.btc_df = None
        self.eth_df = None
        
        # 设置中文字体支持
        plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS']
        plt.rcParams['axes.unicode_minus'] = False
        
        # 设置图表样式
        plt.style.use('seaborn-v0_8' if 'seaborn-v0_8' in plt.style.available else 'default')
    
    def fetch_crypto_data(self, months: int = 6) -> bool:
        """
        获取加密货币历史数据
        
        Args:
            months: 获取最近几个月的数据
            
        Returns:
            bool: 是否成功获取数据
        """
        try:
            # 计算日期范围
            end_date = datetime.now()
            start_date = end_date - timedelta(days=months * 30)
            
            start_str = start_date.strftime("%Y-%m-%d")
            end_str = end_date.strftime("%Y-%m-%d")
            
            print(f"📊 获取数据期间: {start_str} 到 {end_str}")
            
            # 获取比特币数据
            print("🔄 正在获取比特币数据...")
            self.btc_data = obb.crypto.price.historical(
                symbol="BTC-USD",
                start_date=start_str,
                end_date=end_str,
                provider="yfinance"
            )
            
            # 获取以太坊数据
            print("🔄 正在获取以太坊数据...")
            self.eth_data = obb.crypto.price.historical(
                symbol="ETH-USD",
                start_date=start_str,
                end_date=end_str,
                provider="yfinance"
            )
            
            # 转换为 DataFrame
            self.btc_df = self.btc_data.to_dataframe()
            self.eth_df = self.eth_data.to_dataframe()
            
            print(f"✅ 成功获取数据:")
            print(f"   BTC: {len(self.btc_df)} 个数据点")
            print(f"   ETH: {len(self.eth_df)} 个数据点")
            
            return True
            
        except Exception as e:
            print(f"❌ 获取数据失败: {e}")
            return False
    
    def calculate_technical_indicators(self) -> bool:
        """
        计算技术指标
        
        Returns:
            bool: 是否成功计算指标
        """
        try:
            print("🔄 正在计算技术指标...")
            
            # 为 BTC 和 ETH 计算移动平均线
            for df, name in [(self.btc_df, "BTC"), (self.eth_df, "ETH")]:
                # 简单移动平均线
                df['SMA_20'] = df['close'].rolling(window=20).mean()
                df['SMA_50'] = df['close'].rolling(window=50).mean()
                
                # 指数移动平均线
                df['EMA_12'] = df['close'].ewm(span=12).mean()
                df['EMA_26'] = df['close'].ewm(span=26).mean()
                
                # MACD
                df['MACD'] = df['EMA_12'] - df['EMA_26']
                df['MACD_Signal'] = df['MACD'].ewm(span=9).mean()
                
                # RSI
                delta = df['close'].diff()
                gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
                loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
                rs = gain / loss
                df['RSI'] = 100 - (100 / (1 + rs))
                
                # 布林带
                df['BB_Middle'] = df['close'].rolling(window=20).mean()
                bb_std = df['close'].rolling(window=20).std()
                df['BB_Upper'] = df['BB_Middle'] + (bb_std * 2)
                df['BB_Lower'] = df['BB_Middle'] - (bb_std * 2)
            
            print("✅ 技术指标计算完成")
            return True
            
        except Exception as e:
            print(f"❌ 技术指标计算失败: {e}")
            return False
    
    def get_latest_info(self) -> Dict[str, Any]:
        """
        获取最新价格信息
        
        Returns:
            Dict: 包含最新价格信息的字典
        """
        try:
            btc_latest = self.btc_df.iloc[-1]
            eth_latest = self.eth_df.iloc[-1]
            
            # 计算价格变化
            btc_change = ((btc_latest['close'] - self.btc_df['close'].iloc[-2]) / 
                         self.btc_df['close'].iloc[-2] * 100)
            eth_change = ((eth_latest['close'] - self.eth_df['close'].iloc[-2]) / 
                         self.eth_df['close'].iloc[-2] * 100)
            
            return {
                'btc': {
                    'price': btc_latest['close'],
                    'change': btc_change,
                    'volume': btc_latest['volume'],
                    'high': btc_latest['high'],
                    'low': btc_latest['low'],
                    'rsi': btc_latest['RSI'] if 'RSI' in btc_latest else None
                },
                'eth': {
                    'price': eth_latest['close'],
                    'change': eth_change,
                    'volume': eth_latest['volume'],
                    'high': eth_latest['high'],
                    'low': eth_latest['low'],
                    'rsi': eth_latest['RSI'] if 'RSI' in eth_latest else None
                },
                'date': btc_latest.name
            }
            
        except Exception as e:
            print(f"❌ 获取最新信息失败: {e}")
            return {}

    def create_price_comparison_chart(self) -> bool:
        """
        创建价格对比图表

        Returns:
            bool: 是否成功创建图表
        """
        try:
            print("🔄 正在创建价格对比图表...")

            # 创建图表
            fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
            fig.suptitle('加密货币价格分析仪表板', fontsize=16, fontweight='bold')

            # 获取最新信息
            latest_info = self.get_latest_info()

            # 图表1: 价格走势对比
            ax1.plot(self.btc_df.index, self.btc_df['close'],
                    label=f'BTC (${latest_info.get("btc", {}).get("price", 0):,.0f})',
                    color='#f7931a', linewidth=2)
            ax1.plot(self.eth_df.index, self.eth_df['close'],
                    label=f'ETH (${latest_info.get("eth", {}).get("price", 0):,.0f})',
                    color='#627eea', linewidth=2)

            # 添加移动平均线
            ax1.plot(self.btc_df.index, self.btc_df['SMA_20'],
                    color='#f7931a', alpha=0.5, linestyle='--', label='BTC SMA(20)')
            ax1.plot(self.eth_df.index, self.eth_df['SMA_20'],
                    color='#627eea', alpha=0.5, linestyle='--', label='ETH SMA(20)')

            ax1.set_title('价格走势对比', fontweight='bold')
            ax1.set_ylabel('价格 (USD)')
            ax1.legend()
            ax1.grid(True, alpha=0.3)
            ax1.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
            ax1.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))

            # 图表2: 标准化价格对比（百分比变化）
            btc_normalized = (self.btc_df['close'] / self.btc_df['close'].iloc[0] - 1) * 100
            eth_normalized = (self.eth_df['close'] / self.eth_df['close'].iloc[0] - 1) * 100

            ax2.plot(self.btc_df.index, btc_normalized,
                    label=f'BTC ({btc_normalized.iloc[-1]:+.1f}%)',
                    color='#f7931a', linewidth=2)
            ax2.plot(self.eth_df.index, eth_normalized,
                    label=f'ETH ({eth_normalized.iloc[-1]:+.1f}%)',
                    color='#627eea', linewidth=2)

            ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
            ax2.set_title('标准化收益率对比', fontweight='bold')
            ax2.set_ylabel('收益率 (%)')
            ax2.legend()
            ax2.grid(True, alpha=0.3)
            ax2.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
            ax2.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))

            # 图表3: RSI 指标
            ax3.plot(self.btc_df.index, self.btc_df['RSI'],
                    label='BTC RSI', color='#f7931a', linewidth=2)
            ax3.plot(self.eth_df.index, self.eth_df['RSI'],
                    label='ETH RSI', color='#627eea', linewidth=2)

            # RSI 超买超卖线
            ax3.axhline(y=70, color='red', linestyle='--', alpha=0.7, label='超买线 (70)')
            ax3.axhline(y=30, color='green', linestyle='--', alpha=0.7, label='超卖线 (30)')
            ax3.fill_between(self.btc_df.index, 70, 100, alpha=0.1, color='red')
            ax3.fill_between(self.btc_df.index, 0, 30, alpha=0.1, color='green')

            ax3.set_title('相对强弱指数 (RSI)', fontweight='bold')
            ax3.set_ylabel('RSI')
            ax3.set_ylim(0, 100)
            ax3.legend()
            ax3.grid(True, alpha=0.3)
            ax3.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
            ax3.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))

            # 图表4: 成交量对比
            ax4.bar(self.btc_df.index, self.btc_df['volume'],
                   alpha=0.7, color='#f7931a', label='BTC 成交量', width=0.8)

            # 创建第二个y轴用于ETH成交量
            ax4_twin = ax4.twinx()
            ax4_twin.bar(self.eth_df.index, self.eth_df['volume'],
                        alpha=0.7, color='#627eea', label='ETH 成交量', width=0.8)

            ax4.set_title('成交量对比', fontweight='bold')
            ax4.set_ylabel('BTC 成交量', color='#f7931a')
            ax4_twin.set_ylabel('ETH 成交量', color='#627eea')
            ax4.tick_params(axis='y', labelcolor='#f7931a')
            ax4_twin.tick_params(axis='y', labelcolor='#627eea')
            ax4.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
            ax4.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))

            # 调整布局
            plt.tight_layout()

            # 添加最新价格信息文本框
            if latest_info:
                info_text = self._create_info_text(latest_info)
                fig.text(0.02, 0.02, info_text, fontsize=10,
                        bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8))

            print("✅ 图表创建完成")
            return True

        except Exception as e:
            print(f"❌ 图表创建失败: {e}")
            return False

    def _create_info_text(self, latest_info: Dict[str, Any]) -> str:
        """
        创建信息文本

        Args:
            latest_info: 最新价格信息

        Returns:
            str: 格式化的信息文本
        """
        try:
            btc_info = latest_info.get('btc', {})
            eth_info = latest_info.get('eth', {})
            date_str = latest_info.get('date', datetime.now()).strftime('%Y-%m-%d %H:%M')

            text = f"📊 最新数据 ({date_str})\n"
            text += f"🟠 BTC: ${btc_info.get('price', 0):,.2f} "
            text += f"({btc_info.get('change', 0):+.2f}%)\n"
            text += f"🔵 ETH: ${eth_info.get('price', 0):,.2f} "
            text += f"({eth_info.get('change', 0):+.2f}%)\n"

            if btc_info.get('rsi') is not None:
                text += f"📈 BTC RSI: {btc_info.get('rsi', 0):.1f}\n"
            if eth_info.get('rsi') is not None:
                text += f"📈 ETH RSI: {eth_info.get('rsi', 0):.1f}"

            return text

        except Exception as e:
            return f"信息显示错误: {e}"

    def print_summary(self) -> None:
        """打印数据摘要"""
        try:
            latest_info = self.get_latest_info()

            print("\n" + "="*60)
            print("📊 加密货币数据分析摘要")
            print("="*60)

            if latest_info:
                btc_info = latest_info.get('btc', {})
                eth_info = latest_info.get('eth', {})

                print(f"📅 数据日期: {latest_info.get('date', 'N/A')}")
                print(f"\n🟠 比特币 (BTC):")
                print(f"   💰 当前价格: ${btc_info.get('price', 0):,.2f}")
                print(f"   📈 24h变化: {btc_info.get('change', 0):+.2f}%")
                print(f"   📊 24h最高: ${btc_info.get('high', 0):,.2f}")
                print(f"   📉 24h最低: ${btc_info.get('low', 0):,.2f}")
                print(f"   📦 成交量: {btc_info.get('volume', 0):,.0f}")
                if btc_info.get('rsi'):
                    print(f"   📈 RSI(14): {btc_info.get('rsi', 0):.1f}")

                print(f"\n🔵 以太坊 (ETH):")
                print(f"   💰 当前价格: ${eth_info.get('price', 0):,.2f}")
                print(f"   📈 24h变化: {eth_info.get('change', 0):+.2f}%")
                print(f"   📊 24h最高: ${eth_info.get('high', 0):,.2f}")
                print(f"   📉 24h最低: ${eth_info.get('low', 0):,.2f}")
                print(f"   📦 成交量: {eth_info.get('volume', 0):,.0f}")
                if eth_info.get('rsi'):
                    print(f"   📈 RSI(14): {eth_info.get('rsi', 0):.1f}")

                # 计算相关性
                if len(self.btc_df) > 1 and len(self.eth_df) > 1:
                    btc_returns = self.btc_df['close'].pct_change().dropna()
                    eth_returns = self.eth_df['close'].pct_change().dropna()
                    correlation = btc_returns.corr(eth_returns)
                    print(f"\n📊 BTC-ETH 价格相关性: {correlation:.3f}")

                # 波动率分析
                btc_volatility = self.btc_df['close'].pct_change().std() * np.sqrt(365) * 100
                eth_volatility = self.eth_df['close'].pct_change().std() * np.sqrt(365) * 100
                print(f"\n📈 年化波动率:")
                print(f"   🟠 BTC: {btc_volatility:.1f}%")
                print(f"   🔵 ETH: {eth_volatility:.1f}%")

            print("="*60)

        except Exception as e:
            print(f"❌ 摘要生成失败: {e}")

    def save_chart(self, filename: str = "crypto_analysis.png") -> bool:
        """
        保存图表

        Args:
            filename: 文件名

        Returns:
            bool: 是否成功保存
        """
        try:
            plt.savefig(filename, dpi=300, bbox_inches='tight')
            print(f"✅ 图表已保存为: {filename}")
            return True
        except Exception as e:
            print(f"❌ 图表保存失败: {e}")
            return False


def main():
    """主程序"""
    print("🚀 OpenBB 加密货币数据分析演示程序")
    print("="*50)

    # 创建分析器实例
    analyzer = CryptoAnalyzer()

    try:
        # 步骤1: 获取数据
        print("\n📊 步骤 1: 获取加密货币数据")
        if not analyzer.fetch_crypto_data(months=6):
            print("❌ 数据获取失败，程序退出")
            return False

        # 步骤2: 计算技术指标
        print("\n📈 步骤 2: 计算技术指标")
        if not analyzer.calculate_technical_indicators():
            print("❌ 技术指标计算失败，程序退出")
            return False

        # 步骤3: 打印摘要
        print("\n📋 步骤 3: 生成数据摘要")
        analyzer.print_summary()

        # 步骤4: 创建图表
        print("\n📊 步骤 4: 创建可视化图表")
        if not analyzer.create_price_comparison_chart():
            print("❌ 图表创建失败")
            return False

        # 步骤5: 保存图表
        print("\n💾 步骤 5: 保存图表")
        analyzer.save_chart("crypto_analysis_dashboard.png")

        # 步骤6: 显示图表
        print("\n🖼️  步骤 6: 显示交互式图表")
        print("提示: 关闭图表窗口以结束程序")
        plt.show()

        print("\n✅ 程序执行完成!")
        return True

    except KeyboardInterrupt:
        print("\n⚠️  程序被用户中断")
        return False
    except Exception as e:
        print(f"\n❌ 程序执行出错: {e}")
        import traceback
        traceback.print_exc()
        return False


def check_dependencies():
    """检查依赖项"""
    required_packages = ['pandas', 'matplotlib', 'numpy']
    missing_packages = []

    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)

    if missing_packages:
        print(f"❌ 缺少必要的包: {', '.join(missing_packages)}")
        print("请运行: pip install pandas matplotlib numpy")
        return False

    return True


if __name__ == "__main__":
    print("🔍 检查依赖项...")
    if not check_dependencies():
        sys.exit(1)

    print("🔍 检查 OpenBB 平台...")
    try:
        # 简单测试 OpenBB 是否可用
        test_data = obb.crypto.search(provider="fmp")
        print("✅ OpenBB 平台可用")
    except Exception as e:
        print(f"❌ OpenBB 平台不可用: {e}")
        print("请确保您在正确的目录中运行此脚本")
        sys.exit(1)

    # 运行主程序
    success = main()
    sys.exit(0 if success else 1)
