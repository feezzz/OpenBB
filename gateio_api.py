#!/usr/bin/env python3
"""
Gate.io API 数据获取模块
======================

这个模块提供了与 Gate.io API 交互的功能，用于获取加密货币的实时和历史价格数据。
Gate.io 是一个知名的加密货币交易所，提供丰富的市场数据 API。

主要功能：
- 获取加密货币实时价格
- 获取历史K线数据
- 处理API认证和速率限制
- 数据格式标准化

作者: 加密货币分析演示项目
日期: 2024年
"""

import requests
import pandas as pd
import time
from datetime import datetime, timedelta
from typing import Optional, Dict, Any, List
import json


class GateIOAPI:
    """Gate.io API 客户端类"""
    
    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None):
        """
        初始化 Gate.io API 客户端
        
        Args:
            api_key: API 密钥（可选，公开数据不需要）
            api_secret: API 密钥（可选，公开数据不需要）
        """
        self.base_url = "https://api.gateio.ws/api/v4"
        self.api_key = api_key
        self.api_secret = api_secret
        
        # 请求会话，用于连接复用
        self.session = requests.Session()
        self.session.headers.update({
            'Accept': 'application/json',
            'Content-Type': 'application/json',
            'User-Agent': 'OpenBB-Crypto-Demo/1.0'
        })
        
        # 速率限制控制
        self.last_request_time = 0
        self.min_request_interval = 0.1  # 最小请求间隔（秒）
        
        print("✅ Gate.io API 客户端初始化完成")
    
    def _rate_limit(self):
        """实施速率限制"""
        current_time = time.time()
        time_since_last = current_time - self.last_request_time
        
        if time_since_last < self.min_request_interval:
            sleep_time = self.min_request_interval - time_since_last
            time.sleep(sleep_time)
        
        self.last_request_time = time.time()
    
    def _make_request(self, endpoint: str, params: Optional[Dict] = None) -> Dict[str, Any]:
        """
        发送 API 请求
        
        Args:
            endpoint: API 端点
            params: 请求参数
            
        Returns:
            Dict: API 响应数据
            
        Raises:
            Exception: 请求失败时抛出异常
        """
        self._rate_limit()
        
        url = f"{self.base_url}{endpoint}"
        
        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            
            data = response.json()
            return data
            
        except requests.exceptions.RequestException as e:
            raise Exception(f"Gate.io API 请求失败: {e}")
        except json.JSONDecodeError as e:
            raise Exception(f"Gate.io API 响应解析失败: {e}")
    
    def get_ticker(self, symbol: str) -> Dict[str, Any]:
        """
        获取交易对的实时价格信息
        
        Args:
            symbol: 交易对符号，如 'BTC_USDT'
            
        Returns:
            Dict: 包含价格信息的字典
        """
        try:
            endpoint = f"/spot/tickers"
            params = {"currency_pair": symbol}
            
            data = self._make_request(endpoint, params)
            
            if not data:
                raise Exception(f"未找到交易对 {symbol} 的数据")
            
            ticker = data[0] if isinstance(data, list) else data
            
            # 标准化数据格式
            return {
                'symbol': symbol,
                'price': float(ticker.get('last', 0)),
                'high_24h': float(ticker.get('high_24h', 0)),
                'low_24h': float(ticker.get('low_24h', 0)),
                'volume_24h': float(ticker.get('base_volume', 0)),
                'change_24h': float(ticker.get('change_percentage', 0)),
                'timestamp': datetime.now()
            }
            
        except Exception as e:
            raise Exception(f"获取 {symbol} 实时价格失败: {e}")
    
    def get_historical_data(self, symbol: str, interval: str = '1d', 
                          start_date: Optional[str] = None, 
                          end_date: Optional[str] = None,
                          limit: int = 1000) -> pd.DataFrame:
        """
        获取历史K线数据
        
        Args:
            symbol: 交易对符号，如 'BTC_USDT'
            interval: 时间间隔 ('1m', '5m', '15m', '30m', '1h', '4h', '8h', '1d', '7d')
            start_date: 开始日期 (YYYY-MM-DD)
            end_date: 结束日期 (YYYY-MM-DD)
            limit: 数据条数限制
            
        Returns:
            pd.DataFrame: 历史价格数据
        """
        try:
            endpoint = f"/spot/candlesticks"
            
            # 构建请求参数
            params = {
                'currency_pair': symbol,
                'interval': interval,
                'limit': limit
            }
            
            # 处理日期参数
            if start_date:
                start_timestamp = int(datetime.strptime(start_date, '%Y-%m-%d').timestamp())
                params['from'] = start_timestamp
            
            if end_date:
                end_timestamp = int(datetime.strptime(end_date, '%Y-%m-%d').timestamp())
                params['to'] = end_timestamp
            
            print(f"🔄 正在获取 {symbol} 的历史数据...")
            data = self._make_request(endpoint, params)
            
            if not data:
                raise Exception(f"未获取到 {symbol} 的历史数据")
            
            # 转换为 DataFrame
            df_data = []
            for candle in data:
                df_data.append({
                    'timestamp': datetime.fromtimestamp(int(candle[0])),
                    'open': float(candle[5]),
                    'high': float(candle[3]),
                    'low': float(candle[4]),
                    'close': float(candle[2]),
                    'volume': float(candle[1])
                })
            
            df = pd.DataFrame(df_data)
            df.set_index('timestamp', inplace=True)
            df.sort_index(inplace=True)
            
            print(f"✅ 成功获取 {len(df)} 条 {symbol} 历史数据")
            return df
            
        except Exception as e:
            raise Exception(f"获取 {symbol} 历史数据失败: {e}")
    
    def get_multiple_tickers(self, symbols: List[str]) -> Dict[str, Dict[str, Any]]:
        """
        批量获取多个交易对的实时价格
        
        Args:
            symbols: 交易对符号列表
            
        Returns:
            Dict: 包含所有交易对价格信息的字典
        """
        results = {}
        
        for symbol in symbols:
            try:
                ticker_data = self.get_ticker(symbol)
                results[symbol] = ticker_data
                print(f"✅ 获取 {symbol} 价格: ${ticker_data['price']:,.2f}")
            except Exception as e:
                print(f"⚠️  获取 {symbol} 价格失败: {e}")
                results[symbol] = None
        
        return results
    
    def convert_symbol_format(self, symbol: str, from_format: str = 'standard') -> str:
        """
        转换交易对符号格式
        
        Args:
            symbol: 原始符号
            from_format: 原始格式 ('standard' 如 'BTC-USD', 'gateio' 如 'BTC_USDT')
            
        Returns:
            str: 转换后的符号
        """
        if from_format == 'standard':
            # 从标准格式 (BTC-USD) 转换为 Gate.io 格式 (BTC_USDT)
            if '-USD' in symbol:
                return symbol.replace('-USD', '_USDT')
            elif '-USDT' in symbol:
                return symbol.replace('-', '_')
            else:
                return symbol.replace('-', '_')
        else:
            # 从 Gate.io 格式转换为标准格式
            return symbol.replace('_', '-').replace('USDT', 'USD')
    
    def test_connection(self) -> bool:
        """
        测试 API 连接
        
        Returns:
            bool: 连接是否成功
        """
        try:
            endpoint = "/spot/currencies/BTC"
            self._make_request(endpoint)
            print("✅ Gate.io API 连接测试成功")
            return True
        except Exception as e:
            print(f"❌ Gate.io API 连接测试失败: {e}")
            return False


