import yfinance as yf
import csv
import json
import util
_ = 'hoge'

# CSVから証券コード・会社の日本語名を取得
stocks = []
with open('name.csv', 'r', encoding='utf-8') as csv_file:
    rows = csv.reader(csv_file, delimiter=',', quotechar='"')
    for row in rows:
        stocks.append(tuple(row))

# 証券コードから株価を取得
stock_data = []
for (security_code, japanese_name) in stocks:
    stock_data.append({
        'code': _,
        'name': japanese_name,
        'currentPrice': _,
        'predictPrice': _,
        'profitRatio': _,
        'recommendation': _,
        'reasonsForRecommendation': _,
    })


# JSONを出力
output_data = {'data': stock_data}
with open('data.json', 'w', encoding='utf-8') as json_file:
    json.dump(output_data, json_file, ensure_ascii=False, indent=2)
