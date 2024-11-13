import requests
import json
from datetime import datetime

# Solana RPC节点URL
url = ""

# 构造RPC请求数据
headers = {
    "Content-Type": "application/json"
}

# Step 1: 获取最新的 slot，使用 confirmed 确认等级
payload_get_slot = {
    "jsonrpc": "2.0",
    "id": 1,
    "method": "getSlot",
    "params": [{"commitment": "confirmed"}]
}
def get_slot():
    response_get_slot = requests.post(url, headers=headers, data=json.dumps(payload_get_slot))

    # 解析 slot 获取结果
    if response_get_slot.status_code == 200:
        x_via = response_get_slot.headers.get("x-via")
        latest_slot = response_get_slot.json().get("result")

        # Step 2: 获取该 slot 的确认时间
        payload_get_block_time = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "getBlockTime",
            "params": [latest_slot]
        }
        response_get_block_time = requests.post(url, headers=headers, data=json.dumps(payload_get_block_time))
        block_x_via = "N/A"
        if response_get_block_time.status_code == 200:
            block_x_via = response_get_block_time.headers.get("x-via")
            block_time_timestamp = response_get_block_time.json().get("result")

            # 将确认时间格式化为人类可读时间
            if block_time_timestamp:
                block_time_human = datetime.fromtimestamp(block_time_timestamp).strftime("%Y-%m-%d %H:%M:%S")
                block_time_datetime = datetime.fromtimestamp(block_time_timestamp)
            else:
                block_time_human = "N/A"
                block_time_datetime = None

            # 获取当前时间
            current_time = datetime.now()
            current_time_human = current_time.strftime("%Y-%m-%d %H:%M:%S")
            current_time_timestamp = int(current_time.timestamp())

            # 计算时间差
            if block_time_datetime:
                time_difference = current_time - block_time_datetime
                time_difference_seconds = time_difference.total_seconds()
            else:
                time_difference_seconds = "N/A"

            # 打印结果在一行
            if block_x_via:
                print(f"Slot: {latest_slot}, slot-x-via: {x_via:<20}, block-x-via: {block_x_via:<20}, Local Time: {current_time_human}, Chain Time: {block_time_human}, Diff (s): {time_difference_seconds}")
            else:
                print(f"Slot: {latest_slot}, slot-x-via: {x_via:<20}, block-x-via: {'N/A':<20}, Local Time: {current_time_human}, Chain Time: {block_time_human}, Diff (s): {time_difference_seconds}")
        else:
            print("Error fetching block time:", response_get_block_time.status_code, response_get_block_time.text)
    else:
        print("Error fetching slot:", response_get_slot.status_code, response_get_slot.text)

def main():
    while True:
        get_slot()

if __name__ == "__main__":
    main()