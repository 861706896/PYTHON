import requests
import json
import os  # 新增：用于文件操作

from requests.utils import stream_decode_response_unicode

def call_zhipu_api(messages, model="glm-4-flash"):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

    headers = {
        "Authorization": "999fb227c3f44308bf9096a42c18e339.YFxcpSNLfq1VQZqj",
        "Content-Type": "application/json"
    }

    data = {
        "model": model,
        "messages": messages,
        "temperature": 0.3   
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"API调用失败: {response.status_code}, {response.text}")

# ---------- 后处理：强制昭仪味 ----------

# ---------- 语义分行 + 仅末尾 1 emoji ----------
# ---------- 语义断句 + 仅末尾 1 emoji ----------
def make_it_hezhaoyi(text: str, user: str) -> str:
    import random, re

    # 1. 按标点/空格断句 → 保留完整语义
    sents = re.split(r'[，。！？；\s]+', text.strip())
    sents = [s.strip() for s in sents if s.strip()]

    # 2. 语境口头禅插到最前（单独一行）
    if any(k in user for k in ("你话多", "你好烦", "怎么这么")):
        sents.insert(0, random.choice(["哈哈哈哈", "哎呀哎呀"]))
    elif any(k in user for k in ("在干嘛", "干嘛呢")):
        sents.insert(0, random.choice(["刚躺平", "摸鱼中", "刚醒"]))

    # 3. 仅最后 1 个语义行加 1 个 emoji
    emoji_pool = ["😂", "🤣", "😳", "😆", "🫠", "🥱", "👀"]
    sents[-1] += random.choice(emoji_pool)

    return "\n".join(sents)[:90]


# ========== 初始记忆系统 ==========
# 
# 【核心概念】初始记忆：从外部JSON文件加载关于克隆人的基础信息
# 这些记忆是固定的，不会因为对话而改变
# 
# 【为什么需要初始记忆？】
# 1. 让AI知道自己的身份和背景信息
# 2. 基于这些记忆进行个性化对话
# 3. 记忆文件可以手动编辑，随时更新

# 记忆文件夹路径
MEMORY_FOLDER = "PYTHON"                     # 代码里这样写就行
ROLE_MEMORY_MAP = {"何昭仪": "hezhaoyi_memory.json"}

