from tkinter import *
from ui_helper import VerticalScrolledFrame, ResizingCanvas
from tkinter import messagebox
from tkinter import simpledialog
from collections import namedtuple

import geometry
from geometry import Point2D

WINDOW_SIZE = namedtuple('WidthHeight', ['width', 'height'])(width=1400, height=900)


class PointTableRow:
    def __init__(self, point_table: "PointTable", point_manager: "PointManger", point: Point2D):
        self.point = point
        self.x_var = StringVar()
        self.y_var = StringVar()

        self.point_manager = point_manager

        self.update(point.x, point.y)

        self.x_label = Label(point_table, textvariable=self.x_var, anchor="w")
        self.y_label = Label(point_table, textvariable=self.y_var, anchor="w")
        self.edit_button = Button(point_table, text="Edit", command=self.handle_edit)
        self.delete_button = Button(point_table, text="Delete", command=self.handle_delete)

        self.x_label.grid(row=point_table.rows_count(), column=0, sticky="ne")
        self.y_label.grid(row=point_table.rows_count(), column=1, sticky="ne")
        self.edit_button.grid(row=point_table.rows_count(), column=2, columnspan=2, sticky="ne")
        self.delete_button.grid(row=point_table.rows_count(), column=4, columnspan=2, sticky="ne")

    def handle_delete(self):
        self.point_manager.delete_point(self.point)

    def handle_edit(self):
        new_coords = simpledialog.askstring("Редактирование точки", "Введите координаты через пробел").split()
        try:
            x_val = float(new_coords[0])
            y_val = float(new_coords[1])
        except ValueError:
            messagebox.showerror("Ошибка!", "Координаты могут задаваться только вещественными числами")
            return
        except IndexError:
            messagebox.showerror("Ошибка!", "Необходимо задать x и y координаты")
            return
        self.point_manager.update_point(self.point, x_val, y_val)

    def destroy(self):
        self.x_label.destroy()
        self.y_label.destroy()
        self.edit_button.destroy()
        self.delete_button.destroy()

    def update(self, x, y):
        self.point.x = x
        self.point.y = y
        self.x_var.set("{:.2f}".format(x))
        self.y_var.set("{:.2f}".format(y))

    def get_point(self) -> Point2D:
        return self.point

    def color(self, color):
        if color == 'black':
            color = '#d9d9d9'
        self.x_label.configure(bg=color)
        self.y_label.configure(bg=color)


class PointTable(Frame):
    def __init__(self, point_manager: "PointManager", *args, **kwargs):
        Frame.__init__(self, *args, **kwargs)
        self.rows: list[PointTableRow] = []

        self.point_manager = point_manager

        self.grid_columnconfigure(1, weight=1)
        Label(self, text="X", anchor="w").grid(row=0, column=0, sticky="ne")
        Label(self, text="Y", anchor="w").grid(row=0, column=1, sticky="ne")

        self.entry_x = Entry(self, width=10)
        self.entry_y = Entry(self, width=10)
        self.add_button = Button(self, text="Add",
                                 command=self.__add_button_handler)

        self.__grid_add_new_dots()

    def add(self, point: Point2D):
        self.__grid_add_new_dots(self.rows_count() + 1)
        self.rows.append(PointTableRow(self, self.point_manager, point))

    def rows_count(self) -> int:
        return len(self.rows) + 1

    def __grid_add_new_dots(self, row=None):
        if row is None:
            row = self.rows_count() + 1
        self.entry_x.grid(row=row, column=0, sticky="ne")
        self.entry_y.grid(row=row, column=1, sticky="ne")
        self.add_button.grid(row=row, column=2, columnspan=4, sticky="we")

    def __add_button_handler(self):
        try:
            x_val = float(self.entry_x.get())
            y_val = float(self.entry_y.get())
        except ValueError:
            messagebox.showerror("Ошибка!", "Координаты могут задаваться только вещественными числами")
            return
        self.point_manager.add_point(Point2D(x=x_val, y=y_val))

    def delete(self, point: Point2D):
        for rows in self.rows:
            if rows.get_point() is point:
                rows.destroy()
                # return хз почему два объекта

    def update(self, point: Point2D, x, y):
        for rows in self.rows:
            if rows.get_point() is point:
                rows.update(x, y)
                # return хз почему два объекта(больше делете)

    def color(self, point: Point2D, color):
        for row in self.rows:
            if row.get_point() is point:
                try:
                    row.color(color)
                except Exception as e:
                    print('129', e)


