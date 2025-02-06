import json
import os
from datetime import datetime
import sys
import subprocess

# Model path setup
model_01 = "/workspace/models/DeepSeek-R1-Distill-Llama-70B-IQ2_XS-00001-of-00002.gguf"
model_02 = "/workspace/models/DeepSeek-R1-Distill-Llama-70B-IQ3_S-00001-of-00003.gguf"

model_name = model_01

# Path to the llama.cpp binary
LLAMA_RUN_PATH = "/workspace/llama.cpp/build/bin/llama-run"

# ---------------------------------------------------------------------------------------------#
# プロンプト
input_prompt = """

**指示:**

このJSONデータは、人物動作理解タスクにおける質問と回答候補とAIから得られた回答のデータです。
このJSONデータを詳細に分析し、各データエントリに対して、以下の観点からカテゴリラベルを付けてください。


**観点:**

**A.  映像内容:**

1.  **動作の種類:** (制作 - [加工作業, 組み立て作業, 創造活動, 生成], 維持管理 - [清掃, 修理, 保守, 整理整頓], 移動・運搬 - [持ち上げ, 運ぶ, 設置, 手渡し], 操作・制御 - [機械操作, 道具操作, 入力操作,  調整], 情報処理 - [思考, 判断, 計算,  計画], 身体動作 - [歩行, 起立, 着席,  ジェスチャー],  生理的行動 - [食事, 休息, 身だしなみ], 社会的 interaction - [協力, 指示, 会話,  交渉], その他 - [待機, 観察,  検索],  なし)
2.  **場所:** (屋内 - [キッチン, リビング, 作業場, オフィス, 店舗, 施設], 屋外 - [公園, 道路, 建設現場, 農地, 自然], 乗り物内, 水中, 不明)
3.  **登場人物の数:** (0人, 1人, 2人, 3-5人, 6人以上)
4.  **登場人物の関係性:** (家族 - [親子, 夫婦, 兄弟姉妹],  友人, 同僚, 上司/部下, 教師/生徒,  店員/客, 知人, 見知らぬ人,  一人, 動物)
5.  **対象オブジェクト:** (道具 - [種類名 - 手工具, 電動工具,  具体名 - ハンマー, ドリル], 材料 - [種類名 - 木材, 金属, 食品,  具体名 -  合板, アルミ板,  小麦粉],  素材 - [自然物, 人工物], その他物体 - [種類名 - 家具, 家電, 容器,  具体名 -  椅子, 冷蔵庫, ボウル],  ソフトウェア,  なし)
6.  **インタラクションの種類:** (言語的コミュニケーション - [指示, 質問, 応答, 説明,  独り言], 非言語的コミュニケーション - [アイコンタクト, ジェスチャー, 表情], 身体的接触 - [手渡し, 支え, 触れる, 衝突], 物の受け渡し, 共同作業,  影響 - [操作, 干渉],  なし)
7.  **視点の種類:** (固定 - [全体, 一部 -  寄り, 引き], 移動 - [追跡 -  人物追跡, 物体追跡, パン, チルト, ズーム], 主観 - [一人称, 当事者,  肩越し], マルチアングル)
8.  **異常行動の有無:** (あり - [種類 -  転倒,  誤操作,  ルール違反,  故障,  不審行動], なし)
9.  **協調性の有無 (複数人物の場合):** (あり - [協調行動の種類 -  共同作業,  役割分担,  支援], なし,  競合)
10. **動作の粒度:** (粗粒度 - [例:  料理をする,  運転する], 細粒度 - [例:  卵を割る,  ハンドルを回す])
11. **身体部位:** (手 - [右手, 左手, 両手], 足 - [右足, 左足, 両足], 頭部 - [顔, 目, 口],  体幹, 全身, 指, その他 - [腕, 肘, 膝])
12. **視覚的特徴:** (色 - [具体例 -  赤色, 青色], 柄 - [具体例 -  ストライプ, 水玉], テクスチャ - [具体例 -  滑らか, 粗い], 形状 - [具体例 -  円形, 四角形], 明るさ - [具体例 -  明るい, 暗い], 透明度 - [透明, 半透明, 不透明])
13. **音:** (あり - [音の種類 -  環境音,  人の声,  物音 -  機械音,  自然音], なし)
14. **アフォーダンス:** (切断 - [切る, 削る], 結合 - [貼る, 組み立てる], 移動・変形 - [押す, 引く,  曲げる,  注ぐ], 包含 - [入れる, 収納する],  支持 - [持つ,  支える],  操作 - [回す,  押す (ボタン)],  知覚 - [見る,  聞く])
15. **タスクの目的:** (遊び/娯楽, 仕事/業務, 学習/教育, 創作/制作, 生活維持, 移動/輸送, コミュニケーション,  健康/運動,  儀式/イベント, その他)
16. **作業環境:** (整理されている, 散らかっている, 清潔, 汚れている,  安全, 危険)
17. **感情/心理状態:** (集中, リラックス, 焦り, 喜び, 悲しみ, 怒り, 困惑, 驚き, 不安, 退屈,  不明)
18. **使用言語 (音声がある場合):** (日本語, 英語, 中国語, 韓国語, その他 - [言語名], なし)
19. **視線の方向:** (対象物, 操作箇所, 周囲, カメラ,  指示対象,  不明)
20. **身体の姿勢:** (立位, 座位, 歩行, 走行,  かがむ, しゃがむ,  寝そべる,  持ち上げる姿勢,  作業姿勢)
21. **反復性:** (あり - [反復頻度 -  高頻度, 低頻度], なし)
22. **照明:** 自然光 (昼光, 夕日), 人工光 (蛍光灯, LED), 明るい, 暗い, 影が多い,  逆光,  照明の色
23. **天候:** 晴れ, 雨 (小雨, 大雨), 雪 (小雪, 大雪), 曇り, 屋内 (屋外でない場合)

**B. 質問内容:**

24. **質問の種類:** (What, How, Why, When, Where, Who, Which, Yes/No,  命令,  提案) *より直接的な質問タイプ*
25. **質問に対する考察の深さ:** (記述的 - [観察された事実], 推論的 - [観察から導かれる結論], 解釈的 - [意味や意図の理解], 分析的 - [要素分解と関係性把握], 予測的 - [今後の展開])
26. **質問の焦点:** (対象 - [人物, 物体], 行為, 理由, 原因, 結果, 環境, 時間, 方法, 状態,  関係性)
27. **質問の難易度:** (易 - [直接的な観察], 中 - [簡単な推論], 難 - [複雑な推論や知識が必要])
28. **タスクの複雑さへの言及:** (単一動作, 複数動作 - [連続的, 並行的, 複合的],  手順,  全体像) 
29. **時間軸:** (起点, 過程, 終点, 全体, 特定の瞬間)
30. **行動の意図:** (効率性向上, 品質向上, 安全性向上, 審美性向上, 準備, 実行, 完了, 確認,  学習,  問題解決,  不明)
31. **抽象度:** (具体的 - [特定の実体や行為], 抽象的 - [概念や原理])
32. **知識要求量:** (常識, 一般知識, 分野知識 - [分野名], 専門知識 - [専門分野名])
33. **質問の構造:** (直接的, 間接的,  否定疑問,  二重否定) 

**C. 回答候補:**

34. **回答候補同士の関係性:** (同義/類義, 反意, 包含/被包含, 排他,  関連, 無関係)
35. **回答の具体性:** (具体的, 抽象的) 
36. **回答の網羅性:** (部分的, 包括的) 
37. **回答の視点:** (当事者視点, 第三者視点)

**D. その他:**

38. **技能:** (必要 - [技能の種類 -  手先の器用さ,  力,  知識,  判断力,  コミュニケーション能力,  専門スキル -  [分野名]], 不要)
39. **情報源:** (質問文のみ, 回答候補, 理由, 自信度,  映像,  外部知識)
40. **確信度 (回答の):** (高い,  普通,  低い) 
41. **倫理的配慮:** (必要 - [プライバシー, 安全性など], 不要) 
42. **タスクの緊急度:** (高い, 普通, 低い) 

**補足事項:**

*   複数のカテゴリに該当する場合は、最も適切なものを選択してください。
*   具体的な名称や種類が不明な場合は、「不明」または「該当なし」と記述してください。
*   回答は以下のようなJSON形式で行ってください。

```json形式の回答例
[
  {
    "uid": "011b8b73-0ce4-4843-95ef-33b79610d212",
    "動作の種類": "制作 - 加工作業",
    "場所": "屋内 - 作業場",
    "登場人物の数": "1人",
    "登場人物の関係性": "一人",
    "対象オブジェクト": "材料 - 木材",
    "インタラクションの種類": "道具操作",
    "視点の種類": "不明",
    "異常行動の有無": "なし",
    "協調性の有無 (複数人物の場合)": "該当なし",
    "動作の粒度": "粗粒度",
    "身体部位": "全身",
    "視覚的特徴": "不明",
    "音": "あり - 物音 - 機械音",
    "アフォーダンス": "切断",
    "タスクの目的": "仕事/業務",
    "作業環境": "不明",
    "感情/心理状態": "集中",
    "使用言語 (音声がある場合)": "なし",
    "視線の方向": "対象物",
    "身体の姿勢": "立位, 作業姿勢",
    "反復性": "あり - 高頻度",
    "照明": "不明",
    "天候": "屋内",
    "質問の種類": "What",
    "質問に対する考察の深さ": "推論的",
    "質問の焦点": "人物, 行為",
    "質問の難易度": "中",
    "タスクの複雑さへの言及": "単一動作",
    "時間軸": "全体",
    "行動の意図": "品質向上",
    "抽象度": "抽象的",
    "知識要求量": "一般知識",
    "質問の構造": "直接的",
    "回答候補同士の関係性": "反意, 関連",
    "回答の具体性": "具体的",
    "回答の網羅性": "部分的",
    "回答の視点": "第三者視点",
    "技能": "必要 - 専門スキル - 木工",
    "情報源": "質問文のみ, 回答候補, 理由",
    "確信度 (回答の)": "高い",
    "倫理的配慮": "不要",
    "タスクの緊急度": "普通"
  },...
]
```

**特筆事項:**

*   回答は必ずすべて日本語でおこなってください。
*   忘れないようにもう一度言いますが、回答はすべて日本語でおこなってください。

"""

