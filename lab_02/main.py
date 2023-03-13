from controll.controllView import *

from view.CanvasField import *
from view.keyInput import *
from tkinter import messagebox
from tkinter import Tk


def main():
    root = Tk()
    root.geometry('1440x1080')

    root.title('Лабораторная номер 2')

    c = WrapCanva(root, Canva=PolygonField, highlightthickness=0, background='white')
    menu = Menu(root)
    root.config(menu=menu)
    inputPointsFromFile(c, 'data/loc.txt')

    menu.add_command(label="Автор", command=lambda: messagebox.showinfo(
        "Информация об авторе",
        "Программа сделана Булгаковым Иваном ИУ7-44Б",
    ))
    menu.add_command(label="О программе", command=lambda: messagebox.showinfo(
        "Информация о программе",
        "Нарисовать исходный рисунок, затем его переместить, промасштабировать, повернуть"
    ))
    menu.add_command(label="Отменить", command=lambda: c.canva.undo())
    menu.add_command(label="Повернуть", command=lambda: c.action(RotateFrame))
    menu.add_command(label="Сдвинуть", command=lambda: c.action(ShiftFrame))
    menu.add_command(label="Масштабировать", command=lambda: c.action(ScaleFrameSecondVersion))

    c.show(Settings.X_CANVA, Settings.Y_CANVA, Settings.REL_X_CANVA, Settings.REL_Y_CANVA)

    root.mainloop()


if __name__ == "__main__":
    main()


# from tkinter import *
# from PIL import ImageTk
# from view.CanvasField import *
#
# root = Tk()
# root.geometry('850x650')
# root['bg'] = 'yellow'
# f = WrapCanva(root, width=200, height=200, highlightthickness=0)
# f.show(Settings.X_CANVA, Settings.Y_CANVA, Settings.REL_X_CANVA, Settings.REL_Y_CANVA)
# image = ImageTk.PhotoImage(file = r"C:\projects\Сomputer graphics\lab_02\shared\rootIcon.png")
# f.canva.create_line(10, 10, 100, 100)
# f.canva.create_image(10, 10, image = image, anchor = NW)
# f = Frame(root, width=200, height=200)
# canvas = CartesianField(root, f, width=200, height=200, bg='blue')
# canvas.place(x=0, y=0, relwidth=1)
#
# image = ImageTk.PhotoImage(file = r"C:\projects\Сomputer graphics\lab_02\shared\rootIcon.png")
# canvas.create_image(10, 10, image = image, anchor = NW)
# canvas.create_line(10, 10, 100, 100)
# f.place(x=0, y=0, relwidth=0.7)

# mainloop()