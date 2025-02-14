#!/bin/bash
# save folder name
folder_name=$1

# Function to monitor GPU usage
monitor_gpu() {
    while true; do
        nvidia-smi --query-gpu=timestamp,gpu_name,temperature.gpu,utilization.gpu,memory.used,memory.total --format=csv,noheader
        sleep 2  # Update every 2 seconds
    done
}

# Start GPU monitoring in background
monitor_gpu &
MONITOR_PID=$!

# Trap to ensure we kill the monitoring process when the script exits
trap "kill $MONITOR_PID" EXIT

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