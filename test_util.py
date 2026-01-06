import unittest
import pandas as pd
import numpy as np
import talib
import util

class TestStockAnalysis(unittest.TestCase):

    def setUp(self):
        """テストの前準備"""
        self.days = 50
        self.df = pd.DataFrame({
            'Close': np.full(self.days, 1000.0),
            'Volume': np.full(self.days, 1000.0)
        })

    # SMA上昇トレンドのテスト
    def test_sma_rising_trend(self):
        self.df.iloc[-1, self.df.columns.get_loc('Close')] = 2000.0
        result = util.analyze_stock(self.df)

        expected_reason = "上昇トレンドです"
        print(f"期待値: {expected_reason} 実測値: {result[1]}")
        
        self.assertEqual(result[1], expected_reason)
    
    # SMA下降トレンドのテスト
    def test_sma_falling_trend(self):
        self.df.iloc[-1, self.df.columns.get_loc('Close')] = 500.0
        result = util.analyze_stock(self.df)

        expected_reason = "下降トレンドです"
        print(f"期待値: {expected_reason} 実測値: {result[1]}")
        
        self.assertEqual(result[1], expected_reason)
    
    # SMA横ばいのテスト
    def test_sma_sideways_trend(self):
        result = util.analyze_stock(self.df)

        expected_reason = "横ばいです"
        print(f"期待値: {expected_reason} 実測値: {result[1]}")
        
        self.assertEqual(result[1], expected_reason)

    # RSI買われ過ぎのテスト
    def test_rsi_overbought(self):
        self.df.iloc[-1, self.df.columns.get_loc('Close')] = 3000.0
        result = util.analyze_stock(self.df)

        expected_reason = "買われすぎが確認されます"
        print(f"期待値: {expected_reason} 実測値: {result[2]}")
        
        self.assertEqual(result[2], expected_reason)
    
    # RSI売られ過ぎのテスト
    def test_rsi_oversold(self):
        self.df.iloc[-1, self.df.columns.get_loc('Close')] = 100.0
        result = util.analyze_stock(self.df)

        expected_reason = "売られすぎが確認されます"
        print(f"期待値: {expected_reason} 実測値: {result[2]}")
        
        self.assertEqual(result[2], expected_reason)
    
    # RSI中立のテスト
    def test_rsi_neutral(self):
        result = util.analyze_stock(self.df)

        expected_reason = "中立的な状態が確認されます"
        print(f"期待値: {expected_reason} 実測値: {result[2]}")
        
        self.assertEqual(result[2], expected_reason)

    # MACDゴールデンクロスのテスト
    def test_macd_golden_cross(self):
        self.df.iloc[-2, self.df.columns.get_loc('Close')] = 900.0
        self.df.iloc[-1, self.df.columns.get_loc('Close')] = 2000.0
        result = util.analyze_stock(self.df)

        expected_reason = "ゴールデンクロスが発生した"
        print(f"期待値: {expected_reason} 実測値: {result[3]}")
        
        self.assertEqual(result[3], expected_reason)
    
    # MACDデッドクロスのテスト
    def test_macd_dead_cross(self):
        self.df.iloc[-2, self.df.columns.get_loc('Close')] = 2000.0
        self.df.iloc[-1, self.df.columns.get_loc('Close')] = 900.0
        result = util.analyze_stock(self.df)

        expected_reason = "デッドクロスが発生しています"
        print(f"期待値: {expected_reason} 実測値: {result[3]}")
        
        self.assertEqual(result[3], expected_reason)

    # MACDクロスなしのテスト
    def test_macd_no_cross(self):
        result = util.analyze_stock(self.df)

        expected_reason = "クロスは発生していません"
        print(f"期待値: {expected_reason} 実測値: {result[3]}")
        
        self.assertEqual(result[3], expected_reason)
    
    # ボリンジャーバンド上限超えのテスト
    def test_bbands_upper_break(self):
        self.df.iloc[-1, self.df.columns.get_loc('Close')] = 3000.0
        result = util.analyze_stock(self.df)

        expected_reason = "ボリンジャーバンドの上限を上回りました"
        print(f"期待値: {expected_reason} 実測値: {result[4]}")
        
        self.assertEqual(result[4], expected_reason)
    # ボリンジャーバンド下限割れのテスト
    def test_bbands_lower_break(self):
        self.df.iloc[-1, self.df.columns.get_loc('Close')] = 100.0
        result = util.analyze_stock(self.df)

        expected_reason = "ボリンジャーバンドの下限を下回りました"
        print(f"期待値: {expected_reason} 実測値: {result[4]}")
        
        self.assertEqual(result[4], expected_reason)
    # ボリンジャーバンド範囲内のテスト
    def test_bbands_within_range(self):
        result = util.analyze_stock(self.df)

        expected_reason = "ボリンジャーバンドの範囲内です"
        print(f"期待値: {expected_reason} 実測値: {result[4]}")
        
        self.assertEqual(result[4], expected_reason)



if __name__ == '__main__':
    print("=== テストを開始します ===")
    unittest.main(argv=['first-arg-is-ignored'], exit=False, verbosity=2)