import re
import tkinter as tk
from tkinter import ttk


class LeftFrame:
    def __init__(self, root, right_frame) -> None:
        self.root = tk.Frame(root)
        self.root.grid(row=0, column=0, sticky="nsew")

        self.frame_web = tk.Frame(self.root)
        self.frame_web.pack(pady=10, padx=10)

        self.label_web = tk.Label(
            self.frame_web, font=("微软雅黑", 20, "bold"), text="网址: "
        )
        self.label_web.grid(row=0, column=0, padx=10, pady=10, sticky="e")

        # 网址
        self.entry = tk.Entry(self.frame_web, font=("微软雅黑", 20, "bold"))
        self.entry.grid(row=0, column=1, padx=10, pady=10, sticky="w")

        # 说明文字 + 选择框
        self.frame_label_select = tk.Frame(self.root)
        self.frame_label_select.pack(pady=10, padx=10)

        self.label_ai = tk.Label(
            self.frame_label_select, font=("微软雅黑", 20, "bold"), text="AI 时间戳"
        )
        self.label_ai.grid(row=0, column=0, padx=0, pady=10, sticky="e")

        self.combobox = ttk.Combobox(self.frame_label_select)
        self.combobox.configure(
            font=("微软雅黑", 16, "normal"),
            values=["豆包AI", "哔哩哔哩字幕列表"],
            state="READONLY",  # 只可选择
            width=15,  # 需要设置 width 来保证有下拉箭头
        )
        self.combobox.current(1)
        self.combobox.grid(row=0, column=1, padx=10, pady=10, sticky="e")

        # 原始时间戳文本
        self.text = tk.Text(self.root, height=5, font=("微软雅黑", 16, "bold"))
        self.text.pack(pady=10, padx=10, fill="both", expand=True)

        # 转换按钮
        self.button = tk.Button(
            self.root, font=("微软雅黑", 20, "bold"), text="生成时间戳"
        )
        self.button.configure(bg="lightblue", relief="raised", command=self.convert)
        self.button.pack()

        # 右边的frame
        self.right_frame = right_frame

    def output(self, timestamp_text):
        self.right_frame.text.delete("1.0", tk.END)
        self.right_frame.text.insert("1.0", timestamp_text)

    def convert(self):
        # 获取网址
        URL = self.entry.get()
        url = None
        if URL.startswith(r"https://www.bilibili.com"):
            url = self.extract_url_from_B(URL)
            if url:
                result = self.generate_video_time_of_B(url)
                result = "\n".join(result)
                self.output(timestamp_text=result)

        if URL.startswith(r"https://www.youtube.com"):
            url = self.extract_url_from_Y(URL)
            if url:
                result = self.generate_video_time_of_Y(url)
                result = "\n".join(result)
                self.output(timestamp_text=result)

    def extract_url_from_B(self, URL):
        pattern = r"(https://www\.bilibili\.com/video/[a-zA-Z0-9]+/)"
        match = re.search(pattern, URL)
        if match:
            return match.group(1)
        else:
            return None

    def extract_url_from_Y(self, URL):
        pattern = r"(https://www\.youtube\.com/watch\?v=[^&]+)"
        match = re.search(pattern, URL)
        if match:
            return match.group(1)
        else:
            return None

    def calc_time(self, timestamp) -> str:
        time = timestamp.split(":")
        # print(timestamp)
        seconds = 0
        if len(time) == 3:
            seconds += int(time[2]) + int(time[1]) * 60 + int(time[0]) * 3600
        else:
            seconds += int(time[1]) + int(time[0]) * 60

        return str(seconds)

    def extract_time_of_B(self, text, url, haveTab: bool) -> None | str:
        # 提取时间和文字
        pattern = r"\[([0-9:]+)\](.*)"
        match = re.search(pattern, text)
        if match:
            timestamp = match.group(1)
            description = match.group(2)
            # 计算时间
            time = self.calc_time(timestamp)
            # 拼接时间和文字
            time = "?" + "t=" + time + "#t=" + time + ".00"
            result = "- " + "[" + timestamp + "]" + "(" + url + time + ")" + description
            if haveTab:
                result += "\t"

            return result
        return None

    def generate_video_time_of_B(self, url):
        timestamps = []
        text = self.text.get("1.0", tk.END)
        lines = text.splitlines()

        # 如果字幕是哔哩哔哩字幕列表生成的，先转换成 豆包AI样式的字幕列表
        if self.combobox.get() == "哔哩哔哩字幕列表":
            # 通过哔哩哔哩字幕列表插件获得的时间戳
            # 提取时间和内容合并成一行
            lines = self.merge_time_text_of_BPlugin(lines)
            print(lines)

        # 抽取时间和内容
        for line in lines:
            if line.startswith("["):
                timestamps.append(self.extract_time_of_B(line, url, False))

            if line.startswith("\t"):
                timestamps.append(self.extract_time_of_B(line, url, True))

        # 返回结果
        return timestamps

    def merge_time_text_of_BPlugin(self, lines):
        new_lines = []
        length = len(lines)
        for i in range(0, length, 3):
            time = "[" + lines[i + 1] + "]"
            text = lines[i + 2]
            new_lines.append(time + " " + text)

        return new_lines

    def extract_time_of_Y(self, text, url, haveTab: bool) -> None | str:
        # 提取时间和文字
        pattern = r"\[([0-9:]+)\](.*)"
        match = re.search(pattern, text)
        if match:
            timestamp = match.group(1)
            print(timestamp)
            description = match.group(2)
            # 计算时间
            time = self.calc_time(timestamp)
            # 拼接网址和时间
            time = "&t=" + time + "#t=" + timestamp + ".00"
            result = "- " + "[" + timestamp + "]" + "(" + url + time + ")" + description
            if haveTab:
                result += "\t"
            return result

    def generate_video_time_of_Y(self, url):
        text = self.text.get("1.0", tk.END)
        lines = text.splitlines()
        timestamps = []
        for line in lines:
            if line.startswith("["):
                timestamps.append(self.extract_time_of_Y(line, url, False))

            if line.startswith("\t"):
                timestamps.append(self.extract_time_of_Y(line, url, True))
        return timestamps


