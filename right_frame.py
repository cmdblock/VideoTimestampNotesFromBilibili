import tkinter as tk


class RightFrame:
    def __init__(self, root) -> None:
        self.root = tk.Frame(root)
        self.root.grid(row=0, column=1, sticky="nsew")

        self.label = tk.Label(
            self.root, font=("微软雅黑", 20, "bold"), text="在线视频时间戳"
        )
        self.label.pack(pady=10, padx=10)

        self.text = tk.Text(self.root, font=("微软雅黑", 16, "bold"))
        self.text.configure(height=15)
        self.text.pack(pady=10, padx=10, fill="both", expand=True)

        self.button = tk.Button(
            self.root,
            bg="lightblue",
            font=("微软雅黑", 20, "bold"),
            text="复制在线视频时间戳",
            command=self.copy_timestamp_to_clipboard,
        )
        self.button.pack()

    # text 收件中的内容拷贝到剪切板
    def copy_timestamp_to_clipboard(self):
        text = self.text.get("1.0", tk.END)
        self.root.clipboard_clear()
        self.root.clipboard_append(text)

