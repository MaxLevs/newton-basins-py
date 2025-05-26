import multiprocessing
import tkinter as tk

from PIL import ImageTk

from application.basins_drawer_service import BasinsDrawerService


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent
        tk.Button(self, text='Calculate', command=self.draw).pack(side="top")
        self.canvas = tk.Canvas(self, width=parent.winfo_width(), height=parent.winfo_width())
        self.canvas.pack(side="top", fill="both", expand=True)

        self.roots = [complex(1.2, -4), complex(3, 2.4), complex(-1.2, - 1.4),]
        self.tk_images = []
        self.drawer = BasinsDrawerService(self.roots)


    def draw(self):
        points = ((x, y) for x in range(12) for y in range(10))
        for point in points:
            self.draw_single(point)

    def draw_single(self, point):
        x, y = point
        image = self.drawer.draw(0, 0, 1)
        tk_image = ImageTk.PhotoImage(image, master=self)
        self.canvas.create_image(image.size[0] * x, image.size[1] * y, image=tk_image)
        self.tk_images.append(tk_image)
        print(x, y, tk_image)
        return 1


if __name__ == "__main__":
    tk_root = tk.Tk()
    tk_root.geometry(f'512x512')
    app = MainApplication(tk_root)
    app.pack(side="top", fill="both", expand=True)

    tk_root.mainloop()
