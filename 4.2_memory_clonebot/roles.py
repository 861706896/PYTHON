import json
import os

# 记忆配置
MEMORY_FOLDER = "PYTHON"
ROLE_MEMORY_MAP = {"何昭仪": "hezhaoyi_memory.json"}

def load_role_memory(role_name):
    """加载角色外部记忆文件"""
    memory_content = ""
    memory_file = ROLE_MEMORY_MAP.get(role_name)
    if memory_file:
        memory_path = os.path.join(MEMORY_FOLDER, memory_file)
        try:
            if os.path.exists(memory_path):
                with open(memory_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    if isinstance(data, list):
                        contents = [item.get('content', '') for item in data if isinstance(item, dict) and item.get('content')]
                        memory_content = '\n'.join(contents)
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
    return memory_content

def get_role_personality(role_name):
    """获取角色基础人格设定"""
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
    return role_personality.get(role_name, "你是一个普通的人，没有特殊角色特征。")

def build_role_system(role_name):
    """整合记忆和人格，构建完整角色设定"""
    memory_content = load_role_memory(role_name)
    personality = get_role_personality(role_name)
    role_prompt_parts = []
    
    if memory_content:
        role_prompt_parts.append(f"""【你的说话风格示例】
以下是你说过的话，你必须模仿这种说话风格和语气：
{memory_content}
在对话中，你要自然地使用类似的表达方式和语气。""")
    
    role_prompt_parts.append(f"【角色设定】\n{personality}")
    return "\n\n".join(role_prompt_parts)