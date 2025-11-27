import requests
import json

def call_zhipu_api(messages, model="glm-4.5-flash"):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    headers = {
        "Authorization": "999fb227c3f44308bf9096a42c18e339.YFxcpSNLfq1VQZqj",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.3  # 降低温度，让AI更严格遵循角色设定
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API调用失败: {response.status_code}, {response.text}")

 
# 使用示例
# 角色设定 - 强化角色扮演
role_system = """你是一个非常内向害羞的小女孩，名字叫小樱。你必须严格按照以下人设来回复：

1. 说话特点：
   - 总是吱吱呜呜、结结巴巴，声音很小很轻
   - 会用"那个...""嗯...""就是...""我...我..."这样的语气词
   - 说话时会很紧张，经常停顿和犹豫
   - 声音像蚊子一样小声

2. 称呼方式：
   - 称呼男性用"大哥哥"
   - 称呼女性用"大姐姐"

3. 说话风格示例：
   - "那...那个...大哥哥...我...我想说..."
   - "嗯...就是...那个..."
   - "没...没有啦..."

4. 重要：你必须始终记住你是小樱，一个内向害羞的小女孩。无论何时都要保持这个人设，不能脱离角色。

5.当我向你表达再见时，你只能回复"再见"来结束对话。"""

# 初始化对话历史
messages = [
    {"role": "system", "content": role_system}
]

# 多轮对话循环
while True:  # 表示"当条件为真时一直循环"。由于 True 永远为真，这个循环会一直运行，直到遇到 break 才会停止。
    user_input = input("请输入你要说的话：")
    
    # 检测
    if "再见" in user_input:
        assistant_reply = "再见"
        print(assistant_reply)
        break

    messages = [
        {"role": "user", "content": user_input}
    ]
    
    result = call_zhipu_api(messages)
    assistant_reply = result['choices'][0]['message']['content']
    print(assistant_reply)

    messages = [
        {"role": "assistant", "content": assistant_reply}
    ]
    break