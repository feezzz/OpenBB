# 🚀 加密货币数据分析演示项目

基于 OpenBB 平台和 Gate.io API 的专业加密货币数据分析工具

![GitHub Stars](https://img.shields.io/github/stars/feezzz/OpenBB?style=social)
![Python Version](https://img.shields.io/badge/python-3.9%2B-blue)
![License](https://img.shields.io/badge/license-AGPL--3.0-green)

## 🎯 项目简介

这是一个功能完整的加密货币数据分析演示项目，专门设计用于获取、分析和可视化比特币（BTC）和以太坊（ETH）的市场数据。项目优先使用 Gate.io API 作为数据源，提供实时、准确的市场数据分析。

### 🌟 核心特性

- **🚀 Gate.io API 集成** - 优先使用 Gate.io 交易所的实时数据
- **📊 专业图表分析** - 多维度价格走势和技术指标可视化  
- **🔍 深度市场分析** - 详细的价格、成交量、波动率分析
- **🎨 中文界面** - 完全中文化的用户界面和文档
- **💾 数据导出** - 高分辨率图表保存功能
- **🔄 多数据源支持** - Gate.io API + OpenBB 备用数据源

## 🚀 快速开始

### 安装依赖

```bash
# 安装必要的 Python 包
pip install pandas matplotlib numpy requests

# 可选：安装 OpenBB 平台（备用数据源）
pip install openbb
```

### 运行程序

#### 🎯 推荐方式：使用交互式启动器

```bash
python run_crypto_demo.py
```

#### 🌐 直接运行 Gate.io API 版本

```bash
python crypto_demo_simple.py
```

#### 📊 运行离线演示版本

```bash
python crypto_demo_offline.py
```

## 📊 功能展示

### 实时数据分析
- BTC/USDT 和 ETH/USDT 实时价格
- 历史K线数据（最近3个月）
- 24小时价格变化和成交量
- 技术指标分析（移动平均线、相关性等）

### 示例输出

```
🟠 比特币 (BTC) 市场分析:
   💰 当前价格: $114,207.80 USDT
   📈 24小时变化: +1.47%
   📦 24小时成交量: 200,286,730 BTC
   📈 年化波动率: 31.8%

🔵 以太坊 (ETH) 市场分析:
   💰 当前价格: $3,496.59 USDT
   📈 24小时变化: +3.02%
   📦 24小时成交量: 271,870,263 ETH
   📈 年化波动率: 75.8%

📊 BTC-ETH 价格相关性: 0.740 (强正相关)
```

## 📁 项目结构

```
├── gateio_api.py              # Gate.io API 客户端模块
├── crypto_demo_simple.py      # Gate.io API 版本演示程序
├── crypto_demo_offline.py     # 离线模拟数据版本
├── run_crypto_demo.py         # 交互式启动器
├── README_CN.md               # 详细中文说明文档
└── openbb_platform/           # OpenBB 核心平台文件
```

## 📚 文档

- [中文详细说明](README_CN.md) - 完整的项目介绍和使用指南
- [功能演示指南](README_CRYPTO_DEMO.md) - 详细的功能说明
- [项目总结](DEMO_SUMMARY.md) - 开发过程和技术总结

## 🔧 技术栈

- **Python 3.9+** - 主要编程语言
- **pandas** - 数据处理和分析
- **matplotlib** - 数据可视化
- **requests** - HTTP 请求处理
- **Gate.io API** - 主要数据源
- **OpenBB Platform** - 备用数据源

## ⚠️ 注意事项

- 本项目仅用于教育和演示目的，不构成投资建议
- Gate.io API 版本需要网络连接
- 数据来源于 Gate.io 交易所，为 USDT 计价
- 建议在稳定的网络环境中运行

## 🤝 贡献

欢迎提交 Issue 和 Pull Request 来改进项目！

## 📄 许可证

本项目基于 [AGPL-3.0 许可证](LICENSE) 开源。

---

**🎉 感谢使用加密货币数据分析演示项目！**

*本项目仅用于教育和演示目的，不构成投资建议。*
