#!/usr/bin/env python3
"""
OpenBB 加密货币数据分析演示程序 - 离线版本
==========================================

这个版本使用模拟数据来演示图表功能，适用于无法连接数据源的情况。
展示了完整的分析流程和可视化功能。

作者: OpenBB 演示
日期: 2024年
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import numpy as np
from datetime import datetime, timedelta

# 设置中文字体支持
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans', 'Arial Unicode MS']
plt.rcParams['axes.unicode_minus'] = False

def generate_mock_crypto_data():
    """生成模拟的加密货币数据"""
    print("📊 生成模拟加密货币数据...")
    
    # 生成日期范围（最近3个月）
    end_date = datetime.now()
    start_date = end_date - timedelta(days=90)
    dates = pd.date_range(start=start_date, end=end_date, freq='D')
    
    # 生成 BTC 模拟数据（基于随机游走）
    np.random.seed(42)  # 确保结果可重现
    btc_base_price = 95000
    btc_returns = np.random.normal(0.001, 0.03, len(dates))  # 日收益率
    btc_prices = [btc_base_price]
    
    for ret in btc_returns[1:]:
        btc_prices.append(btc_prices[-1] * (1 + ret))
    
    # 生成 ETH 模拟数据（与 BTC 有一定相关性）
    eth_base_price = 3400
    correlation = 0.7
    eth_returns = correlation * btc_returns + np.sqrt(1 - correlation**2) * np.random.normal(0, 0.04, len(dates))
    eth_prices = [eth_base_price]
    
    for ret in eth_returns[1:]:
        eth_prices.append(eth_prices[-1] * (1 + ret))
    
    # 创建 DataFrame
    btc_df = pd.DataFrame({
        'open': [p * (1 + np.random.normal(0, 0.005)) for p in btc_prices],
        'high': [p * (1 + abs(np.random.normal(0, 0.01))) for p in btc_prices],
        'low': [p * (1 - abs(np.random.normal(0, 0.01))) for p in btc_prices],
        'close': btc_prices,
        'volume': np.random.lognormal(15, 0.5, len(dates))
    }, index=dates)
    
    eth_df = pd.DataFrame({
        'open': [p * (1 + np.random.normal(0, 0.005)) for p in eth_prices],
        'high': [p * (1 + abs(np.random.normal(0, 0.015))) for p in eth_prices],
        'low': [p * (1 - abs(np.random.normal(0, 0.015))) for p in eth_prices],
        'close': eth_prices,
        'volume': np.random.lognormal(14, 0.6, len(dates))
    }, index=dates)
    
    print(f"✅ 模拟数据生成完成:")
    print(f"   BTC: {len(btc_df)} 个数据点")
    print(f"   ETH: {len(eth_df)} 个数据点")
    print(f"   数据期间: {dates[0].strftime('%Y-%m-%d')} 到 {dates[-1].strftime('%Y-%m-%d')}")
    
    return btc_df, eth_df


def create_comprehensive_chart(btc_df, eth_df):
    """创建综合分析图表"""
    print("📊 正在创建综合分析图表...")
    
    try:
        # 创建图表
        fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, figsize=(16, 12))
        fig.suptitle('加密货币综合分析仪表板 (模拟数据)', fontsize=16, fontweight='bold')
        
        # 获取最新价格
        btc_latest = btc_df['close'].iloc[-1]
        eth_latest = eth_df['close'].iloc[-1]
        
        # 计算价格变化
        btc_change = (btc_latest - btc_df['close'].iloc[-2]) / btc_df['close'].iloc[-2] * 100
        eth_change = (eth_latest - eth_df['close'].iloc[-2]) / eth_df['close'].iloc[-2] * 100
        
        # 图表1: 价格走势对比
        ax1.plot(btc_df.index, btc_df['close'], 
                label=f'BTC (${btc_latest:,.0f}, {btc_change:+.1f}%)', 
                color='#f7931a', linewidth=2)
        ax1.plot(eth_df.index, eth_df['close'], 
                label=f'ETH (${eth_latest:,.0f}, {eth_change:+.1f}%)', 
                color='#627eea', linewidth=2)
        
        # 添加移动平均线
        btc_ma20 = btc_df['close'].rolling(20).mean()
        eth_ma20 = eth_df['close'].rolling(20).mean()
        btc_ma50 = btc_df['close'].rolling(50).mean()
        eth_ma50 = eth_df['close'].rolling(50).mean()
        
        ax1.plot(btc_df.index, btc_ma20, color='#f7931a', alpha=0.5, linestyle='--', label='BTC MA(20)')
        ax1.plot(eth_df.index, eth_ma20, color='#627eea', alpha=0.5, linestyle='--', label='ETH MA(20)')
        ax1.plot(btc_df.index, btc_ma50, color='#f7931a', alpha=0.3, linestyle=':', label='BTC MA(50)')
        ax1.plot(eth_df.index, eth_ma50, color='#627eea', alpha=0.3, linestyle=':', label='ETH MA(50)')
        
        ax1.set_title('价格走势对比', fontweight='bold')
        ax1.set_ylabel('价格 (USD)')
        ax1.legend(fontsize=8)
        ax1.grid(True, alpha=0.3)
        
        # 图表2: 标准化收益率对比
        btc_normalized = (btc_df['close'] / btc_df['close'].iloc[0] - 1) * 100
        eth_normalized = (eth_df['close'] / eth_df['close'].iloc[0] - 1) * 100
        
        ax2.plot(btc_df.index, btc_normalized, 
                label=f'BTC ({btc_normalized.iloc[-1]:+.1f}%)', 
                color='#f7931a', linewidth=2)
        ax2.plot(eth_df.index, eth_normalized, 
                label=f'ETH ({eth_normalized.iloc[-1]:+.1f}%)', 
                color='#627eea', linewidth=2)
        
        ax2.axhline(y=0, color='black', linestyle='-', alpha=0.3)
        ax2.set_title('标准化收益率对比', fontweight='bold')
        ax2.set_ylabel('收益率 (%)')
        ax2.legend()
        ax2.grid(True, alpha=0.3)
        
        # 图表3: RSI 指标
        def calculate_rsi(prices, window=14):
            delta = prices.diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=window).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=window).mean()
            rs = gain / loss
            return 100 - (100 / (1 + rs))
        
        btc_rsi = calculate_rsi(btc_df['close'])
        eth_rsi = calculate_rsi(eth_df['close'])
        
        ax3.plot(btc_df.index, btc_rsi, label='BTC RSI', color='#f7931a', linewidth=2)
        ax3.plot(eth_df.index, eth_rsi, label='ETH RSI', color='#627eea', linewidth=2)
        
        # RSI 超买超卖线
        ax3.axhline(y=70, color='red', linestyle='--', alpha=0.7, label='超买线 (70)')
        ax3.axhline(y=30, color='green', linestyle='--', alpha=0.7, label='超卖线 (30)')
        ax3.fill_between(btc_df.index, 70, 100, alpha=0.1, color='red')
        ax3.fill_between(btc_df.index, 0, 30, alpha=0.1, color='green')
        
        ax3.set_title('相对强弱指数 (RSI)', fontweight='bold')
        ax3.set_ylabel('RSI')
        ax3.set_ylim(0, 100)
        ax3.legend(fontsize=8)
        ax3.grid(True, alpha=0.3)
        
        # 图表4: 成交量对比
        ax4.bar(btc_df.index, btc_df['volume'], alpha=0.7, color='#f7931a', 
               label='BTC 成交量', width=0.8)
        
        # 创建第二个y轴用于ETH成交量
        ax4_twin = ax4.twinx()
        ax4_twin.bar(eth_df.index, eth_df['volume'], alpha=0.7, color='#627eea', 
                    label='ETH 成交量', width=0.8)
        
        ax4.set_title('成交量对比', fontweight='bold')
        ax4.set_ylabel('BTC 成交量', color='#f7931a')
        ax4_twin.set_ylabel('ETH 成交量', color='#627eea')
        ax4.tick_params(axis='y', labelcolor='#f7931a')
        ax4_twin.tick_params(axis='y', labelcolor='#627eea')
        
        # 格式化日期轴
        for ax in [ax1, ax2, ax3, ax4]:
            ax.xaxis.set_major_formatter(mdates.DateFormatter('%m-%d'))
            ax.xaxis.set_major_locator(mdates.WeekdayLocator(interval=2))
            plt.setp(ax.xaxis.get_majorticklabels(), rotation=45)
        
        plt.tight_layout()
        
        # 添加信息文本框
        info_text = f"📊 模拟数据分析结果\n"
        info_text += f"🟠 BTC: ${btc_latest:,.0f} ({btc_change:+.1f}%)\n"
        info_text += f"🔵 ETH: ${eth_latest:,.0f} ({eth_change:+.1f}%)\n"
        info_text += f"📈 BTC RSI: {btc_rsi.iloc[-1]:.1f}\n"
        info_text += f"📈 ETH RSI: {eth_rsi.iloc[-1]:.1f}"
        
        fig.text(0.02, 0.02, info_text, fontsize=10, 
                bbox=dict(boxstyle="round,pad=0.5", facecolor="lightgray", alpha=0.8))
        
        print("✅ 图表创建完成")
        return True
        
    except Exception as e:
        print(f"❌ 图表创建失败: {e}")
        return False


def print_analysis_summary(btc_df, eth_df):
    """打印分析摘要"""
    print("\n" + "="*60)
    print("📊 加密货币分析摘要 (基于模拟数据)")
    print("="*60)
    
    try:
        # BTC 分析
        btc_latest = btc_df.iloc[-1]
        btc_change = (btc_latest['close'] - btc_df['close'].iloc[-2]) / btc_df['close'].iloc[-2] * 100
        btc_volatility = btc_df['close'].pct_change().std() * np.sqrt(365) * 100
        
        print(f"🟠 比特币 (BTC) 分析:")
        print(f"   💰 当前价格: ${btc_latest['close']:,.2f}")
        print(f"   📈 24h变化: {btc_change:+.2f}%")
        print(f"   📊 期间最高: ${btc_df['high'].max():,.2f}")
        print(f"   📉 期间最低: ${btc_df['low'].min():,.2f}")
        print(f"   📦 平均成交量: {btc_df['volume'].mean():,.0f}")
        print(f"   📊 年化波动率: {btc_volatility:.1f}%")
        
        # ETH 分析
        eth_latest = eth_df.iloc[-1]
        eth_change = (eth_latest['close'] - eth_df['close'].iloc[-2]) / eth_df['close'].iloc[-2] * 100
        eth_volatility = eth_df['close'].pct_change().std() * np.sqrt(365) * 100
        
        print(f"\n🔵 以太坊 (ETH) 分析:")
        print(f"   💰 当前价格: ${eth_latest['close']:,.2f}")
        print(f"   📈 24h变化: {eth_change:+.2f}%")
        print(f"   📊 期间最高: ${eth_df['high'].max():,.2f}")
        print(f"   📉 期间最低: ${eth_df['low'].min():,.2f}")
        print(f"   📦 平均成交量: {eth_df['volume'].mean():,.0f}")
        print(f"   📊 年化波动率: {eth_volatility:.1f}%")
        
        # 相关性分析
        btc_returns = btc_df['close'].pct_change().dropna()
        eth_returns = eth_df['close'].pct_change().dropna()
        correlation = btc_returns.corr(eth_returns)
        
        print(f"\n📊 市场分析:")
        print(f"   🔗 BTC-ETH 价格相关性: {correlation:.3f}")
        print(f"   📅 分析期间: {btc_df.index[0].strftime('%Y-%m-%d')} 到 {btc_df.index[-1].strftime('%Y-%m-%d')}")
        print(f"   📈 数据点数量: {len(btc_df)} 天")
        
        # 技术分析信号
        btc_ma20 = btc_df['close'].rolling(20).mean().iloc[-1]
        btc_ma50 = btc_df['close'].rolling(50).mean().iloc[-1]
        eth_ma20 = eth_df['close'].rolling(20).mean().iloc[-1]
        eth_ma50 = eth_df['close'].rolling(50).mean().iloc[-1]
        
        print(f"\n📈 技术分析信号:")
        btc_trend = "看涨" if btc_latest['close'] > btc_ma20 > btc_ma50 else "看跌" if btc_latest['close'] < btc_ma20 < btc_ma50 else "震荡"
        eth_trend = "看涨" if eth_latest['close'] > eth_ma20 > eth_ma50 else "看跌" if eth_latest['close'] < eth_ma20 < eth_ma50 else "震荡"
        
        print(f"   🟠 BTC 趋势: {btc_trend}")
        print(f"   🔵 ETH 趋势: {eth_trend}")
        
        print("="*60)
        print("⚠️  注意: 以上数据为模拟数据，仅用于演示目的")
        
    except Exception as e:
        print(f"❌ 摘要生成失败: {e}")


def main():
    """主程序"""
    print("🚀 OpenBB 加密货币数据分析演示程序 (离线版)")
    print("="*55)
    print("ℹ️  本程序使用模拟数据演示完整的分析功能")
    
    # 生成模拟数据
    btc_df, eth_df = generate_mock_crypto_data()
    
    # 打印分析摘要
    print_analysis_summary(btc_df, eth_df)
    
    # 创建综合图表
    if create_comprehensive_chart(btc_df, eth_df):
        # 保存图表
        try:
            plt.savefig("crypto_offline_analysis.png", dpi=300, bbox_inches='tight')
            print("✅ 图表已保存为: crypto_offline_analysis.png")
        except Exception as e:
            print(f"⚠️  图表保存失败: {e}")
        
        # 显示图表
        print("\n🖼️  显示交互式图表...")
        print("提示: 关闭图表窗口以结束程序")
        plt.show()
    
    print("\n✅ 程序执行完成!")
    print("💡 提示: 这是使用模拟数据的演示版本")
    return True


if __name__ == "__main__":
    try:
        success = main()
        exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n⚠️  程序被用户中断")
        exit(1)
    except Exception as e:
        print(f"\n❌ 程序执行出错: {e}")
        exit(1)
