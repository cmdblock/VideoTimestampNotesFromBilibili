import left_frame
import right_frame


class MainWindow:
    def __init__(
        self, root, title="生成视频时间戳", locationAndsize="800x600+500+100",
    ) -> None:
        self.root = root
        self.root.geometry(locationAndsize)  # 设置窗口大小和位置
        self.root.title(title)  # 设置窗口标题
        self.root.bind("<Control-w>", func=self.close_window)  # 绑定窗口关闭快捷键

        self.right_frame = right_frame.RightFrame(self.root)
        self.left_frame = left_frame.LeftFrame(self.root, self.right_frame)

        # weight = 0 表示组件固定，当窗口发生变化的时候不会随着窗口而移动
        # weight = 1 便是组件大小会随着窗口大小改变而改变自身的大小
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)

        self.root.columnconfigure(
            (0, 1), uniform="a"
        )  # uniform 表示 gird 中 每行一样宽

    # 关闭窗口
    def close_window(self, event=None):
        self.root.destroy()

