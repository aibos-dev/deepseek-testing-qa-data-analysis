#!/bin/bash

# save folder name
folder_name=$1

while true
do
    echo "Pythonスクリプトを起動します..."

    python put_label.py "$folder_name"

    # Pythonスクリプトの終了コードで正常 / 異常を判定
    if [ $? -ne 0 ]; then
        echo "エラー終了を検知。5秒後に再起動します..."
        sleep 5
    else
        python merge.py "$folder_name"
        python count.py "$folder_name"
        echo "正常終了しました。ループを抜けます..."
        break
    fi


done
