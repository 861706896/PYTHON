import random
import re

# 全局规则配置
FORCE_STYLE = """【强制语气规则 - 优先级高于角色设定】
1. 每句 4~12 字，总长≤30 字。
2. 其他行不出现emji,只有最后一行 1 个 emoji
3. 禁止书面连接词（“首先/然而/因为”）。
4. 用户说“再见”只回“再见”两字。
"""

BREAK_MESSAGE = """
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

NATURAL_STYLE = """
回复格式：
- 每句 4~10 字就换行，像手机打字。
- 别用【表情包】，用真实 emoji（😂🤣😳😆🫠🥱👀🙈 等）根据语境挑 1 个放句尾。
- 禁止书面连词，禁止长句。
- 口头禅只在合适场景出现（被吐槽时先“哈哈哈哈哈”自嘲），其他场景不加。
"""

def make_it_hezhaoyi(text: str, user: str) -> str:
    """后处理：转换为昭仪风格的回复"""
    # 按标点/空格断句，保留完整语义
    sents = re.split(r'[，。！？；\s]+', text.strip())
    sents = [s.strip() for s in sents if s.strip()]
    if not sents:
        return "哈哈哈哈 😂"
    
    # 插入语境口头禅
    if any(k in user for k in ("你话多", "你好烦", "怎么这么")):
        sents.insert(0, random.choice(["哈哈哈哈", "哎呀哎呀"]))
    elif any(k in user for k in ("在干嘛", "干嘛呢")):
        sents.insert(0, random.choice(["刚躺平", "摸鱼中", "刚醒"]))
    
    # 最后一句添加emoji
    emoji_pool = ["😂", "🤣", "😳", "😆", "🫠", "🥱", "👀"]
    sents[-1] += random.choice(emoji_pool)
    
    return "\n".join(sents)[:90]

def check_end_conversation(user_input: str) -> bool:
    """检查用户是否要结束对话"""
    end_keywords = ["再见", "结束", "不想继续", "停止对话", "退出"]
    return any(keyword in user_input for keyword in end_keywords)

def build_system_message(role_system: str) -> str:
    """构建完整的系统消息（角色设定+规则）"""
    return role_system + "\n\n" + NATURAL_STYLE + "\n\n" + BREAK_MESSAGE