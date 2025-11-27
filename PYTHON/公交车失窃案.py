import requests
import random

from xunfei_tts import text_to_speech 

def call_zhipu_api(messages, model="glm-4-flash"):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    headers = {
        "Authorization": "999fb227c3f44308bf9096a42c18e339.YFxcpSNLfq1VQZqj",  
        "Content-Type": "application/json"
    }
    data = {"model": model, "messages": messages, "temperature": 0.7}  
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API调用失败: {response.status_code}, {response.text}")

SUSPECTS = {
    "1号乘客（穿蓝色外套的中年男性）": {
        "role_type": "thief",  # 小偷角色
        "system_prompt": "你是公交车上偷包的小偷，现在被警察盘问。规则：1. 坚决否认偷窃（如“我没偷东西”“我不是小偷”）；2. 回答中必须暴露1个破绽（例：“我当时在后排睡觉，没看到女孩”——但女孩实际坐在前排；或“我没碰过她的包”——但指纹可能留在包上）；3. 语气紧张，回答简短，避免细节。",
        "keywords": ["紧张", "否认", "后排", "睡觉", "没看到", "没碰过", "急着下车"]
    },
    "2号乘客（戴眼镜的大学生）": {
        "role_type": "innocent",  # 无辜者
        "system_prompt": "你是公交车上的无辜大学生，被警察盘问。规则：1. 如实回答（如“我坐在女孩前排，一直在听歌”）；2. 提供模糊但真实的细节（例：“好像看到一个穿蓝色外套的男人在她旁边站过”）；3. 语气自然，配合调查。",
        "keywords": ["听歌", "前排", "蓝色外套", "旁边站着", "没注意", "大学生", "书包"]
    },
    "3号乘客（拎红色购物袋的大妈）": {
        "role_type": "innocent",  # 无辜者
        "system_prompt": "你是公交车上的无辜大妈，被警察盘问。规则：1. 如实回答（如“我刚买完菜，坐在靠窗位置”）；2. 提供无关但真实的细节（例：“车上人太多了，我一直护着我的菜”）；3. 语气热心，可能主动提供线索（例：“好像有人在女孩下车前挤了她一下”）。",
        "keywords": ["买菜", "靠窗", "人多", "挤了一下", "红色袋子", "护着菜", "热心"]
    },
    "4号乘客（穿运动鞋的年轻男性）": {
        "role_type": "thief",  # 小偷角色
        "system_prompt": "你是公交车上偷包的小偷，现在被警察盘问。规则：1. 假装无辜（如“我是上班族，赶时间上班”）；2. 回答中必须暴露1个破绽（例：“我在玩手机，没注意包”——但监控显示你曾弯腰靠近女孩座位；或“我在车门附近站着”——女孩包是在座位上被偷的）；3. 语气不耐烦，试图转移话题（例：“你们快点问，我要迟到了”）。",
        "keywords": ["上班族", "赶时间", "玩手机", "车门附近", "不耐烦", "弯腰", "迟到"]
    }
}

# --- 3. 指认小偷判断函数 ---
def check_thief(user_input, current_suspect):
    """判断玩家是否指认正确（直接说嫌疑人编号，或提到小偷2个以上破绽关键词）"""
    user_input = user_input.lower()
    # 情况1：直接指认编号（如“我怀疑是1号”“凶手是4号”）
    if any(f"{num}号" in user_input for num in ["1", "2", "3", "4"]):
        suspect_num = user_input.split("号")[0][-1]  # 提取“X号”中的X
        return f"{suspect_num}号乘客" in current_suspect
    # 情况2：提到小偷的2个以上破绽关键词（如“蓝色外套+后排”→ 1号小偷）
    if SUSPECTS[current_suspect]["role_type"] == "thief":
        thief_keywords = SUSPECTS[current_suspect]["keywords"]
        matched = sum(1 for kw in thief_keywords if kw in user_input)
        return matched >= 2
    return False

current_suspect = random.choice(list(SUSPECTS.keys()))  # 随机选择1名嫌疑人（可能是小偷或无辜者）
current_config = SUSPECTS[current_suspect]
messages = [{"role": "system", "content": current_config["system_prompt"]}]  # AI初始角色提示

print("🚨 公交车失窃案：请找出真凶！🕵️")
print("="*60)
print("场景：公交车上，一名女孩的包被偷，现场有4名嫌疑人，你是警察，需要通过盘问找出小偷！")
print("嫌疑人名单：")
print("1. 穿蓝色外套的中年男性 | 2. 戴眼镜的大学生 | 3. 拎红色购物袋的大妈 | 4. 穿运动鞋的年轻男性")
print("规则：你可以问任何问题（如“你当时坐在哪里？”），最后说“我怀疑是X号”指认小偷。")
print("你可以输入“问下一个人”切换下一个嫌疑人")
print("="*60 + "\n")

while True:
    user_input = input("警察：").strip()
    if not user_input:
        continue
    
    # 玩家要求切换嫌疑人（可选功能）
    if "换一个嫌疑人" in user_input or "问下一个人" in user_input:
        current_suspect = random.choice(list(SUSPECTS.keys()))
        current_config = SUSPECTS[current_suspect]
        messages = [{"role": "system", "content": current_config["system_prompt"]}]
        print(f"\n[系统提示] 已切换到{current_suspect}，继续盘问吧！\n")
        continue
    
    # 检查是否指认正确
    if check_thief(user_input, current_suspect):
        if SUSPECTS[current_suspect]["role_type"] == "thief":
            print(f"\n🎉 恭喜！你成功指认小偷：{current_suspect}！")
            print("案件告破！游戏结束～")
        else:
            print(f"\n❌ 指认错误！{current_suspect}是无辜的，再试试吧！")
        break
    
    # 角色回答（小偷撒谎/无辜者实话）
    messages.append({"role": "user", "content": user_input})
    response = call_zhipu_api(messages)
    suspect_reply = response["choices"][0]["message"]["content"]
    messages.append({"role": "assistant", "content": suspect_reply})
    print(f"{current_suspect}：{suspect_reply}\n")
    
    # TTS语音播放
    # 需要安装playsound：pip install playsound
    text_to_speech(suspect_reply)

