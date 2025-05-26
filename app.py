import tkinter as tk

from PIL import ImageTk

from application.basins_drawer_service import BasinsDrawerService


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

        self.roots = [complex(1.2, -4), complex(3, 2.4), complex(-1.2, - 1.4),]
        self.drawer = BasinsDrawerService(self.roots)

        self.canvas = tk.Canvas(app, width=app.winfo_width(), height=app.winfo_height())
        self.canvas.pack(side="top", fill="both", expand=True)

        tk.Button(self, text='Calculate', command=self.draw).pack(side="right")

    def draw(self):
        image = self.drawer.draw(0, 0, 1)
        tk_image = ImageTk.PhotoImage(image, master=self)
        kk = self.canvas.create_image(image.size[0] / 2, image.size[1] / 2, image=tk_image)


if __name__ == "__main__":
    app = tk.Tk()
    app.geometry(f'512x512')
    MainApplication(app).pack(side="top", fill="both", expand=True)
    app.mainloop()