def test_gateio_api():
    """测试 Gate.io API 功能"""
    print("🧪 开始测试 Gate.io API...")
    
    # 创建 API 客户端
    api = GateIOAPI()
    
    # 测试连接
    if not api.test_connection():
        return False
    
    try:
        # 测试获取实时价格
        print("\n📊 测试获取实时价格...")
        btc_ticker = api.get_ticker('BTC_USDT')
        eth_ticker = api.get_ticker('ETH_USDT')
        
        print(f"BTC 价格: ${btc_ticker['price']:,.2f} ({btc_ticker['change_24h']:+.2f}%)")
        print(f"ETH 价格: ${eth_ticker['price']:,.2f} ({eth_ticker['change_24h']:+.2f}%)")
        
        # 测试获取历史数据
        print("\n📈 测试获取历史数据...")
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        
        btc_history = api.get_historical_data(
            'BTC_USDT', 
            interval='1d',
            start_date=start_date.strftime('%Y-%m-%d'),
            end_date=end_date.strftime('%Y-%m-%d')
        )
        
        print(f"获取到 {len(btc_history)} 天的 BTC 历史数据")
        print("最近5天的收盘价:")
        print(btc_history['close'].tail().to_string())
        
        print("\n✅ Gate.io API 测试完成!")
        return True
        
    except Exception as e:
        print(f"❌ Gate.io API 测试失败: {e}")
        return False


if __name__ == "__main__":
    # 运行测试
    test_gateio_api()
