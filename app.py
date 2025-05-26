from application.basins_drawer_service import BasinsDrawerService
from PIL import ImageTk
import tkinter as tk

class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry('256x256')
    MainApplication(root).pack(side="top", fill="both", expand=True)
    canvas = tk.Canvas(root, width=256, height=256)
    drawer = BasinsDrawerService()
    image = drawer.draw(0, 0, 1)
    tk_image = ImageTk.PhotoImage(image, master=root)
    kk = canvas.create_image(128, 128, image=tk_image)
    canvas.pack(side="top", fill="both", expand=True)
    root.mainloop()
