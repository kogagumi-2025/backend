import yfinance as yf
import csv
import json
import util

# CSVから証券コード・会社の日本語名を取得
stocks = []
with open('name.csv', 'r', encoding='utf-8') as csv_file:
    rows = csv.reader(csv_file, delimiter=',', quotechar='"')
    for row in rows:
        stocks.append(tuple(row))

# 証券コードから株価を取得
stock_data = []
security_codes = [row[0] for row in stocks]
df = yf.download(tickers=security_codes, period='3mo', auto_adjust=True)
for (security_code, japanese_name) in stocks:
    tmp = yf.Ticker(security_code)
    analyzed_data = util.analyze_stock(df.loc[:, (slice(None), security_code)])
    stock_data.append({
        'code': security_code,
        'name': japanese_name,
        'currentPrice': tmp.info['currentPrice'],
        'recommendation': analyzed_data[0],
        'reasonsForRecommendation': '<br>'.join(analyzed_data[1:]),
    })


# JSONを出力
output_data = {'data': stock_data}
with open('data.json', 'w', encoding='utf-8') as json_file:
    json.dump(output_data, json_file, ensure_ascii=False, indent=2)
