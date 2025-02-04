import json
from collections import defaultdict
import sys
import os

# ファイルを読み込む
input_file = 'merged_data.json'
output_file = os.path.join(sys.argv[1], 'category_count.json')

# 文字列を正規化する関数
def normalize_classification(s: str) -> str:
    # 全角半角の混在対策や表記ゆれをまとめたいなら適宜ここで調整
    # 今回は角括弧を削除し、前後の空白を除去する
    s = s.replace("[", "").replace("]", "")
    s = s.strip()
    return s

with open(input_file, 'r', encoding='utf-8') as file:
    data = json.load(file)

# カテゴリごとの分類数をカウントする辞書
category_counts = defaultdict(lambda: defaultdict(int))

# 各エントリーを処理
for entry in data:
    for category, classification in entry.items():
        if category == "uid":  # uidは無視
            continue
        # classification がリストの場合と文字列の場合を処理
        if isinstance(classification, list):
            for item in classification:
                normalized_item = normalize_classification(item)
                category_counts[category][normalized_item] += 1
        elif isinstance(classification, str):
            for item in classification.split(", "):  # 文字列をカンマで分割
                normalized_item = normalize_classification(item)
                category_counts[category][normalized_item] += 1

# カウント結果をファイルに保存
with open(output_file, 'w', encoding='utf-8') as file:
    json.dump(category_counts, file, ensure_ascii=False, indent=4)

print(f"分類数の頻度を {output_file} に保存しました。")
