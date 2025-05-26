import tkinter as tk

from PIL import ImageTk

from application.basins_drawer_service import BasinsDrawerService
from domain.image_tile import ImageTile


class MainApplication(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
        tk.Frame.__init__(self, parent, *args, **kwargs)
        self.parent = parent

if __name__ == "__main__":
    root = tk.Tk()
    image_size = ImageTile.image_size
    root.geometry(f'{image_size[0]*2}x{image_size[1]*2}')
    MainApplication(root).pack(side="top", fill="both", expand=True)
    canvas = tk.Canvas(root, width=image_size[0]*2, height=image_size[1]*2)
    drawer = BasinsDrawerService([complex(1.2, -4), complex(3, 2.4), complex(-1.2, - 1.4),])
    image = drawer.draw(0, 0, 1).resize((image_size[0]*2, image_size[1]*2))
    tk_image = ImageTk.PhotoImage(image, master=root)
    kk = canvas.create_image(image_size[0] / 2, image_size[1] / 2, image=tk_image)
    canvas.pack(side="top", fill="both", expand=True)
    root.mainloop()
