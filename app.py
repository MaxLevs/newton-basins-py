import multiprocessing
import tkinter as tk

from PIL import ImageTk

from application.basins_drawer_service import BasinsDrawerService


class ControlUnit(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent


    # noinspection PyUnresolvedReferences
    def place(self, func):
        func(self)
        return self

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        cu = ControlUnit(self, *args, **kwargs)
        cu.place(lambda itself: tk.Button(itself, text='Move Left', command=self.move_left).pack(side="left"))
        cu.place(lambda itself: tk.Button(itself, text='Calculate', command=self.draw).pack(side="left"))
        cu.place(lambda itself: tk.Button(itself, text='Move Right', command=self.move_right).pack(side="left"))
        cu.place(lambda itself: tk.Button(itself, text='Clear All', command=self.clear_elements).pack(side="left"))
        cu.pack(side="top")

        self.canvas = tk.Canvas(self, width=parent.winfo_width(), height=parent.winfo_width())
        self.canvas.pack(side="top", fill="both", expand=True)

        self.roots = [complex(1.2, -4), complex(3, 2.4), complex(-1.2, - 1.4),]
        self.tk_images = []
        self.drawer = BasinsDrawerService(self.roots)


    def draw(self):
        image = self.drawer.draw(0, 0, 1)
        tk_image = ImageTk.PhotoImage(image, master=self)
        self.canvas.create_image(image.size[0], image.size[1], image=tk_image, tag="basins_tiles")
        self.tk_images.append(tk_image)

    def move_left(self):
        # self.canvas.itemconfig(img, state="hidden")
        self.canvas.move("basins_tiles", -10, 0)

    def move_right(self):
        self.canvas.move("basins_tiles", 10, 0)

    def clear_elements(self):
        self.tk_images = []


if __name__ == "__main__":
    tk_root = tk.Tk()
    tk_root.title("Newton's basins")
    tk_root.geometry(f'512x512')
    app = MainApplication(tk_root)
    app.pack(side="top", fill="both", expand=True)

    tk_root.mainloop()