class PointManager:
    def __init__(self):
        self.circle_upper_id = None
        self.circle_lower_id = None
        self.canvas = None
        self.point_table = None
        self.points = []
        self.actions = []
        self.line_id = None

    def set_canvas(self, canvas: Canvas):
        self.canvas = canvas

    def set_point_table(self, point_table: PointTable):
        self.point_table = point_table

    def find_point_id(self, point: Point2D):
        for p_id, _point in self.points:
            if _point is point:
                return p_id
        return None

    def get_idx_of_point(self, point: Point2D):
        for idx, (_, _point) in enumerate(self.points):
            if _point is point:
                return idx

    def delete_point_from_storage(self, point: Point2D):
        for idx, (_, _point) in enumerate(self.points):
            if _point is point:
                self.points.pop(idx)
                return

    def delete_point(self, point: Point2D, track=True):
        if track:
            self.actions.append(("delete", point))

        point_id = self.find_point_id(point)
        self.canvas.delete(point_id)
        self.point_table.delete(point)
        self.canvas.configure(scrollregion=self.canvas.bbox("scroll"))
        self.delete_point_from_storage(point)

    def add_point(self, point: Point2D, track=True):
        if track:
            self.actions.append(("add", point))

        point_id = self.canvas.draw_point(point)
        self.canvas.configure(scrollregion=self.canvas.bbox("scroll"))
        self.point_table.add(point)
        self.points.append([point_id, point])

    def update_point(self, point: Point2D, new_x, new_y, track=True):
        if track:
            self.actions.append(("update", point, point.x, point.y))

        point_idx = self.get_idx_of_point(point)
        self.canvas.delete(self.points[point_idx][0])
        self.points[point_idx][0] = self.canvas.draw_point(Point2D(x=new_x, y=new_y))
        self.canvas.configure(scrollregion=self.canvas.bbox("scroll"))
        self.point_table.update(point, new_x, new_y)

    def clear(self, track=True):
        if track:
            self.actions.append(("clear", [point[1] for point in self.points]))

        while len(self.points) > 0:
            self.delete_point(self.points[0][1], track=False)

        self.canvas.itemconfig(self.line_id, state='hidden')
        self.canvas.itemconfig(self.circle_lower_id, state='hidden')
        self.canvas.itemconfig(self.circle_upper_id, state='hidden')

    def undo(self):
        print(self.actions)
        if not self.actions:
            return

        last_action = self.actions.pop()
        if last_action[0] == "clear":
            for point in last_action[1]:
                self.add_point(point, track=False)
            self.canvas.itemconfig(self.line_id, state='normal')
            self.canvas.itemconfig(self.circle_lower_id, state='normal')
            self.canvas.itemconfig(self.circle_upper_id, state='normal')
        elif last_action[0] == "update":
            self.update_point(last_action[1], last_action[2], last_action[3], track=False)
        elif last_action[0] == "add":
            self.delete_point(last_action[1], track=False)
        elif last_action[0] == "delete":
            self.add_point(last_action[1], track=False)
        elif last_action[0] == "task":
            self.color_default()
            self.clear_task()

    def clear_task(self):
        self.canvas.delete(self.line_id)
        self.canvas.delete(self.circle_lower_id)
        self.canvas.delete(self.circle_upper_id)
        self.color_default()
        self.line_id = None
        self.circle_lower_id = None


    def color_default(self):
        for p in self.points:
            self.color_point(p[1], 'black')

    def color_point(self, point: Point2D, color):
        self.point_table.color(point, color)
        idx = self.get_idx_of_point(point)
        point_id = self.points[idx][0]
        self.canvas.delete(point_id)
        self.points[idx][0] = self.canvas.draw_point(point, color)

    def divide_into_sets(self, divide_vec: geometry.Vector):
        copy_points = []
        for p in self.points:
            if p[1] is not divide_vec.start and p[1] is not divide_vec.end:
                copy_points.append(p[1])
        less, on, upper = geometry.divide_points_by_vec(copy_points, divide_vec)
        return less, on, upper

    def clear_line(self):
        self.canvas.delete(self.line_id)

    def task(self):
        try:
            self.clear_task()
        except Exception as e:
            print(e, 'clear task')
        if len(self.points) < 2:
            messagebox.showerror("Ошибка!", "Для выполнения задания необходимо как минимум 2 точки!")
            return
        points = [p[1] for p in self.points]
        idx_a, idx_b = geometry.select_line_from_points(points)
        divide_vec = geometry.Vector(self.points[idx_a][1], self.points[idx_b][1])
        lower, on, upper = self.divide_into_sets(divide_vec)
        for l in lower:
            color = 'green'
            self.color_point(l, color)
        for u in upper:
            color = 'red'
            self.color_point(u, color)
        for o in on:
            color = 'blue'
            self.color_point(o, color)
        self.line_id = self.canvas.draw_line(self.points[idx_a][0], self.points[idx_b][0])

        message = ""
        circle_lower = None
        circle_upper = None
        try:
            circle_lower = geometry.Circle.min_circle(lower)
            self.circle_lower_id = self.canvas.draw_circle(circle_lower, 'green')
            message += f"Зеленая окружность:\nРадиус:{int(circle_lower.radius)}\n" + \
                       f"Центр: x={int(circle_lower.center.x)}, y={int(circle_lower.center.y)}\n" + \
                       f"Площадь: {int(circle_lower.square())}\n\n\n"
        except Exception as e:
            print(e, 'circle_lower')
        try:
            circle_upper = geometry.Circle.min_circle(upper)
            self.circle_upper_id = self.canvas.draw_circle(circle_upper, 'red')
            message += f"Красная окружность:\nРадиус:{int(circle_upper.radius)}\n" + \
                       f"Центр: x={int(circle_upper.center.x)}, y={int(circle_upper.center.y)}\n" + \
                       f"Площадь: {int(circle_upper.square())}\n\n\n"
        except Exception as e:
            print(e, 'circle_upper')

        if circle_lower is None:
            circle_lower = geometry.Circle(Point2D(0, 0), 0)
        if circle_upper is None:
            circle_upper = geometry.Circle(Point2D(0, 0), 0)

        message += f"Суммарная площадь: {int(geometry.Circle.total_area(circle_lower, circle_upper))}"

        messagebox.showinfo("", message)
        self.actions.append(("task", 0))


