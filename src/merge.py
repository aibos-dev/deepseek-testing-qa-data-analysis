import os
import json
import sys

def collect_all_in_one(
    folder_path=sys.argv[1],
    output_file='merged_data.json'
):
    """
    1) folder_path 内の .txt ファイルを探し、
       '[AI Output]' 行以降の ```json ～ ``` ブロックをすべて抽出します。
    2) UID が重複する場合は、先に出現したデータを優先（後からの同一UIDは無視）します。
    3) 抽出したすべてのデータをまとめてフラットな配列にし、output_file に JSON 出力します。
    """

    all_data_map = {}  # { uid: JSONオブジェクト } (重複排除用)

    for filename in os.listdir(folder_path):
        if not filename.endswith('.txt'):
            continue

        filepath = os.path.join(folder_path, filename)

        with open(filepath, 'r', encoding='utf-8') as f:
            lines = f.readlines()

        inside_ai_output = False
        inside_json_block = False
        json_buffer = []

        for line in lines:
            # [AI Output] が出現したらフラグON
            if '[AI Output]' in line:
                inside_ai_output = True
                inside_json_block = False
                json_buffer = []
                continue

            if inside_ai_output:
                # ```json で JSONブロック開始
                if '```json' in line:
                    inside_json_block = True
                    json_buffer = []
                    continue

                # ``` (終端) で JSONブロック終了
                if '```' in line and inside_json_block:
                    inside_json_block = False
                    json_text = ''.join(json_buffer).strip()

                    # JSONパースして UID をキーとして保存
                    try:
                        data = json.loads(json_text)
                        if isinstance(data, list):
                            for item in data:
                                uid = item.get('uid')
                                if uid and uid not in all_data_map:
                                    all_data_map[uid] = item
                        elif isinstance(data, dict):
                            uid = data.get('uid')
                            if uid and uid not in all_data_map:
                                all_data_map[uid] = data
                    except json.JSONDecodeError as e:
                        print(f"[JSONDecodeError] {filename} の JSON パースに失敗: {e}")

                    continue

                # JSONブロック内の行をバッファに保持
                if inside_json_block:
                    json_buffer.append(line)

    # 収集したデータを1つのリストにしてJSON出力
    merged_data = list(all_data_map.values())

    with open(output_file, 'w', encoding='utf-8') as f_out:
        json.dump(merged_data, f_out, ensure_ascii=False, indent=2)

    print(f"[INFO] すべてのデータを {output_file} に統合しました。")


if __name__ == '__main__':
    collect_all_in_one()
