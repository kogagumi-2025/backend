# 証券コードを受け取って、推奨度と理由をtaple型で返すコード
import talib
import numpy as np
import pandas as pd

def analyze_stock(df):

    # TALib の SMA を計算（1次元に変換）
    close = df['Close'].values.flatten()
    cols = ['Original']
    df['SMA5'] = talib.SMA(close, timeperiod=5)
    df['SMA30'] = talib.SMA(close, timeperiod=30)


    # RSIの計算
    output = np.c_[output, talib.RSI(close)]
    cols += ['RSI']

    # MACDの計算
    for arr in talib.MACD(close):
        output = np.c_[output, arr]
    cols += ['MACD', 'MACD_signal', 'MACD_hist']


    # ボリンジャーバンドの計算
    for arr in talib.BBANDS(close):
        output = np.c_[output, arr]
    cols += ['BBANDS_upperband', 'BBANDS_middleband', 'BBANDS_lowerband']

    
    # 出来高移動平均の計算
    volume = df['Volume'].values.flatten()
    vma = volume.mean()

    # SMAのスコア化
    # 短期SMAが長期SMAを上回っていれば1、下回っていれば-1、同じなら0
    if(df['SMA5'] - df['SMA30']).iloc[-1] > 0:
        sma_score = 1
        sma_reason = "上昇トレンドです"
    elif(df['SMA5'] - df['SMA30']).iloc[-1] < 0:
        sma_score = -1
        sma_reason = "下降トレンドです"
    else:
        sma_score = 0
        sma_reason = "横ばいです"

    # RSIのスコア化
    # RSIが70以上なら-1、30以下なら1、その他は0
    # RSIが70％～80％を超えると買われ過ぎ、反対に20％～30％を割り込むと売られ過ぎとされる。(参考サイト：https://info.monex.co.jp/technical-analysis/indicators/005.html)
    if output[-1, cols.index('RSI')] >= 70:
        rsi_score = -1
        rsi_reason = "買われすぎが確認されます"
    elif output[-1, cols.index('RSI')] <= 30:
        rsi_score = 1
        rsi_reason = "売られすぎが確認されます"
    else:
        rsi_score = 0
        rsi_reason = "中立的な状態が確認されます"

    # MACDのスコア化
    # ゴールデンクロスで1、デッドクロスで-1、その他は0
    if output[-1, cols.index('MACD')] > output[-1, cols.index('MACD_signal')] and \
    output[-2, cols.index('MACD')] <= output[-2, cols.index('MACD_signal')]:
        macd_score = 1 # ゴールデンクロス
        macd_reason = "ゴールデンクロスが発生した"
    elif output[-1, cols.index('MACD')] < output[-1, cols.index('MACD_signal')] and \
        output[-2, cols.index('MACD')] >= output[-2, cols.index('MACD_signal')]:
        macd_score = -1 # デッドクロス
        macd_reason = "デッドクロスが発生しています"
    else:
        macd_score = 0
        macd_reason = "クロスは発生していません"

    # ボリンジャーバンドのスコア化
    # 終値が上部バンドを上回れば-1、下部バンドを下回れば1、その他は0
    if output[-1, cols.index('Original')] > output[-1, cols.index('BBANDS_upperband')]:
        bbands_score = -1
        bbands_reason = "ボリンジャーバンドの上限を上回りました"
    elif output[-1, cols.index('Original')] < output[-1, cols.index('BBANDS_lowerband')]:
        bbands_score = 1
        bbands_reason = "ボリンジャーバンドの下限を下回りました"
    else:
        bbands_score = 0
        bbands_reason = "ボリンジャーバンドの範囲内です"

    # 出来高移動平均のスコア化
    # 直近1日の出来高が移動平均を上回れば1、下回れば-1、同じなら0
    if vma > volume[-1]:
        volume_sma_score = 1
        volume_sma_reason = "出来高が平均より高く、活発です"
    elif vma < volume[-1]:
        volume_sma_score = -1
        volume_sma_reason = "出来高が平均より低く、低調です"
    else:
        volume_sma_score = 0
        volume_sma_reason = "出来高は平均的です"

    # 推奨度の計算
    recommendation_score = (sma_score + rsi_score + macd_score + bbands_score + volume_sma_score) / 5

    # 推奨度と理由をtuple型で返す
    recommendation = (recommendation_score, sma_reason, rsi_reason, macd_reason, bbands_reason, volume_sma_reason)
    return recommendation