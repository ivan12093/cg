from tkinter import *
import geometry
from geometry import Point2D


class VerticalScrolledFrame(Frame):
    """A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame.
    * Construct and pack/place/grid normally.
    * This frame only allows vertical scrolling.
    """

    def __init__(self, parent, *args, **kw):
        Frame.__init__(self, parent, *args, **kw)

        # Create a canvas object and a vertical scrollbar for scrolling it.
        vscrollbar = Scrollbar(self, orient=VERTICAL)
        vscrollbar.pack(fill=Y, side=RIGHT, expand=FALSE)
        canvas = Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        canvas.pack(side=LEFT, fill=BOTH, expand=TRUE)
        vscrollbar.config(command=canvas.yview)

        # Reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # Create a frame inside the canvas which will be scrolled with it.
        self.interior = interior = Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=NW)

        # Track changes to the canvas and frame width and sync them,
        # also updating the scrollbar.
        def _configure_interior(event):
            # Update the scrollbars to match the size of the inner frame.
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the canvas's width to fit the inner frame.
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # Update the inner frame's width to fill the canvas.
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())

        canvas.bind('<Configure>', _configure_canvas)


class XCanvas(Canvas):
    def __init__(self, rootwin, **opt):
        width = opt.get("width", 1000)
        height = opt.get("height", 600)
        bg = opt.get("bg", "white")
        scrollbars = opt.get("scrollbars", True)
        x_axis = opt.get("x_axis", 7)
        y_axis = opt.get("y_axis", 7)

        self.r = 1.0
        self.region = (-50, -50, width, height)
        self.rootwin = rootwin
        self.rootframe = Frame(rootwin, width=width, height=height, bg=bg)
        self.rootframe.pack(expand=YES, fill=BOTH)
        Canvas.__init__(self, self.rootframe, width=width, height=height, bg=bg)
        self.config(highlightthickness=0)

        if scrollbars:
            self.scrollbars()

        self.pack(side=LEFT, expand=True, fill=BOTH)

        self.xview_moveto(0)
        self.yview_moveto(0)
        if x_axis or y_axis:
            self.draw_axis(x_axis, y_axis)
        self.configure(scrollregion=self.bbox("all"))
        self.bindings()

    def scrollbars(self):
        self.sbarV = Scrollbar(self.rootframe, orient=VERTICAL)
        self.sbarH = Scrollbar(self.rootframe, orient=HORIZONTAL)
        self.sbarV.config(command=self.yview)
        self.sbarH.config(command=self.xview)
        self.config(yscrollcommand=self.sbarV.set)
        self.config(xscrollcommand=self.sbarH.set)
        self.sbarV.pack(side=RIGHT, fill=Y)
        self.sbarH.pack(side=BOTTOM, fill=X)

    def bindings(self):
        self.bind("<MouseWheel>", self.onMouseWheel)
        self.bind("<Shift-MouseWheel>", self.onShiftMouseWheel)
        self.bind("<Up>", self.onArrowUp)
        self.bind("<Down>", self.onArrowDown)
        self.bind("<Left>", self.onArrowLeft)
        self.bind("<Right>", self.onArrowRight)
        self.bind("<Prior>", self.onArrowUp)
        self.bind("<Next>", self.onArrowDown)
        self.bind("<Shift-Prior>", self.onPrior)
        self.bind("<Shift-Next>", self.onNext)
        # self.bind("all", self.eventEcho)

    def show(self, force=False):
        if force or not self.winfo_ismapped():
            self.rootwin.iconify()
            self.rootwin.update()
            self.rootwin.deiconify()
            self.rootwin.lift()
            # self.rootwin.mainloop()
            # mainloop()

    def hide(self):
        self.rootwin.iconify()

    def resize(self, percent):
        x1, y1, x2, y2 = self.region
        canvas_breadth = max(x2 - x1, y2 - y1)
        _region = self.config('scrollregion')[4].split()
        region = tuple(float(x) for x in _region)
        print(f"region: {region}")
        x1, y1, x2, y2 = region
        breadth = max(x2 - x1, y2 - y1)
        if breadth == 0:
            return
        self.r = float(percent) / 100
        print(f"r: {self.r}")
        if self.r < 0.01 or self.r > 30:
            return
        s = self.r / (float(breadth) / canvas_breadth)
        self.scale('all', 0, 0, s, s)
        nregion = tuple(x * self.r for x in self.region)
        self.config(scrollregion=nregion)

    def onMouseWheel(self, event):
        self.yview_scroll(int(-1 * (event.delta / 120)), "units")

    def onArrowUp(self, event):
        if event.keysym == "Up":
            self.yview_scroll(-1, "units")
        else:
            self.yview_scroll(-1, "pages")

    def onArrowDown(self, event):
        if event.keysym == "Down":
            self.yview_scroll(1, "units")
        else:
            self.yview_scroll(1, "pages")

    def onArrowLeft(self, event):
        self.xview_scroll(-1, "units")

    def onArrowRight(self, event):
        # print(event.keysym)
        self.xview_scroll(1, "units")

    def onPrior(self, event):
        self.xview_scroll(1, "pages")

    def onNext(self, event):
        # print(event.keysym)
        self.xview_scroll(-1, "pages")

    def onShiftMouseWheel(self, event):
        self.xview_scroll(int(-1 * (event.delta / 120)), "units")

    def draw_axis(self, m, n):
        self.create_line(-100 * (m - 1), 0, 100 * m, 0, width=1, fill='black', arrow='last')
        self.create_line(0, -100 * (n - 1), 0, 100 * n, width=1, fill='black', arrow='last')

        for i in range(-m + 1, m):
            self.create_line(100 * i, -5, 100 * i, 0, width=1, fill='black')
            self.create_text(100 * i, -5, text=str(100 * i), font='Consolas 8', anchor='s')
        for i in range(-n + 1, n):
            self.create_line(-5, 100 * i, 0, 100 * i, width=1, fill='black')
            self.create_text(-7, 100 * i, text=str(100 * i), font='Consolas 8', anchor='e')

    def eventEcho(self, event):
        print(event.keysym)


class ResizingCanvas(XCanvas):
    def __init__(self, parent, **kwargs):
        XCanvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.on_resize)
        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

    def on_resize(self, event: Event):
        wscale = float(event.width) / self.width
        hscale = float(event.height) / self.height

        self.width = event.width
        self.height = event.height

        self.config(width=self.width, height=self.height)
        self.scale("all", 0, 0, wscale, hscale)

    def draw_point(self, p: Point2D, color='black'):
        return self.create_oval(p.x - 3, p.y - 3, p.x + 3, p.y + 3, fill=color, tags=['scroll'])

    def draw_line(self, p_start_id: int, p_end_id: int):
        p_start = self.coords(p_start_id)
        p_end = self.coords(p_end_id)
        p_vec = (p_end[0] - p_start[0], p_end[1] - p_start[1])
        p_start_draw = (p_start[0] + p_vec[0] * (-1000), p_start[1] + p_vec[1] * (-1000))
        p_end_draw = (p_start[0] + p_vec[0] * 1000, p_start[1] + p_vec[1] * 1000)
        return self.create_line(p_start_draw[0] + 3, p_start_draw[1] + 3, p_end_draw[0] + 3, p_end_draw[1] + 3, width=3)

    def draw_circle(self, circle: geometry.Circle, color='black'):
        x = circle.center.x
        y = circle.center.y
        r = circle.radius
        return self.create_oval(x - r, y - r, x + r, y + r, outline=color, width=3, tags=['scroll'])

    def clear(self):
        self.delete("all")
