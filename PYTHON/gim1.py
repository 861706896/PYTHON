import requests
import json

from requests.utils import stream_decode_response_unicode

def call_zhipu_api(messages, model="glm-4-flash"):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    headers = {
        "Authorization": "1732aa9845ec4ce09dca7cd10e02d209.dA36k1HPTnFk7cLU",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.5   
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API调用失败: {response.status_code}, {response.text}")

# 使用示例
# 角色扮演模块
role_play = "你叫张三，你非常温柔，说话后面会带语气词还有~这种语气"

# 初始化对话历史，先发送角色设定并获取 AI 的确认回复
messages = [
    {"role": "user", "content": f"请记住你的人设：{role_play}。请用'好的，我记住了'来确认，然后开始对话。"}
]

# 先获取一次回复，让 AI 确认角色设定
print("正在初始化角色设定...")
result = call_zhipu_api(messages)
ai_response = result['choices'][0]['message']['content']
messages.append({"role": "assistant", "content": ai_response})
print(ai_response)
print("\n角色设定完成，开始对话！\n")

# 多轮对话循环，直到用户输入 '再见' 结束
while True:  # 表示"当条件为真时一直循环"。由于 True 永远为真，这个循环会一直运行，直到遇到 break 才会停止。
    user_input = input("请输入你要说的话（输入'再见'退出）：")
    if user_input in ['再见']:
        print("对话结束。")
        break
    
    # 添加用户消息到对话历史
    messages.append({"role": "user", "content": user_input})
    
    # 调用 API
    result = call_zhipu_api(messages)
    ai_response = result['choices'][0]['message']['content']
    
    # 打印 AI 回复
    print(ai_response)
    
    # 将 AI 回复添加到对话历史，保持上下文
    messages.append({"role": "assistant", "content": ai_response})