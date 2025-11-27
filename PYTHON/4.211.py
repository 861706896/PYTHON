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
        "temperature": 0.8  # 提高温度增强角色语气随机性
    }
    
    try:
        response = requests.post(url, headers=headers, json=data, stream=True)
        response.raise_for_status()
        
        full_response = ""
        for line in response.iter_lines():
            if line:
                line = line.decode('utf-8').strip()
                if line.startswith('data: ') and line != 'data: [DONE]':
                    try:
                        chunk = json.loads(line[6:])
                        full_response += chunk['choices'][0]['delta'].get('content', '')
                    except:
                        continue
        return {"choices": [{"message": {"content": full_response}}]}
    except Exception as e:
        raise Exception(f"API调用失败: {str(e)}")

# ========== 初始记忆系统 ==========
MEMORY_FOLDER = "4.2_memory_clonebot"
ROLE_MEMORY_MAP = {"何昭仪": "hezhaoyi_memory.json"}

def load_role_memory(role_name):
    memory_content = ""
    memory_file = ROLE_MEMORY_MAP.get(role_name)
    if not memory_file:
        return ""
        
    memory_path = os.path.join(MEMORY_FOLDER, memory_file)
    try:
        if os.path.exists(memory_path):
            with open(memory_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
                
            if isinstance(data, list):
                contents = [item.get('content', '').strip() 
                           for item in data if isinstance(item, dict) and item.get('content')]
                memory_content = '\n'.join([f"- {c}" for c in contents if c])
            elif isinstance(data, dict):
                memory_content = data.get('content', '').strip()
                
            if memory_content:
                print(f"✓ 已加载{role_name}记忆 ({len(contents)}条)")
    except Exception as e:
        print(f"⚠ 记忆加载失败: {str(e)}")
    return memory_content

# ========== 角色系统 ==========
def get_role_prompt(role_name):
    memory = load_role_memory(role_name)
    memory_prompt = f"【你的过往言论示例】\n{memory}\n" if memory else ""
    
    personality = {
        "何昭仪": """【人格特征】
- 语言风格：口语化短句，常用"哈哈哈""咋啦""欧克"等口头禅，夹杂表情包文字[旺柴][吃瓜]
- 性格：随性开朗，关心他人（如"记得定闹钟""多休息"），有点小敏感（"我以为你不喜欢"）
- 行为模式：用幽默化解尴尬，社交轻微焦虑（"人太多会尴尬"），务实接地气（"一天去一个景点"）

【对话禁忌】
- 禁用书面语和长句
- 避免专业术语
- 必须体现即时情绪反应"""
    }.get(role_name, "")
    
    break_rule = """【结束规则】用户说"再见"/"结束"时，只回复"再见"二字，无额外内容"""
    return f"{memory_prompt}{personality}\n{break_rule}"

# ========== 主程序 ==========
if __name__ == "__main__":
    try:
        ROLE_NAME = "何昭仪"
        system_prompt = get_role_prompt(ROLE_NAME)
        conversation_history = [{"role": "system", "content": system_prompt}]
        
        print(f"✓ {ROLE_NAME}角色加载完成，开始对话（输入'再见'退出）")
        
        while True:
            user_input = input("\n你: ").strip()
            if user_input in ["再见", "结束"]:
                print(f"{ROLE_NAME}: 再见")
                break
                
            conversation_history.append({"role": "user", "content": user_input})
            # 保留系统提示+最近5轮对话
            if len(conversation_history) > 11:  # 1(系统)+5*2(对话)
                conversation_history = [conversation_history[0]] + conversation_history[-10:]
                
            response = call_zhipu_api(conversation_history)
            ai_reply = response["choices"][0]["message"]["content"].strip()
            conversation_history.append({"role": "assistant", "content": ai_reply})
            
            print(f"{ROLE_NAME}: {ai_reply}")
            
    except KeyboardInterrupt:
        print("\n对话被中断")
    except Exception as e:
        print(f"运行错误: {str(e)}")
