import tkinter as tk


class FlashCardsWindow(tk.Tk):

    def __init__(self, window_width, window_height):
        super().__init__()
        self.window(window_width, window_height)
        self.current_frame = tk.Frame(self)
        self.new_frame = FrameOne(self)
        self.switch_frame()

    def window(self, window_width, window_height):
        self.title("Arithmetic Flashcards")
        x = (self.winfo_screenwidth() - window_width) // 2
        y = (self.winfo_screenheight() - window_height) // 2
        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def switch_frame(self):
        if self.new_frame:
            self.current_frame.destroy()
            self.current_frame = self.new_frame
            self.current_frame.pack(fill="both", expand=True)
            self.new_frame = None

        self.after(1, self.switch_frame)


class FrameOne(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.button = tk.Button(self, text="Foo", command=self.switch)
        self.button.pack()
        self.parent = parent

    def switch(self):
        self.parent.new_frame = FrameTwo(self.parent)


class FrameTwo(tk.Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.button = tk.Button(self, text="Bar", command=self.switch)
        self.button.pack()
        self.parent = parent

    def switch(self):
        self.parent.new_frame = FrameOne(self.parent)


if __name__ == "__main__":
    window = FlashCardsWindow(500, 300)
    window.mainloop()
