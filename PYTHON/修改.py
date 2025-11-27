import tkinter as tk
from tkinter import messagebox
import random
import textwrap
import threading

try:
    from xunfei_tts import text_to_speech
    TTS_AVAILABLE = True
except ImportError as e:
    print(f"警告: 无法导入 xunfei_tts 模块: {e}")
    text_to_speech = None
    TTS_AVAILABLE = False 

try:
    import requests
except ImportError:
    requests = None

# ---------------------- 核心配置（修改嫌疑人角色） ----------------------
def call_ai_api(messages, is_thief=False):
    url = "https://open.bigmodel.cn/api/paas/v4/chat/completions"
    headers = {
        "Authorization": "999fb227c3f44308bf9096a42c18e339.YFxcpSNLfq1VQZqj",  # 替换为你的API密钥
        "Content-Type": "application/json"
    }
    temperature = 0.8 if is_thief else 0.5
    data = {"model": "glm-4-flash", "messages": messages, "temperature": temperature}
    if requests is None:
        return "【AI回答失败】当前环境未安装 requests 库，无法连接AI接口。"
    try:
        response = requests.post(url, headers=headers, json=data, timeout=15)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        return f"【AI回答失败】{str(e)}"

SUSPECTS = {
    "1号乘客（穿蓝色外套的中年男性）": {
        "role_type": "thief",  # 仅1号为小偷
        "system_prompt": "你是公交车上偷包的小偷，现在被警察盘问。规则：1. 坚决否认偷窃（如“我没偷东西”“我不是小偷”）；2. 回答中必须暴露1个破绽（例：“我当时在后排睡觉，没看到女孩”——但女孩实际坐在前排；或“我没碰过她的包”——但指纹可能留在包上）；3. 语气紧张，回答简短，避免细节。",
        "keywords": ["紧张", "否认", "后排", "睡觉", "没看到", "没碰过", "急着下车"],
        # 新增：1号（小偷）具体动线及作案过程
        "schedule": [
            "13:00 从汽车北站上车，计划前往西湖文化广场找朋友借钱",
            "13:15 坐在车厢后排右侧座位，一直观察周围乘客",
            "13:40 受害人（女大学生）在武林广场站上車，坐在前排中部靠窗位置",
            "13:45 趁车辆转弯、乘客晃动时，悄悄移动到受害人座位旁假装站立",
            "13:58 车辆快到西湖文化广场站，趁受害人低头看手机，用刀片划开其双肩包拉链，偷走笔记本电脑和钱包",
            "14:00 将赃物藏在外套内侧口袋，迅速返回后排座位，假装睡觉",
            "14:02 司机锁门，警察上车调查"
        "只用第一人称回答。"
        ]
    },
    "2号乘客（戴眼镜的大学生）": {
        "role_type": "innocent",
        "system_prompt": "你是公交车上的无辜大学生，被警察盘问。规则：1. 如实回答（如“我坐在女孩前排，一直在听歌”）；2. 提供模糊但真实的细节（例：“好像看到一个穿蓝色外套的男人在她旁边站过”）；3. 语气自然，配合调查。",
        "keywords": ["听歌", "前排", "蓝色外套", "旁边站着", "没注意", "大学生", "书包"],
        # 新增：2号（无辜者）具体动线
        "schedule": [
            "13:30 从下沙高教园区上车，前往市区书店买考研资料",
            "13:35 坐在受害人前排座位，全程戴耳机听网课",
            "13:45 感觉身后有人走动（后来知道是1号乘客），但没回头看",
            "13:55 隐约听到后排有拉链声，但以为是别人拿东西"
        "只用第一人称回答。"
        ]
    },
    "3号乘客（拎红色购物袋的大妈）": {
        "role_type": "innocent",
        "system_prompt": "你是公交车上的无辜大妈，被警察盘问。规则：1. 如实回答（如“我刚买完菜，坐在靠窗位置”）；2. 提供无关但真实的细节（例：“车上人太多了，我一直护着我的菜”）；3. 语气热心，可能主动提供线索（例：“好像有人在女孩下车前挤了她一下”）。",
        "keywords": ["买菜", "靠窗", "人多", "挤了一下", "红色袋子", "护着菜", "热心"],
        # 新增：3号（无辜者）具体动线
        "schedule": [
            "13:00 在古荡新村站上车，刚从菜市场买完菜（拎红色购物袋）",
            "13:05 坐在车厢左侧前排靠窗位置，全程在整理菜篮子",
            "13:40 看到受害人上车，背着双肩包坐在她斜后方",
            "13:50 注意到一个穿蓝色外套的中年男人在受害人旁边站了很久，还频频看手表",
            "13:58 车辆到站前，听到受害人小声惊呼“我的包怎么开了！”"
        "只用第一人称回答。"
        ]
    },
    "4号乘客（穿运动鞋的年轻男性）": {
         "role_type": "innocent",  # 关键修改：4号从thief改为innocent（无辜者）
        "system_prompt": "你是公交车上的无辜上班族，被警察盘问。规则：1. 如实回答（如“我赶时间上班，站在车门附近”）；2. 提供真实细节（例：“我一直在看手机，没注意周围情况”）；3. 语气略带不耐烦但配合调查（例：“能快点问吗？我怕迟到”）。",
        "keywords": ["上班族", "赶时间", "玩手机", "车门附近", "不耐烦", "看时间", "迟到"],
        # 新增：4号（无辜者）具体动线
        "schedule": [
            "13:20 从三墩站上车，赶去公司加班（下午4点打卡）",
            "13:25 因座位满员，一直站在车门附近刷手机工作群消息",
            "13:50 抬头看路线时，看到后排一个穿蓝色外套的男人神色紧张，手插在外套口袋里动来动去",
            "14:00 听到有人喊“抓小偷”，司机锁门后开始烦躁地看时间"
        "只用第一人称回答"
        ]
    }
}

