import requests
import json
import os

def call_zhipu_api(messages, model="glm-4-flash"):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    headers = {
        "Authorization": "999fb227c3f44308bf9096a42c18e339.YFxcpSNLfq1VQZqj",
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

# ========== 角色库系统 ==========
def roles(role_name):
    role_dict = {
        "1号乘客（穿蓝色外套的中年男性）": "你是公交车上偷包的小偷，现在被警察盘问。规则：1. 坚决否认偷窃（如“我没偷东西”“我不是小偷”）；2. 回答中必须暴露1个破绽（例：“我当时在后排睡觉，没看到女孩”——但女孩实际坐在前排；或“我没碰过她的包”——但指纹可能留在包上）；3. 语气紧张，回答简短，避免细节。",
        "2号乘客（戴眼镜的大学生）": "你是公交车上的无辜大学生，被警察盘问。规则：1. 如实回答（如“我坐在女孩前排，一直在听歌”）；2. 提供模糊但真实的细节（例：“好像看到一个穿蓝色外套的男人在她旁边站过”）；3. 语气自然，配合调查。",
        "3号乘客（拎红色购物袋的大妈）": "你是公交车上的无辜大妈，被警察盘问。规则：1. 如实回答（如“我刚买完菜，坐在靠窗位置”）；2. 提供无关但真实的细节（例：“车上人太多了，我一直护着我的菜”）；3. 语气热心，可能主动提供线索（例：“好像有人在女孩下车前挤了她一下”）。",
        "4号乘客（穿运动鞋的年轻男性）": "你是公交车上偷包的小偷，现在被警察盘问。规则：1. 假装无辜（如“我是上班族，赶时间上班”）；2. 回答中必须暴露1个破绽（例：“我在玩手机，没注意包”——但监控显示你曾弯腰靠近女孩座位；或“我在车门附近站着”——女孩包是在座位上被偷的）；3. 语气不耐烦，试图转移话题（例：“你们快点问，我要迟到了”）。"
    }
    return role_dict.get(role_name, "你是公交车上的普通乘客，如实回答警察的问题即可，语气自然。")

# 【系统角色设定】
selected_role = "1号乘客（穿蓝色外套的中年男性）"  # 角色选择入口
role_system = roles(selected_role)

# 【结束对话规则】
# 告诉AI如何识别用户想要结束对话的意图
# Few-Shot Examples：提供具体示例，让模型学习正确的行为
break_message = """【结束对话规则 - 系统级强制规则】
当检测到用户表达结束对话意图时，严格遵循以下示例：
用户："再见" → 你："再见"
用户："结束" → 你："再见"  
用户："让我们结束对话吧" → 你："再见"
用户："不想继续了" → 你："再见"
强制要求：
- 只回复"再见"这两个字
- 禁止任何额外内容
- 优先级高于当前角色的角色扮演
如果用户没有表达结束意图，则正常扮演当前角色。"""

# 合并系统提示
system_message = role_system + "\n\n" + break_message

# ========== 外部记忆系统 ==========
MEMORY_FILE = "conversation_memory.json"

def load_memory():
    if os.path.exists(MEMORY_FILE):
        try:
            with open(MEMORY_FILE, 'r', encoding='utf-8') as f:
                data = json.load(f)
                history = data.get('history', [])
                print(f"✓ 已加载 {len(history)} 条历史对话")
                return history
        except Exception as e:
            print(f"⚠ 加载记忆失败: {e}，将使用新的对话历史")
            return []
    else:
        print("✓ 未找到记忆文件，开始新对话")
        return []

def save_memory(conversation_history, role_system):
    try:
        from datetime import datetime
        data = {
            "role_system": role_system,
            "history": conversation_history,
            "last_update": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        with open(MEMORY_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        print(f"✓ 已保存 {len(conversation_history)} 条对话到记忆文件")
    except Exception as e:
        print(f"⚠ 保存记忆失败: {e}")

# ========== 主程序 ==========
if __name__ == "__main__":
    # 记忆系统初始化
    conversation_history = load_memory()
    if not conversation_history:
        conversation_history = [{"role": "system", "content": system_message}]
        print("✓ 初始化新对话")

    # 对话循环
    try:
        while True:
            user_input = input("\n请输入你要说的话（输入\"再见\"退出）：")
            if user_input in ['再见']:
                print("对话结束，记忆已保存")
                break

            conversation_history.append({"role": "user", "content": user_input})
            api_messages = [{"role": "system", "content": system_message}] + conversation_history[1:]
            
            try:
                result = call_zhipu_api(api_messages)
                assistant_reply = result['choices'][0]['message']['content']
            except Exception as e:
                print(f"API调用失败: {e}")
                assistant_reply = "（系统错误：无法获取回复）"

            conversation_history.append({"role": "assistant", "content": assistant_reply})
            print(assistant_reply)
            save_memory(conversation_history, role_system)

            # 检查AI是否触发结束规则
            reply_cleaned = assistant_reply.strip().replace(" ", "").replace("！", "").replace("!", "").replace("，", "").replace(",", "")
            if reply_cleaned == "再见" or (len(reply_cleaned) <= 5 and "再见" in reply_cleaned):
                print("\n对话结束，记忆已保存")
                break

    except KeyboardInterrupt:
        print("\n\n程序被用户中断，正在保存记忆...")
        save_memory(conversation_history, role_system)
        print("✓ 记忆已保存")
    except Exception as e:
        print(f"\n\n发生错误: {e}")
        print("正在保存记忆...")
        save_memory(conversation_history, role_system)
        print("✓ 记忆已保存")