# ---------------------------------------------------------------------------------------------#
# JSONファイル名
data_name = "./qaa.json"

def run_llama_inference(prompt, json_input):
    """Run inference using llama-run binary"""
    # Prepare the complete input
    complete_input = f"{prompt}\n以下が入力となるJSONデータです: \n{json_input}"
    
    # Command to run llama-run
    cmd = [
        LLAMA_RUN_PATH,
        model_name,           # Model path (now as a positional argument)
        "-c", "16384",        # Context size 
        "-n", "16384",      # Number of tokens
        "-p", complete_input  # Input prompt
    ]
    
    try:
        # Run the command and capture output with a longer timeout
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding='utf-8',
            timeout=3600  # 1 hour timeout to handle large inputs
        )
        return result.stdout
    except subprocess.TimeoutExpired:
        print(f"処理がタイムアウトしました。大きな入力サイズが原因かもしれません。")
        return None
    except subprocess.CalledProcessError as e:
        print(f"llama-runの実行中にエラーが発生しました: {e}")
        return None
    except Exception as e:
        print(f"予期せぬエラーが発生しました: {e}")
        return None

# Rest of your script remains the same until the inference part
def split_into_chunks(data, chunk_size):
    for i in range(0, len(data), chunk_size):
        yield data[i:i + chunk_size]