class App:
    def __init__(self):
        self.root = Tk()
        self.frame = Frame(self.root)
        self.frame.pack(fill=BOTH, expand=YES)

        self.point_manager = PointManager()

        self.point_table_frame = Frame(self.frame)
        self.point_table_frame.pack(side=RIGHT, fill=BOTH)
        self.point_table_frame_scroll = VerticalScrolledFrame(self.point_table_frame)
        self.point_table_frame_scroll.pack(side=RIGHT, fill=BOTH)

        self.point_table = PointTable(self.point_manager, self.point_table_frame_scroll.interior)
        self.point_table.pack(side=RIGHT, fill=BOTH, expand=True, padx=10, pady=10)

        self.canvas = ResizingCanvas(self.frame, width=WINDOW_SIZE.width, height=WINDOW_SIZE.height,
                                     bg="white", highlightthickness=0)
        self.canvas.pack(fill=BOTH, expand=YES)
        self.canvas.addtag_all("all")
        self.canvas.bind("<Button-1>", self.handle_left_click)

        self.point_manager.set_point_table(self.point_table)
        self.point_manager.set_canvas(self.canvas)

        menu = Menu(self.root)
        self.root.config(menu=menu)
        menu.add_command(label="Об авторе", command=lambda: messagebox.showinfo(
            "Информация об авторе",
            "Программа сделана Булгаковым Иваном ИУ7-44Б",
        ))
        menu.add_command(label="О программе", command=lambda: messagebox.showinfo(
            "Информация о программе",
            "Заданное множество точек на плоскости разбить на два подмножества прямой,"
            " проходящей через две различные точки так, чтобы количества точек, лежащих"
            " по разные стороны прямой, проходящей через эти две точки, различались"
            " наименьшим образом. Каждое из полученных множеств поместить внутрь"
            " окружности минимального радиуса. Найти суммарную площадь, покрытую данными окружностями.",
        ))
        menu.add_command(label="Очистить", command=self.point_manager.clear)
        menu.add_command(label="Отменить", command=self.point_manager.undo)
        menu.add_command(label="Выполнить", command=self.point_manager.task)

        self.root.mainloop()

    def handle_left_click(self, event: Event):
        point = Point2D(x=self.canvas.canvasx(event.x), y=self.canvas.canvasy(event.y))
        self.point_manager.add_point(point)


if __name__ == "__main__":
    app = App()
