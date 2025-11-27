import requests
import json
import random

from requests.utils import stream_decode_response_unicode
from xunfei_tts import text_to_speech

def call_zhipu_api(messages, model="glm-4-flash"):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    headers = {
        "Authorization":"3c5630491548431d8eb87422cd9bbf81.Wm2BfMEkf6STJARm",
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

# 游戏设置
role_system = ["太阳","月亮"]
current_role = random.choice(role_system)

# 系统提示词
game_system = f"""你正在玩"谁是卧底"游戏。你的身份是：{current_role}

游戏规则：
1. 用户会通过提问来猜测你的身份
2. 你要通过描述自己的特征、感受、处境来暗示，但绝对不能直接说出"{current_role}"这个词
3. 不要直接回答"是"或"否"，而是通过描述特征让用户自己判断
4. 不要说"我不是XX"这种直接否定，而是说"我更像是..."来描述
5. 不要提及其他可能的身份选项
6. 当用户准确说出"{current_role}"这个词时，你只回复"我不是"来结束游戏
7. 保持神秘感，让游戏有趣

角色特征提示:
- 如果是"太阳":强调发光发热、白天出现、温暖、能源来源
- 如果是"月亮":强调夜晚出现、反射光、圆形变化、影响潮汐
回答示例：
- 用户问"你白天出现吗？"
  太阳回答："我每天都会升起，带来光明和温暖"
  月亮回答："我更常在夜晚出现，用柔和的光照亮大地。"

- 用户问"你会发光吗？"  
  太阳回答："我是光和热的主要来源"
  月亮回答："我本身不发光，但能反射别人的光"

现在开始游戏，用户会开始提问。保持角色，通过描述特征来暗示，不要直接否定或肯定。"""

# 维护对话历史
conversation_history = [
    {"role": "system", "content": game_system}
]

# 显示游戏开始信息
print("=" * 60)
print("游戏开始！")
print(f"你的身份是：{current_role}")
print("=" * 60)
print("\n系统提示词：")
print(game_system)
print("=" * 60)
print("\n开始游戏，请输入你的问题...\n")

# 多轮对话循环
while True:
    user_input = input("请输入你要说的话：")
    
    # 添加用户消息到历史
    conversation_history.append({"role": "user", "content": user_input})
    
    # 调用API
    result = call_zhipu_api(conversation_history)
    assistant_reply = result['choices'][0]['message']['content']
    
    
    # 添加助手回复到历史（使用原始文本，不是函数返回值）
    conversation_history.append({"role": "assistant", "content": assistant_reply})
    
    # 打印回复
    print(assistant_reply)
    text_to_speech(assistant_reply)
    
    # 检查是否猜对（模型回复"再见"）
    if "再见" in assistant_reply:
        print(f"\n游戏结束！正确答案是：{current_role}")
        break