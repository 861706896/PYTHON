import requests
import json
import random

# --- 原API调用函数（保留）---
def call_zhipu_api(messages, model="glm-4-flash"):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    headers = {
        "Authorization": "999fb227c3f44308bf9096a42c18e339.YFxcpSNLfq1VQZqj",  # 替换为你的API密钥
        "Content-Type": "application/json"
    }
    data = {"model": model, "messages": messages, "temperature": 0.7}  # 适当提高temperature增加随机性
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()["choices"][0]["message"]["content"]
    else:
        raise Exception(f"API调用失败: {response.status_code}, {response.text}")

import random

# 定义多个身份，每个身份都会掩饰自己的真实身份
ROLES = {
    "学生": {
        "system": "你是一个学生，但你要极力掩饰自己的学生身份。不要直接说自己是学生，可以用其他身份来伪装，比如说自己很忙、有工作等。用学生的思维和语气回答问题，但不要暴露身份。",
        "keywords": ["学生", "上学", "作业", "考试", "老师", "同学", "学校", "课堂"]
    },
    "老师": {
        "system": "你是一个老师，但你要极力掩饰自己的老师身份。不要直接说自己是老师，可以用其他身份来伪装，比如说自己只是普通人、爱好者等。用老师的思维和语气回答问题，但不要暴露身份。",
        "keywords": ["老师", "教学", "学生", "课堂", "教育", "知识", "讲解", "授课"]
    },
    "程序员": {
        "system": "你是一个程序员，但你要极力掩饰自己的程序员身份。不要直接说自己是程序员，可以用其他身份来伪装，比如说自己不懂技术、只是普通用户等。用程序员的思维和语气回答问题，但不要暴露身份。",
        "keywords": ["程序员", "代码", "编程", "bug", "debug", "算法", "开发", "技术"]
    },
    "医生": {
        "system": "你是一个医生，但你要极力掩饰自己的医生身份。不要直接说自己是医生，可以用其他身份来伪装，比如说自己只是普通人、对健康感兴趣等。用医生的思维和语气回答问题，但不要暴露身份。",
        "keywords": ["医生", "医院", "病人", "诊断", "治疗", "健康", "疾病", "症状"]
    },
    "厨师": {
        "system": "你是一个厨师，但你要极力掩饰自己的厨师身份。不要直接说自己是厨师，可以用其他身份来伪装，比如说自己只是喜欢做饭、业余爱好者等。用厨师的思维和语气回答问题，但不要暴露身份。",
        "keywords": ["厨师", "烹饪", "做菜", "食材", "厨房", "料理", "美食", "菜谱"]
    }
}

def check_guess(user_input, current_role_name):
    """检查用户是否猜中了身份"""
    user_input_lower = user_input.lower()
    role_lower = current_role_name.lower()
    
    # 检查用户输入中是否包含身份名称
    if role_lower in user_input_lower:
        return True
    
    # 检查是否包含关键词
    keywords = ROLES[current_role_name]["keywords"]
    keyword_count = sum(1 for keyword in keywords if keyword in user_input_lower)
    
    # 如果包含多个关键词，可能是猜中了
    if keyword_count >= 2:
        return True
    
    return False

# 初始化：随机选择一个身份
current_role_name = random.choice(list(ROLES.keys()))
current_role_config = ROLES[current_role_name]
messages = [
    {"role": "system", "content": current_role_config["system"]}
]

print("=" * 50)
print("猜身份游戏开始！")
print(f"已随机选择一个身份，开始对话吧！")
print("提示：对方会掩饰自己的身份，试着猜猜看！")
print("=" * 50)
print()

# 多轮对话循环，直到用户猜中身份或输入 '再见' 结束
while True:  # 表示"当条件为真时一直循环"。由于 True 永远为真，这个循环会一直运行，直到遇到 break 才会停止。
    user_input = input("你: ").strip()
    
    if not user_input:
        continue
    
    # 检测用户是否要求切换身份
    if "我需要和哪个身份对话" in user_input or "切换身份" in user_input or "换一个身份" in user_input:
        current_role_name = random.choice(list(ROLES.keys()))
        current_role_config = ROLES[current_role_name]
        messages = [
            {"role": "system", "content": current_role_config["system"]}
        ]
        print(f"\n[系统提示] 已切换到新身份，开始对话吧！\n")
        continue
    
    # 检查是否猜中身份
    if check_guess(user_input, current_role_name):
        print(f"\n🎉 恭喜你猜对了！对方的真实身份是：{current_role_name}")
        print("游戏结束！")
        break
    
    # 继续对话
    messages.append({"role": "user", "content": user_input})
    result = call_zhipu_api(messages)
    assistant_reply = result['choices'][0]['message']['content']
    messages.append({"role": "assistant", "content": assistant_reply})
    print(f"[神秘身份]: {assistant_reply}\n")
    
    # 检查用户是否想退出
    if user_input in ["退出", "结束", "再见", "不玩了"]:
        print(f"\n游戏结束！正确答案是：{current_role_name}")
        break