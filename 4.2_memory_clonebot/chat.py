from api import call_zhipu_api
from logic import make_it_hezhaoyi, check_end_conversation

def start_chat(system_message: str):
    """启动对话循环"""
    # 初始化内存对话历史
    conversation_history = [{"role": "system", "content": system_message}]
    print("✓ 已加载初始记忆，开始对话（对话记录不会保存）")
    
    # ASCII头像
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
    
    while True:
        # 获取用户输入
        user_input = input("\n请输入你要说的话（输入\"再见\"退出）：")
        
        # 检查结束对话
        if check_end_conversation(user_input):
            print("对话结束")
            print(portrait + "\n再见")
            break
        
        # 更新对话历史
        conversation_history.append({"role": "user", "content": user_input})
        
        # 调用API获取回复
        result = call_zhipu_api(conversation_history)
        assistant_reply = result['choices'][0]['message']['content']
        assistant_reply = make_it_hezhaoyi(assistant_reply, user_input)
        
        # 保存AI回复到对话历史
        conversation_history.append({"role": "assistant", "content": assistant_reply})
        
        # 显示回复
        print(portrait + "\n" + assistant_reply)