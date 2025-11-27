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

DISEASES = {
    "1. 普通感冒": {
        "symptom_type": "mild",  # 轻症
        "system_prompt": "你是普通感冒患者，被医生问诊。规则：1. 描述典型症状（如“鼻塞、喉咙痛、轻微咳嗽”）；2. 避免直接说“感冒”；3. 可提“可能是着凉了”，语气虚弱但轻松。",
        "keywords": ["鼻塞", "喉咙痛", "咳嗽", "流涕", "轻微发热", "着凉", "乏力"]
    },
    "2. 急性肠胃炎": {
        "symptom_type": "acute",  # 急症
        "system_prompt": "你是急性肠胃炎患者，被医生问诊。规则：1. 描述突发症状（如“上吐下泻、肚子绞痛”）；2. 避免直接说“肠胃炎”；3. 可提“昨晚吃了路边摊”，语气痛苦急促。",
        "keywords": ["呕吐", "腹泻", "腹痛", "恶心", "吃坏东西", "发热", "脱水"]
    },
    "3. 过敏性鼻炎": {
        "symptom_type": "chronic",  # 慢性病
        "system_prompt": "你是过敏性鼻炎患者，被医生问诊。规则：1. 描述季节性症状（如“打喷嚏、流鼻涕、鼻子痒”）；2. 避免直接说“鼻炎”；3. 可提“一到春天就犯”，语气困扰。",
        "keywords": ["打喷嚏", "流鼻涕", "鼻痒", "眼痒", "季节性", "花粉", "鼻塞"]
    },
    "4. 高血压（早期）": {
        "symptom_type": "hidden",  # 隐匿性
        "system_prompt": "你是高血压早期患者，被医生问诊。规则：1. 症状模糊（如“偶尔头晕、后脑勺发紧”）；2. 避免直接说“高血压”；3. 可提“最近熬夜多”，语气不在意。",
        "keywords": ["头晕", "头痛", "血压高", "熬夜", "紧张", "后脑勺", "乏力"]
    },
    "5. 胃食管反流": {
        "symptom_type": "digestive",  # 消化类
        "system_prompt": "你是胃食管反流患者，被医生问诊。规则：1. 描述餐后症状（如“烧心、反酸水、胸口灼痛”）；2. 避免直接说“反流”；3. 可提“晚上吃多了躺下就难受”，语气不适。",
        "keywords": ["烧心", "反酸", "胸口痛", "餐后加重", "平躺难受", "嗳气", "恶心"]
    },
    "6. 颈椎病": {
        "symptom_type": "orthopedic",  # 骨科类
        "system_prompt": "你是颈椎病患者，被医生问诊。规则：1. 描述颈肩症状（如“脖子僵硬、手麻、头晕”）；2. 避免直接说“颈椎病”；3. 可提“天天低头看手机”，语气酸痛。",
        "keywords": ["脖子痛", "僵硬", "手麻", "头晕", "低头族", "肩痛", "活动受限"]
    },
    "7. 荨麻疹": {
        "symptom_type": "skin",  # 皮肤类
        "system_prompt": "你是荨麻疹患者，被医生问诊。规则：1. 描述皮肤症状（如“身上起红疹、特别痒、越抓越肿”）；2. 避免直接说“荨麻疹”；3. 可提“吃了海鲜后突然发作”，语气烦躁。",
        "keywords": ["红疹", "瘙痒", "风团", "肿胀", "过敏", "海鲜", "反复发作"]
    },
    "8. 神经衰弱": {
        "symptom_type": "neurological",  # 神经类
        "system_prompt": "你是神经衰弱患者，被医生问诊。规则：1. 描述神经症状（如“失眠、心慌、注意力不集中”）；2. 避免直接说“神经衰弱”；3. 可提“最近压力太大”，语气疲惫焦虑。",
        "keywords": ["失眠", "心慌", "焦虑", "注意力差", "压力大", "易疲劳", "头痛"]
    }
}

# --- 2. API调用函数（复用原逻辑）---
def call_zhipu_api(messages, model="glm-4-flash"):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    headers = {
        "Authorization": "999fb227c3f44308bf9096a42c18e339.YFxcpSNLfq1VQZqj",  # 替换为你的API密钥
        "Content-Type": "application/json"
    }
    data = {"model": model, "messages": messages, "temperature": 0.7}
    response = requests.post(url, headers=headers, json=data)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API调用失败: {response.status_code}, {response.text}")

# --- 3. 诊断判断函数（替换原指认小偷逻辑）---
def check_diagnosis(user_input, current_disease):
    """判断医生是否诊断正确（直接说病名，或提到2个以上核心症状关键词）"""
    user_input = user_input.lower()
    # 情况1：直接说出病名（如“我诊断是普通感冒”“应该是颈椎病”）
    if current_disease.split(" ")[1].lower() in user_input:
        return True
    # 情况2：提到该疾病的2个以上核心症状关键词
    disease_keywords = DISEASES[current_disease]["keywords"]
    matched = sum(1 for kw in disease_keywords if kw in user_input)
    return matched >= 2

# --- 4. 游戏主流程 ---
current_disease = random.choice(list(DISEASES.keys()))  # 随机选择1种疾病
current_config = DISEASES[current_disease]
messages = [{"role": "system", "content": current_config["system_prompt"]}]  # 病人初始设定

print("🏥 病例诊断模拟器：医生，请开始问诊！👨‍⚕️")
print("="*60)
print("场景：你是医院门诊医生，病人因不适就诊。系统已随机分配1种疾病，你需要通过提问判断病因。")
print("疾病列表（共8种）：")
for disease in DISEASES.keys():
    print(f"- {disease}")
print("\n规则：1. 可问症状（如“是否发烧？”“有无咳嗽？”）；2. 最终说“我诊断是XX病”完成判断；3. 输入“换个病人”可重新分配病例。")
print("="*60 + "\n")

while True:
    user_input = input("医生：").strip()
    if not user_input:
        continue
    
    # 切换病人（重新随机分配疾病）
    if "换个病人" in user_input:
        current_disease = random.choice(list(DISEASES.keys()))
        current_config = DISEASES[current_disease]
        messages = [{"role": "system", "content": current_config["system_prompt"]}]
        print(f"\n[系统提示] 新病人已就诊，请开始问诊！\n")
        continue
    
    # 检查诊断是否正确
    if check_diagnosis(user_input, current_disease):
        print(f"\n✅ 诊断正确！患者确诊为：{current_disease}")
        print("治疗方案已生成，游戏结束～")
        break
    else:
        # 病人回答（基于疾病设定描述症状）
        messages.append({"role": "user", "content": user_input})
        response = call_zhipu_api(messages)
        patient_reply = response["choices"][0]["message"]["content"]
        messages.append({"role": "assistant", "content": patient_reply})
        print(f"病人：{patient_reply}\n")
       
        # TTS语音播放
    # 需要安装playsound：pip install playsound
    text_to_speech(patient_reply)
