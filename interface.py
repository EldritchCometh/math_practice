import tkinter as tk


class FlashCardsWindow(tk.Tk):

    def __init__(self, window_width, window_height):
        super().__init__()
        self.window(window_width, window_height)
        self.current_frame = FrameOne(self)
        self.current_frame.pack(fill="both", expand=True)

    def window(self, window_width, window_height):
        self.title("Arithmetic Flashcards")
        x = (self.winfo_screenwidth() - window_width) // 2
        y = (self.winfo_screenheight() - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def clicked(self, flag):
        self.current_frame.destroy()
        if flag == 'frame_1':
            self.current_frame = FrameTwo(self)
        if flag == 'frame_2':
            self.current_frame = FrameOne(self)
        self.current_frame.pack(fill="both", expand=True)


class FrameOne(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.build_layout()

    def build_layout(self):
        tk.Button(self, text="Foo", command=self.clicked).pack()

    def clicked(self):
        self.parent.clicked("frame_1")


class FrameTwo(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.build_layout()

    def build_layout(self):
        tk.Button(self, text="Bar", command=self.clicked).pack()

    def clicked(self):
        self.parent.clicked("frame_2")


if __name__ == "__main__":
    window = FlashCardsWindow(500, 300)
    window.mainloop()