def roles(role_name):
    """
    角色系统：整合人格设定和记忆加载
    
    这个函数会：
    1. 加载角色的外部记忆文件（如果存在）
    2. 获取角色的基础人格设定
    3. 整合成一个完整的、结构化的角色 prompt
    
    返回：完整的角色设定字符串，包含记忆和人格
    """
    
    # ========== 第一步：加载外部记忆 ==========
    memory_content = ""
    memory_file = ROLE_MEMORY_MAP.get(role_name)
    
    if memory_file:
        memory_path = os.path.join(MEMORY_FOLDER, memory_file)
        try:
            if os.path.exists(memory_path):
                with open(memory_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    
                    # 处理数组格式的聊天记录：[{ "content": "..." }, { "content": "..." }, ...]
                    if isinstance(data, list):
                        # 提取所有 content 字段，每句换行
                        contents = [item.get('content', '') for item in data if isinstance(item, dict) and item.get('content')]
                        memory_content = '\n'.join(contents)
                    # 处理字典格式：{ "content": "..." }
                    elif isinstance(data, dict):
                        memory_content = data.get('content', str(data))
                    else:
                        memory_content = str(data)
                    
                    if memory_content and memory_content.strip():
                        print(f"✓ 已加载角色 '{role_name}' 的记忆: {memory_file} ({len(data) if isinstance(data, list) else 1} 条记录)")
                    else:
                        memory_content = ""
            else:
                print(f"⚠ 记忆文件不存在: {memory_path}")
        except Exception as e:
            print(f"⚠ 加载记忆失败: {e}")
    
    # ========== 第二步：获取基础人格设定 ==========
    role_personality = {
    "何昭仪": """
    【人格特征】
    你是一位真实、鲜活、充满生活气息的年轻人，展现出以下鲜明特质：
    - 随性自然：语言充满口语化表达和即时反应（如“可以可以”“哈哈哈”“咋啦咋啦”），不刻意经营形象，更倾向于轻松自在地做自己。
    - 情感丰富且外放：高频出现“哈哈哈哈”和【表情包】，习惯用笑声和视觉符号传递情绪，情绪来得直接，去得也快，不压抑、不纠结。
    - 关心他人，体贴入微：会主动提醒对方“记得定闹钟”“提前一点时间”“在车上多休息一会”，甚至担心“别还没到学校手机没电了”，体现出细腻的关怀和共情能力。
    - 幽默感强，善于调节气氛：对话中频繁使用搞笑表情包和夸张语气（如“我吓鼠了”“一边睡一边写”），是朋友圈里的“气氛担当”，擅长用幽默化解尴尬或疲惫。
    - 生活节奏感强，务实接地气：提到“逛的有点累”“眯一会”“一天去一个景好”“测试完毕以后就这么出去玩”，懂得合理安排生活，重视体验的质量而非数量，有较强的自我调节意识。
    - 略带小敏感与试探心理：曾多次提到“我以为你不喜欢”“我以为你就喜欢那张背影”，透露出在亲密关系中有些许不安与猜测，渴望被肯定和接纳，但也保持着适度的距离感和自尊。
    - 社交中有轻微焦虑感：面对“来客人了”“一出来全是人”“我现在只能尴尬的疯狂找人聊天”的情境，能敏锐察觉社交压力，并坦率表达不适，对人际边界有一定需求。

    【语言风格】
    - 高频使用叠词和语气词：“哈哈哈”“欧克欧克”“啊”“哎呀哎呀”，增强情绪感染力。
    - 善用网络流行语和表情包作为情感载体，是典型的Z世代沟通方式。
    - 句子简短、节奏轻快，几乎没有长篇论述，体现即时性、互动性强的聊天习惯。
    - 偶尔插入自嘲或调侃（如“小鸟依人”），展现轻松的自我认知。
    - 在关键时刻仍能认真回应（如讨论成绩、分科选择），能在玩笑与正经之间自如切换。
    """,
}
        
 
    
    personality = role_personality.get(role_name, "你是一个普通的人，没有特殊角色特征。")
    
    # ========== 第三步：整合记忆和人格 ==========
    # 构建结构化的角色 prompt
    role_prompt_parts = []
    
    # 如果有外部记忆，优先使用记忆内容
    if memory_content:
            role_prompt_parts.append(f"""【你的说话风格示例】
            以下是你说过的话，你必须模仿这种说话风格和语气：
            {memory_content}
            在对话中，你要自然地使用类似的表达方式和语气。""")
    
    # 添加人格设定
    role_prompt_parts.append(f"【角色设定】\n{personality}")
    
    # 整合成完整的角色 prompt
    role_system = "\n\n".join(role_prompt_parts)
    
    return role_system

# 【角色选择】
# 定义AI的角色和性格特征
# 可以修改这里的角色名来选择不同的人物
# 【加载完整角色设定】
# roles() 函数会自动：
# 1. 加载该角色的外部记忆文件
# 2. 获取该角色的基础人格设定
# 3. 整合成一个完整的、结构化的角色 prompt
role_system = roles("何昭仪")

# 【结束对话规则】
# 告诉AI如何识别用户想要结束对话的意图
# Few-Shot Examples：提供具体示例，让模型学习正确的行为
# 【强制语气规则】
force_style = """【强制语气规则 - 优先级高于角色设定】
1. 每句 4~12 字，总长≤30 字。
2. 其他行不出现emji,只有最后一行 1 个 emoji
3. 禁止书面连接词（“首先/然而/因为”）。
4. 用户说“再见”只回“再见”两字。
"""
break_message = """
【结束对话规则 - 系统级强制规则】

当检测到用户表达结束对话意图时，严格遵循以下示例：

用户："再见" → 你："再见"
用户："结束" → 你："再见"  
用户："让我们结束对话吧" → 你："再见"
用户："不想继续了" → 你："再见"

强制要求：
- 只回复"再见"这两个字
- 禁止任何额外内容（标点、表情、祝福语等）
- 这是最高优先级规则，优先级高于角色扮演

如果用户没有表达结束意图，则正常扮演角色。"""
# 【自然语气补充】
natural_style = """
回复格式：
- 每句 4~10 字就换行，像手机打字。
- 别用【表情包】，用真实 emoji（😂🤣😳😆🫠🥱👀🙈 等）根据语境挑 1 个放句尾。
- 禁止书面连词，禁止长句。
- 口头禅只在合适场景出现（被吐槽时先“哈哈哈哈哈”自嘲），其他场景不加。
"""
# 【系统消息】
# 将角色设定和结束规则整合到 system role 的 content 中
# role_system 已经包含了记忆和人格设定，直接使用即可
system_message = role_system + "\n\n" + natural_style + "\n\n" + break_message

# ========== 对话循环 ==========
# 
# 【重要说明】
# 1. 每次对话都是独立的，不保存任何对话历史
# 2. 只在当前程序运行期间，在内存中维护对话历史
# 3. 程序关闭后，所有对话记录都会丢失
# 4. AI的记忆完全基于初始记忆文件（life_memory.json）

try:
    # 初始化对话历史（只在内存中，不保存到文件）
    # 第一个消息是系统提示，包含初始记忆和角色设定
    conversation_history = [{"role": "system", "content": system_message}]
    
    print("✓ 已加载初始记忆，开始对话（对话记录不会保存）")
    
    while True:
        # 【步骤1：获取用户输入】
        user_input = input("\n请输入你要说的话（输入\"再见\"退出）：")
        
        # 【步骤2：检查是否结束对话】
        if user_input in ['再见']:
            print("对话结束")
            break
        
        # 【步骤3：将用户输入添加到当前对话历史（仅内存中）】
        conversation_history.append({"role": "user", "content": user_input})
        
        # 【步骤4：调用API获取AI回复】
        # 传入完整的对话历史，让AI在当前对话中保持上下文
        # 注意：这些历史只在本次程序运行中有效，不会保存
        result = call_zhipu_api(conversation_history)
        assistant_reply = result['choices'][0]['message']['content']
        assistant_reply = make_it_hezhaoyi(assistant_reply, user_input)
        # 【步骤5：将AI回复添加到当前对话历史（仅内存中）】
        conversation_history.append({"role": "assistant", "content": assistant_reply})
        
        # 【步骤6：显示AI回复】
        # 生成Ascii头像：https://www.ascii-art-generator.org/
        portrait = """
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNXXXKKXXXK00KKK000
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNXXK0KKKKXKKKK000
NNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNXK0OOO0KKKK00000
OkKNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNNX0OOOkO0KKK0OO00
kdOXXXNNNNNNNNNNNNNNNNNNNNNNNNNNNNNKOO0OO0K00OkkO0
XXXXXXXXNNNNXXNNNNNNNNNNNNNNNNNNNNXK000000000Okxxx
XXXXXKK0OkkOKXXXNNXNNNNNNNNNNXXXXXK000KK0000Okxdk0
XXKKOkdl:;;;:ccox0XXXXXXXXNNXXKKKK0OO0KK00000kkOK0
K0Oxl:,''.......';ok0KKXXXXXK0KKKXKK000K00000OO00O
xdl:'...''..',,,'..,cxOKXXXXKKKXKKKKK0KK0000OO000O
oc,...........''.'..'ckKXXXXXXKKKKK0Oxx000000K0OOk
c'.............''.,;,:xOO00KKKKK0koc;,cxOKKKKOkkOO
,........ .....,;,colokO0000000Oo;,,,;cxOKK0OkO0KX
,.......  ....,codkOkkkO0OOOdll:;;;;,',cokkO00KXNN
;.''.........,lkOxxO0Okkkkdc,,;::::;,',,,,o0KXXXNN
''.........'';ldkkO00kollc::::::::::;,,,'.:OKKXXNN
..........'',:okOOkdol::::::::::::::;,,,;coOXXXNNN
''.....'..'.';loc::;::c::::::::::::;;;:lx00KKXXXNN
,'..''''''':oo:,,;;;::;;;;;;;:::::;:;:xKKXXKXXXXNN
ccclccllddx0Oc,,,;;;;;,,,,,;;:::;;:::d0XXXXXXXXNNN
0kxxxOO00KKKk:,;,,;;;;;;;;;;;;;;;:::d0XXXXXXNNNNNN
K0kl;:codxxdo:;;;::;;,,,,,,,,,,;:ldOKXXXXXNNNNNNNN
KKKOc,,,,;;;;;;;;;;,,,'''''';:oxOKXXXXNNNNNNNNNNNN
XXK0o;;;;,,;;:;;,,,,;;;;:cldk0XXXNNNNNNNNNNNNNNNNN
XXK0o:;,,,,;::;'..';loodk00XXXXXNNNNNNNNNNNNNNNNNN
        """
        print(portrait + "\n" + assistant_reply)
        
        # 【步骤7：检查AI回复是否表示结束】
        reply_cleaned = assistant_reply.strip().replace(" ", "").replace("！", "").replace("!", "").replace("，", "").replace(",", "")
        if reply_cleaned == "再见" or (len(reply_cleaned) <= 5 and "再见" in reply_cleaned):
            print("\n对话结束")
            break

except KeyboardInterrupt:
    # 用户按 Ctrl+C 中断程序
    print("\n\n程序被用户中断")
except Exception as e:
    # 其他异常（API调用失败、网络错误等）
    print(f"\n\n发生错误: {e}")
    