ACTIONS = {
    "系统": ["系统灯光闪烁，发出提示音", "广播里传来系统声音"],
    "警察": ["警察翻看记录本", "警察皱着眉记录线索", "警察盯着嫌疑人眼睛"],
    "1号乘客（穿蓝色外套的中年男性）": [
        "他抓紧外套下摆，手心微微出汗",
        "他眼神游移，不敢直视警察",
        "他下意识地捏着车票，指尖发白"
    ],
    "2号乘客（戴眼镜的大学生）": [
        "他扶了扶眼镜，语气有些慌张",
        "他低头摆弄着耳机线",
        "他翻着书包寻找着什么"
    ],
    "3号乘客（拎红色购物袋的大妈）": [
        "她拍了拍怀里的菜篮子",
        "她伸手指向车厢另一头",
        "她热心地挪了挪位置"
    ],
    "4号乘客（穿运动鞋的年轻男性）": [
        "他看了看手表，显得有些着急",  # 调整4号动作，符合无辜者设定
        "他刷着手机，时不时抬头催促",
        "他整理了一下背包肩带"
    ]
}


# ---------------------- 游戏界面与逻辑（修改发送快捷键） ----------------------
class DetectiveGame:
    def __init__(self, root):
        self.root = root
        self.root.title("🚨 公交车失窃案：请帮小女孩找出小偷！ 🕵️")
        self.root.geometry("980x640")
        self.root.resizable(False, False)
        
        self.current_suspect = random.choice(list(SUSPECTS.keys()))
        self.messages = []
        self.suspect_buttons = {}
        self.loading_counter = 0
        self.create_ui()
    
    def create_ui(self):
        # 1. 顶部标题栏（未修改）
        tk.Label(
            self.root, 
            text="公交车失窃案：盘问嫌疑人找出小偷！", 
            font=("SimHei", 14, "bold"), 
            bg="#2980b9", 
            fg="white", 
            height=2
        ).pack(fill=tk.X)
        
        # 2. 左侧嫌疑人列表（未修改）
        left_frame = tk.Frame(self.root, width=240, bg="#f7f9fc", relief=tk.RIDGE, bd=2)
        left_frame.pack(side=tk.LEFT, fill=tk.Y)
        tk.Label(left_frame, text="👥 嫌疑人名单", font=("SimHei", 12, "bold"), bg="#f7f9fc").pack(pady=10)
        list_frame = tk.Frame(left_frame, bg="#f7f9fc")
        list_frame.pack(fill=tk.BOTH, expand=True)
        for suspect in SUSPECTS:
            btn = tk.Button(
                list_frame,
                text=suspect,
                font=("SimHei", 11),
                relief=tk.FLAT,
                anchor="w",
                padx=15,
                bg="#f7f9fc",
                fg="#2c3e50",
                command=lambda s=suspect: self.select_suspect(s)
            )
            btn.pack(fill=tk.X, pady=4, padx=8)
            self.suspect_buttons[suspect] = btn
        self.highlight_current_suspect()

        # 左侧指认按钮（未修改）
        tk.Button(
            left_frame,
            text="指认小偷",
            font=("SimHei", 11, "bold"),
            bg="#e74c3c",
            fg="white",
            width=12,
            command=self.accuse_thief
        ).pack(side=tk.BOTTOM, pady=15)
        
        # 3. 右侧对话区域（未修改）
        right_frame = tk.Frame(self.root, bg="#ecf0f1")
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)
        
        # 对话记录文本框（未修改）
        self.chat_log = tk.Text(
            right_frame,
            font=("SimHei", 12),
            wrap=tk.WORD,
            state=tk.DISABLED,
            bg="#ffffff",
            fg="#2c3e50",
            relief=tk.FLAT
        )
        self.chat_log.pack(fill=tk.BOTH, expand=True, padx=15, pady=(15, 5))
        self.add_chat(
         '系统',
         textwrap.dedent('''案件背景：
2025年11月19日下午3点15分，
302路公交车行驶至"西湖文化广场"站时，

一名女大学生报警称随身携带的双肩包被盗，
包内有笔记本电脑（贴有"中国美术学院"校徽贴纸）、学生证及现金500元。
司机立即锁闭车门，等待警察到场。

经初步调查，受害人坐在车厢中部靠窗位置，
于"武林广场"站上车，失窃发生在"西湖文化广场"站停车前2分钟。
当时车厢内乘客较多，受害人因低头看手机未察觉包被拉开。

警察到场后，根据受害人描述及监控初步锁定4名重点嫌疑人（均在受害人附近区域）。
请通过盘问嫌疑人，结合他们的言行破绽，找出真正的小偷！''')
        )
        self.add_chat("系统", f"当前盘问对象：{self.current_suspect}（点击左侧名字可切换）")

        # 4. 输入区域（修改发送快捷键为Enter）
        input_frame = tk.Frame(right_frame, bg="#ecf0f1", pady=6)
        input_frame.pack(fill=tk.X, padx=15, pady=(0, 12))
        input_frame.columnconfigure(0, weight=1)
        
        self.question_entry = tk.Text(
            input_frame,
            font=("SimHei", 12),
            height=1,  # 保持单行输入
            wrap=tk.WORD,
            relief=tk.GROOVE,
            bd=2
        )
        self.question_entry.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.question_entry.focus_set()
        # 关键修改：绑定Enter键发送（原需Ctrl+Enter）
        self.question_entry.bind("<Return>", self.handle_enter_key)  # 新增：Enter键触发
        
        send_btn = tk.Button(
            input_frame,
            text="发送",
            font=("SimHei", 11, "bold"),
            bg="#27ae60",
            fg="white",
            width=10,
            command=self.ask_question
        )
        send_btn.grid(row=0, column=1, sticky="ns")
    
    # ---------------------- 核心逻辑（新增Enter键处理函数） ----------------------
    def handle_enter_key(self, event):
        """处理Enter键：发送消息并阻止默认换行"""
        self.ask_question()
        return "break"  # 阻止文本框插入换行符
    
    def add_chat(self, sender, text):
        self.chat_log.config(state=tk.NORMAL)
        action = self.get_action(sender)
        extra = f"（{action}）" if action else ""
        self.chat_log.insert(tk.END, f"【{sender}】：{text}\n{extra}\n\n")
        self.chat_log.see(tk.END)
        self.chat_log.config(state=tk.DISABLED)
    
    def get_action(self, sender):
        actions = ACTIONS.get(sender)
        if actions:
            return random.choice(actions)
        return ""
    
    def ask_question(self):
        question = self.question_entry.get("1.0", tk.END).strip()
        if not question:
            messagebox.showwarning("提示", "请输入你的问题！")
            return
        self.add_chat("警察", question)
        suspect_name = self.current_suspect
        loading_tag = self.add_loading_message(suspect_name)
        self.question_entry.delete("1.0", tk.END)
        self.root.after(100, lambda: self.fetch_ai_reply(question, loading_tag, suspect_name))

    def fetch_ai_reply(self, question, loading_tag, suspect_name):
        suspect_info = SUSPECTS[suspect_name]
        messages = [{"role": "system", "content": suspect_info["system_prompt"]},{"role": "user", "content": question}]
        reply = call_ai_api(messages, is_thief=(suspect_info["role_type"] == "thief"))
        self.replace_loading_message(loading_tag, suspect_name, reply)

    def add_loading_message(self, sender):
        self.chat_log.config(state=tk.NORMAL)
        loading_text = f"【{sender}】：正在思考……"
        tag = f"loading_{self.loading_counter}"
        self.loading_counter += 1
        self.chat_log.insert(tk.END, loading_text + "\n\n", tag)
        self.chat_log.see(tk.END)
        self.chat_log.config(state=tk.DISABLED)
        return tag

    def replace_loading_message(self, tag, sender, text):
        self.chat_log.config(state=tk.NORMAL)
        ranges = self.chat_log.tag_ranges(tag)
        if ranges:
            start_index, end_index = ranges[0], ranges[1]
            self.chat_log.delete(start_index, end_index)
            action = self.get_action(sender)
            extra = f"（{action}）" if action else ""
            self.chat_log.insert(start_index, f"【{sender}】：{text}\n{extra}\n\n")
        self.chat_log.tag_delete(tag)
        self.chat_log.see(tk.END)
        self.chat_log.config(state=tk.DISABLED)
        
        # 语音朗读嫌疑人回复（在后台线程中运行，避免阻塞界面）
        def play_speech():
            if not TTS_AVAILABLE:
                print("[TTS] 警告: TTS模块未正确导入，跳过语音播放")
                return
                
            try:
                if not text or len(text.strip()) == 0:
                    print("[TTS] 警告: 文本为空，跳过TTS")
                    return
                
                print(f"[TTS] 开始朗读: {text[:50]}...")  # 调试信息
                
                # 检查 text_to_speech 是否可用
                if text_to_speech is None:
                    print("[TTS] 错误: text_to_speech 函数未正确导入")
                    return
                
                text_to_speech(text)
                print("[TTS] 朗读完成")
            except ImportError as e:
                print(f"[TTS] 导入错误: {e}")
                print("[TTS] 请确保已安装: pip install websocket-client pygame")
            except Exception as e:
                # 输出完整错误信息以便调试
                print(f"[TTS] 错误类型: {type(e).__name__}")
                print(f"[TTS] 错误信息: {e}")
                import traceback
                print("[TTS] 完整错误堆栈:")
                traceback.print_exc()
        
        # 在后台线程中执行TTS，避免阻塞UI
        threading.Thread(target=play_speech, daemon=True).start()
    
    def highlight_current_suspect(self):
        for name, btn in self.suspect_buttons.items():
            if name == self.current_suspect:
                btn.config(bg="#d6eaf8", fg="#1b4f72")
            else:
                btn.config(bg="#f7f9fc", fg="#2c3e50")
    
    def select_suspect(self, suspect):
        if suspect == self.current_suspect:
            return
        self.current_suspect = suspect
        self.highlight_current_suspect()
        self.add_chat("系统", f"已切换盘问对象：{self.current_suspect}")
    
    def accuse_thief(self):
        suspect_name = self.current_suspect
        if not suspect_name:
            messagebox.showwarning("提示", "请先选择一名嫌疑人！")
            return

        if SUSPECTS[suspect_name]["role_type"] == "thief":
            # 第一个弹窗：成功提示
            messagebox.showinfo("🎉 成功！", f"恭喜你找出小偷：{suspect_name}！案件告破！")

            # 第二个弹窗：详细证据（用换行符 \n 分隔多条证据）
            evidence = (
        "1. **监控证据**：车辆转弯时，该男子曾靠近受害人座位并做出可疑手部动作；\n"
        "2. **行为破绽**：声称“在后排睡觉”，但受害人实际坐在前排，且多名乘客证实其曾在受害人附近徘徊；\n"
        "3. **物证**：警方在其外套内侧口袋发现带有受害人指纹的笔记本电脑及现金；\n"
        "4. **时间线矛盾**：其声称“13:40在后排睡觉”，但监控显示13:45他正在前排移动。"
            )
            messagebox.showinfo("🔍 破案关键证据", evidence)  # title="破案关键证据", message=证据内容
            self.root.quit()  # 关闭程序（可选，根据需求保留）
        else:
            messagebox.showerror("❌ 错误", f"指认失败！{suspect_name}是无辜的，请重新推理！")

    # ---------------------- 启动游戏 ----------------------
if __name__ == "__main__":
    root = tk.Tk()
    game = DetectiveGame(root)
    root.mainloop()