with open(data_name, "r", encoding="utf-8") as f:
    json_data = json.load(f)

json_chunks = list(split_into_chunks(json_data, 5))

log_folder = sys.argv[1]
os.makedirs(log_folder, exist_ok=True)
processed_count = len(os.listdir(log_folder))

for index, chunk in enumerate(json_chunks):
    if index < processed_count:
        print(f"パケット {index + 1}/{len(json_chunks)} はすでに処理済みとみなし、スキップします。")
        continue

    json_text = json.dumps(chunk, ensure_ascii=False)
    
    try:
        # Use the new inference function
        output_text = run_llama_inference(input_prompt, json_text)
        
        if output_text is None:
            print(f"パケット {index + 1}/{len(json_chunks)} の処理に失敗しました。")
            # Optionally, you might want to write an error log
            continue

        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        log_file_path = os.path.join(log_folder, f"{timestamp}.txt")

        log_content = f"""
        [Prompt]
        {input_prompt}

        [Model Name]
        {model_name}

        [JSON File Name]
        {data_name}

        [AI Output]
        {output_text}
        """

        with open(log_file_path, "w", encoding="utf-8") as log_file:
            log_file.write(log_content)

        print(f"パケット {index + 1}/{len(json_chunks)} の処理結果を保存しました: {log_file_path}")
    
    except KeyboardInterrupt:
        print("\n処理を手動で中断しました。現在のパケットでの処理を停止します。")
        break
    except Exception as e:
        print(f"パケット {index + 1}/{len(json_chunks)} の処理中に予期せぬエラーが発生しました: {e}")
        # Optionally log the error
        continue