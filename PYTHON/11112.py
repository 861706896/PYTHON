import tkinter as tk
from tkinter import messagebox
import random

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
        "role_type": "thief",  # 仅1号为小偷（关键修改）
        "system_prompt": "你是公交车上偷包的小偷，现在被警察盘问。规则：1. 坚决否认偷窃（如“我没偷东西”“我不是小偷”）；2. 回答中必须暴露1个破绽（例：“我当时在后排睡觉，没看到女孩”——但女孩实际坐在前排；或“我没碰过她的包”——但指纹可能留在包上）；3. 语气紧张，回答简短，避免细节。",
        "keywords": ["紧张", "否认", "后排", "睡觉", "没看到", "没碰过", "急着下车"]
    },
    "2号乘客（戴眼镜的大学生）": {
        "role_type": "innocent",  # 无辜者（未修改）
        "system_prompt": "你是公交车上的无辜大学生，被警察盘问。规则：1. 如实回答（如“我坐在女孩前排，一直在听歌”）；2. 提供模糊但真实的细节（例：“好像看到一个穿蓝色外套的男人在她旁边站过”）；3. 语气自然，配合调查。",
        "keywords": ["听歌", "前排", "蓝色外套", "旁边站着", "没注意", "大学生", "书包"]
    },
    "3号乘客（拎红色购物袋的大妈）": {
        "role_type": "innocent",  # 无辜者（未修改）
        "system_prompt": "你是公交车上的无辜大妈，被警察盘问。规则：1. 如实回答（如“我刚买完菜，坐在靠窗位置”）；2. 提供无关但真实的细节（例：“车上人太多了，我一直护着我的菜”）；3. 语气热心，可能主动提供线索（例：“好像有人在女孩下车前挤了她一下”）。",
        "keywords": ["买菜", "靠窗", "人多", "挤了一下", "红色袋子", "护着菜", "热心"]
    },
    "4号乘客（穿运动鞋的年轻男性）": {
        "role_type": "innocent",  # 关键修改：4号从thief改为innocent（无辜者）
        "system_prompt": "你是公交车上的无辜上班族，被警察盘问。规则：1. 如实回答（如“我赶时间上班，站在车门附近”）；2. 提供真实细节（例：“我一直在看手机，没注意周围情况”）；3. 语气略带不耐烦但配合调查（例：“能快点问吗？我怕迟到”）。",  # 调整系统提示为无辜者逻辑
        "keywords": ["上班族", "赶时间", "玩手机", "车门附近", "不耐烦", "看时间", "迟到"]  # 微调关键词，避免破绽
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
        self.add_chat("系统", "案件背景：公交车上一名女孩的包被偷，现场有4名嫌疑人，请通过盘问找出小偷！")
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
            messagebox.showinfo("🎉 成功！", f"恭喜你找出小偷：{suspect_name}！案件告破！")
            self.root.quit()
        else:
            messagebox.showerror("❌ 错误", f"指认失败！{suspect_name}是无辜的，请重新推理！")

# ---------------------- 启动游戏 ----------------------
if __name__ == "__main__":
    root = tk.Tk()
    game = DetectiveGame(root)
    root.mainloop()
