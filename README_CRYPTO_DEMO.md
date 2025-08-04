# OpenBB 加密货币数据分析演示程序

这个演示程序展示了如何使用 OpenBB 平台获取和分析加密货币数据，包括比特币（BTC）和以太坊（ETH）的价格走势对比和技术分析。

## 📁 文件说明

- `crypto_demo.py` - 完整版演示程序，包含高级功能和多个图表
- `crypto_demo_simple.py` - 简化版演示程序，专注于核心功能
- `crypto_demo_offline.py` - 离线版演示程序，使用模拟数据（推荐）
- `README_CRYPTO_DEMO.md` - 本说明文件
- `crypto_offline_analysis.png` - 生成的示例图表

## 🚀 快速开始

### 1. 环境准备

确保您已经克隆了 OpenBB 项目并且在项目根目录中：

```bash
cd OpenBB
```

### 2. 安装依赖

```bash
# 安装基础依赖
pip install pandas matplotlib numpy

# 如果需要完整的 OpenBB 功能
pip install openbb
```

### 3. 运行演示程序

#### 选项 A: 运行离线版（推荐，使用模拟数据）

```bash
python crypto_demo_offline.py
```

#### 选项 B: 运行简化版（需要网络连接）

```bash
python crypto_demo_simple.py
```

#### 选项 C: 运行完整版（需要网络连接和API密钥）

```bash
python crypto_demo.py
```

**注意**: 由于数据提供商的速率限制，推荐首先运行离线版本来体验完整功能。

## 📊 程序功能

### 简化版功能 (`crypto_demo_simple.py`)

- ✅ 获取 BTC 和 ETH 最近6个月的历史价格数据
- ✅ 创建价格走势对比图表
- ✅ 显示标准化收益率对比
- ✅ 添加20日移动平均线
- ✅ 显示最新价格和变化信息
- ✅ 计算价格相关性
- ✅ 保存图表为 PNG 文件

### 完整版功能 (`crypto_demo.py`)

- ✅ 简化版的所有功能
- ✅ 多面板仪表板显示
- ✅ RSI 技术指标分析
- ✅ MACD 指标计算
- ✅ 布林带分析
- ✅ 成交量对比分析
- ✅ 波动率计算
- ✅ 详细的数据摘要报告

## 📈 输出示例

程序运行后会显示：

```
🚀 OpenBB 加密货币数据分析演示程序
==================================================
📊 正在获取加密货币数据...
📅 数据期间: 2024-06-04 到 2024-12-04
🔄 获取比特币数据...
🔄 获取以太坊数据...
✅ 数据获取成功:
   BTC: 184 个数据点
   ETH: 184 个数据点

==================================================
📊 加密货币数据摘要
==================================================
🟠 比特币 (BTC):
   💰 当前价格: $96,234.56
   📈 24h变化: +2.34%
   📊 24h最高: $97,123.45
   📉 24h最低: $94,567.89
   📦 成交量: 12,345,678

🔵 以太坊 (ETH):
   💰 当前价格: $3,456.78
   📈 24h变化: +1.87%
   📊 24h最高: $3,512.34
   📉 24h最低: $3,398.76
   📦 成交量: 8,765,432

📊 BTC-ETH 价格相关性: 0.823
==================================================
```

## 🖼️ 图表说明

### 简化版图表

1. **价格走势对比** - 显示 BTC 和 ETH 的绝对价格走势及20日移动平均线
2. **标准化收益率对比** - 显示两种货币相对于期初的收益率变化

### 完整版图表

1. **价格走势对比** - 包含移动平均线的价格图表
2. **标准化收益率对比** - 百分比收益率对比
3. **RSI 指标** - 相对强弱指数，显示超买超卖区域
4. **成交量对比** - 双轴成交量对比图

## ⚠️ 注意事项

### 数据提供商

- 程序使用 Yahoo Finance 作为数据源（免费，无需 API 密钥）
- 数据可能有15-20分钟的延迟
- 如需实时数据，可以配置付费数据提供商

### 常见问题

1. **导入错误**
   ```
   ❌ OpenBB 导入失败: No module named 'openbb'
   ```
   解决方案：确保在 OpenBB 项目根目录中运行脚本

2. **数据获取失败**
   ```
   ❌ 数据获取失败: HTTP Error 429
   ```
   解决方案：等待几分钟后重试，或检查网络连接

3. **图表显示问题**
   ```
   ❌ 图表创建失败: No display name and no $DISPLAY environment variable
   ```
   解决方案：在有图形界面的环境中运行，或使用 `plt.savefig()` 仅保存图片

## 🔧 自定义选项

### 修改数据期间

在 `get_crypto_data()` 函数中修改：

```python
# 获取最近3个月的数据
start_date = end_date - timedelta(days=90)

# 获取最近1年的数据
start_date = end_date - timedelta(days=365)
```

### 添加其他加密货币

```python
# 添加更多加密货币
ada_data = obb.crypto.price.historical(
    symbol="ADA-USD",
    start_date=start_str,
    end_date=end_str,
    provider="yfinance"
)
```

### 修改技术指标参数

```python
# 修改移动平均线周期
btc_ma10 = btc_df['close'].rolling(10).mean()  # 10日均线
btc_ma50 = btc_df['close'].rolling(50).mean()  # 50日均线
```

## 📚 扩展学习

- [OpenBB 官方文档](https://docs.openbb.co)
- [技术分析指标说明](https://www.investopedia.com/technical-analysis-4689657)
- [加密货币市场分析](https://coinmarketcap.com/academy/)

## 🤝 贡献

欢迎提交问题报告和改进建议！

## 📄 许可证

本演示程序遵循 OpenBB 项目的许可证条款。
