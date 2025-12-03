from roles import build_role_system
from logic import build_system_message
from chat import start_chat

def main():
    """主函数：整合所有模块并启动对话"""
    try:
        # 1. 选择角色并构建角色设定
        role_name = "何昭仪"  # 可修改角色名切换不同角色
        role_system = build_role_system(role_name)
        
        # 2. 构建完整系统消息（角色设定+规则）
        system_message = build_system_message(role_system)
        
        # 3. 启动对话循环
        start_chat(system_message)
    
    except KeyboardInterrupt:
        print("\n\n程序被用户中断")
    except Exception as e:
        print(f"\n\n发生错误: {e}")

if __name__ == "__main__":
    main()