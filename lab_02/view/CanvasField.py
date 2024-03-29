import math
import pickle
from dataclasses import dataclass
from typing import Callable, Any

from view.CanvasPoint import CanvasPoint
from view.CanvasLine import CanvasLine
from view.CanvasCircle import CanvasCircle
from view.Settings import Settings
from view.CanvasPolygon import *
from view.keyInput import *

from model.Tools import Tools

from tkinter import *
from tkinter.colorchooser import askcolor


# пример создания  ResizingCanvas(myFrame, width=850, height=400, bg="red", highlightthickness=0)
class ResizingCanvas(Canvas):
    def __init__(self, parent, **kwargs):
        Canvas.__init__(self, parent, **kwargs)
        self.bind("<Configure>", self.resize)

        self.bind('<1>', lambda event: self.click(event), '+')
        # self.bind("<Motion>", lambda event: self.showCoords(event), '+')
        self.bind("<Leave>", lambda event: self.hideCoords(event), '+')

        self.bind("<MouseWheel>", self.mouseZoom, '+')

        self.bind("<Shift-Down>", lambda event: self.shift(0, 10), '+')
        self.bind("<Shift-Left>", lambda event: self.shift(-10, 0), '+')
        self.bind("<Shift-Up>", lambda event: self.shift(0, -10), '+')
        self.bind("<Shift-Right>", lambda event: self.shift(10, 0), '+')

        # self.bind("<Right>", lambda event: self.arrowMoveAcrossField('X', 'right'), '+')
        # self.bind("<Left>", lambda event: self.arrowMoveAcrossField('X', 'left'), '+')
        # self.bind("<Up>", lambda event: self.arrowMoveAcrossField('Y', 'up'), '+')
        # self.bind("<Down>", lambda event: self.arrowMoveAcrossField('Y', 'down'), '+')

        self.height = self.winfo_reqheight()
        self.width = self.winfo_reqwidth()

        self.image = None

    def mouseRotate(self, mode):
        pass

    def shift(self, xShift, yShift):
        pass

    def resize(self, event):
        self.width = event.width
        self.height = event.height

        self.config(width=self.width, height=self.height)

    def click(self, event):
        print('click')

    def showCoords(self, event):
        print('showCoords')

    def hideCoords(self, event):
        print('delCoods')

    def mouseZoom(self, event):
        pass

    def plug(self, event):
        print('plus')

    def arrowMoveAcrossField(self, axis, side):
        pass


class CoordGrid(ResizingCanvas):
    def __init__(self, window, XStart=-100, XEnd=100, YStart=-100, YEnd=100, gridCoef=10, showArrows=True, **kwargs):
        super(CoordGrid, self).__init__(window, **kwargs)
        self.XStart, self.XEnd, self.YStart, self.YEnd = XStart, XEnd, YStart, YEnd

        self.XLine, self.YLine = None, None
        self.gridLines = []
        self.gridDashes = []
        self.gridText = []

        self.gridCoefX = gridCoef
        self.gridCoefY = gridCoef

        self.showArrows = showArrows

    def changeLimits(self, XStart, XEnd, YStart, YEnd, flagChangeCoef=True):
        if flagChangeCoef:
            if self.controllCoef(XStart, XEnd, YStart, YEnd):
                return Tools.EXIT_FAILURE

        self.XStart, self.XEnd, self.YStart, self.YEnd = XStart, XEnd, YStart, YEnd
        self.update()

    def coordinateShift(self, canvasPoint):
        return self.XShiftPC(canvasPoint.x), self.YShiftPC(canvasPoint.y)

    # Перевод координаты X из представления человека в представление канвы
    def XShiftPC(self, x):
        return 0 + (x - self.XStart) * self.width / abs(self.XEnd - self.XStart)

    # Перевод координаты Y из представления человека в представление канвы
    def YShiftPC(self, y):
        return self.height - (y - self.YStart) * self.height / abs(self.YEnd - self.YStart)

    # Перевод координаты X из представления канвы в представление человека
    def XShiftCP(self, x):
        return self.XStart + x * abs(self.XEnd - self.XStart) / self.width

    # Перевод координаты Y из представления канвы в представление человека
    def YShiftCP(self, y):
        return self.YEnd - y * abs(self.YEnd - self.YStart) / self.height

    # Перевод длины отрезка из представления человека в представление канвы
    def XLineShiftPC(self, lenLine):
        return lenLine * self.width / abs(self.XEnd - self.YStart)

    def arrowsShow(self):
        return
        if self.showArrows:
            self.XLine = self.create_line(0, self.height / 2, self.width, self.height / 2, fill='black', width=2,
                                          arrow=LAST)
            self.YLine = self.create_line(self.width / 2, self.height, self.width / 2, 0, fill='black', width=2,
                                          arrow=LAST)
        else:
            self.XLine = self.create_line(0, self.height / 2, self.width, self.height / 2, fill='grey', width=2,
                                          dash=(2, 2))
            self.YLine = self.create_line(self.width / 2, self.height, self.width / 2, 0, fill='grey', width=2,
                                          dash=(2, 2))

    def arrowsHide(self):
        if self.XLine:
            self.delete(self.XLine)
        if self.YLine:
            self.delete(self.YLine)
        self.XLine, self.YLine = None, None

    def arrowsUpdate(self):
        self.arrowsHide()
        self.arrowsShow()

    def gridShow(self):
        return
        # вертикальная сетка (рисуем линии параллельные оси Y)
        step = self.width / 2 / self.gridCoefX
        i = 0
        while i < self.width - step:
            i += step
            if math.fabs(i - self.width / 2) < 1:
                continue

            self.gridLines.append(self.create_line(i, self.height, i, 0, fill='grey', width=2, dash=(2, 2)))
            if self.showArrows:
                self.gridDashes.append(
                    self.create_line(i, self.height / 2 - 4, i, self.height / 2 + 4, fill='black', width=2))
                self.gridText.append(self.create_text(i, self.height / 2 - 12, text=str(int(self.XShiftCP(i))),
                                                      font=('Arial', 8, 'bold'), justify=CENTER, fill='black'))

        # горизонтальная сетка (рисуем линии параллельные оси X)
        step = self.height / 2 / self.gridCoefY
        i = 0
        while i < self.height - step:
            i += step
            if math.fabs(i - self.height / 2) < 1:
                continue
            self.gridLines.append(self.create_line(0, i, self.width, i, fill='grey', width=2, dash=(2, 2)))
            if self.showArrows:
                self.gridDashes.append(
                    self.create_line(self.width / 2 - 4, i, self.width / 2 + 4, i, fill='black', width=2))
                self.gridText.append(self.create_text(self.width / 2 + 12, i, text=str(int(self.YShiftCP(i))),
                                                      font=('Arial', 8, 'bold'), justify=CENTER, fill='black'))

        # Подпись осей координат
        if self.showArrows:
            self.gridText.append(self.create_text(self.width / 2 + 12, 12, text='Y',
                                                  font=('Arial', 10, 'bold'), justify=CENTER, fill='black'))
            self.gridText.append(self.create_text(self.width - 12, self.height / 2 + 12, text='X',
                                                  font=('Arial', 10, 'bold'), justify=CENTER, fill='black'))

    def gridHide(self):
        for line in self.gridLines:
            self.delete(line)

        for dash in self.gridDashes:
            self.delete(dash)

        for text in self.gridText:
            self.delete(text)

        self.gridLines.clear()
        self.gridDashes.clear()

    def gridUpdate(self):
        self.gridHide()
        self.gridShow()

    def update(self):
        self.arrowsUpdate()
        self.gridUpdate()

    def resize(self, event):
        super().resize(event)
        self.update()

    def zoomPlus(self, XStart, XEnd, YStart, YEnd):
        stepX = abs(XStart - XEnd) / 2 / self.gridCoefX
        while stepX < 1:
            self.gridCoefX -= 1
            stepX = abs(XStart - XEnd) / 2 / self.gridCoefX

        stepY = abs(YStart - YEnd) / 2 / self.gridCoefY
        while stepY < 1:
            self.gridCoefY -= 1
            stepY = abs(YStart - YEnd) / 2 / self.gridCoefY

    def zoomMinus(self, XStart, XEnd, YStart, YEnd):
        stepX = abs(XStart - XEnd) / 2 / self.gridCoefX
        while stepX >= 2 and self.gridCoefX < 10:
            self.gridCoefX += 1
            stepX = abs(XStart - XEnd) / 2 / self.gridCoefX

        stepY = abs(YStart - YEnd) / 2 / self.gridCoefY
        while stepY >= 2 and self.gridCoefY < 10:
            self.gridCoefY += 1
            stepY = abs(YStart - YEnd) / 2 / self.gridCoefY

    def arrowMoveAcrossField(self, axis, side):
        if axis == 'X':
            step = abs(self.XStart - self.XEnd) / self.gridCoefX / 2
            self.changeLimits(self.XStart + (step if side == 'right' else -step),
                              self.XEnd + (step if side == 'right' else -step),
                              self.YStart, self.YEnd)
        else:
            step = abs(self.YStart - self.YEnd) / self.gridCoefX / 2
            self.changeLimits(self.XStart, self.XEnd, self.YStart + (step if side == 'up' else -step),
                              self.YEnd + (step if side == 'up' else -step))

    def controllCoef(self, XStart, XEnd, YStart, YEnd):
        if abs(XEnd - XStart) <= Settings.MIN_LEN_COORDS:
            print('Слишком маленький масштаб сетки для X')
            return Tools.EXIT_FAILURE

        if abs(YEnd - YStart) <= Settings.MIN_LEN_COORDS:
            print('Слишком маленький масштаб сетки для Y')
            return Tools.EXIT_FAILURE

        self.zoomPlus(XStart, XEnd, YStart, YEnd)
        self.zoomMinus(XStart, XEnd, YStart, YEnd)

        return Tools.EXIT_SUCCESS

    def mouseZoom(self, event):
        stepX = abs(self.XStart - self.XEnd) / self.gridCoefX / 2
        stepY = abs(self.YStart - self.YEnd) / self.gridCoefX / 2
        if event.delta > 0:
            self.changeLimits(self.XStart + stepX, self.XEnd - stepX, self.YStart + stepY, self.YEnd - stepY, True)
        elif event.delta < 0:
            self.changeLimits(self.XStart - stepX, self.XEnd + stepX, self.YStart - stepY, self.YEnd + stepY, True)

    def changeCoef(self, sign, *axis):
        if sign == '+':
            self.gridCoefX = self.gridCoefX - 1 if 'X' in axis and self.gridCoefX > 1 else self.gridCoefX
            self.gridCoefY = self.gridCoefY - 1 if 'Y' in axis and self.gridCoefY > 1 else self.gridCoefY
        else:
            self.gridCoefX = self.gridCoefX + 1 if 'X' in axis and self.gridCoefX < 10 else self.gridCoefX
            self.gridCoefY = self.gridCoefY + 1 if 'Y' in axis and self.gridCoefY < 10 else self.gridCoefY

        self.update()

    def flagShowGrid(self, flag):
        self.showArrows = flag
        self.update()


@dataclass
class UndoObject:
    func: Callable
    args: list[Any]
    kwargs: dict[Any]


class CartesianField(CoordGrid):
    def __init__(self, rootFrame, root, colorPoints=Settings.COLOR_LINE,
                 XStart=-100, XEnd=100, YStart=-100, YEnd=100, gridCoef=10, showArrows=False, **kwargs):
        super(CartesianField, self).__init__(rootFrame, XStart, XEnd, YStart, YEnd, gridCoef, showArrows, **kwargs)
        self.root = root

        self.points = []
        self.lines = []
        self.circles = []

        self.t = None

        self.colorPoints = colorPoints

        self.ShowComments = False

    def showCoords(self, event):
        if self.t:
            self.delete(self.t)

        if self.ShowComments:
            self.t = self.create_text(event.x + 10, event.y - 10,
                                      text=str(int(self.XShiftCP(event.x))) + ", " + str(int(self.YShiftCP(event.y))),
                                      font=('Arial', 8, 'bold'), justify=CENTER, fill='black')

    def hideCoords(self, event):
        if self.t:
            self.delete(self.t)

    def clear(self):
        for point in self.points:
            point.hide(self)
        self.points.clear()
        self.clearResult()

    def clearResult(self):
        for line in self.lines:
            line.hide(self)
        for circle in self.circles:
            circle.hide(self)

        self.lines.clear()
        self.circles.clear()

    def changeColorPoints(self, points, newColor=Settings.COLOR_POINT_FIRST_SET):
        for p in points.getAll():
            p.changeColor(self, newColor)

    def showPoint(self, x, y, color=Settings.COLOR_NEW_POINT):
        point = CanvasPoint(float(x), float(y), showComments=self.ShowComments)
        self.points.append(point)
        point.show(self)

    def showLine(self, start, end, color=Settings.COLOR_LINE):
        line = CanvasLine(start, end, color)
        self.lines.append(line)
        line.show(self)

    def showCircle(self, center, r, color, width=2, activefill=None):
        circle = CanvasCircle(center, r, color, width, activefill, showComments=self.ShowComments)
        self.circles.append(circle)
        circle.show(self)

    def update(self):
        super().update()
        self.updateShowFlags()

        for point in self.points:
            point.reShow(self)

        for line in self.lines:
            line.reShow(self)

        for circle in self.circles:
            circle.reShow(self)


    def loadCanva(self, f):
        try:
            points = pickle.load(f)
            lines = pickle.load(f)
            circles = pickle.load(f)
        except:
            print('Ошибка загрузки данных')
            return Tools.EXIT_FAILURE

        self.clear()
        self.points = points
        self.lines = lines
        self.circles = circles

        self.update()
        return Tools.EXIT_SUCCESS

    def rightClick(self, XEvent, YEvent):
        if not XEvent or not YEvent:
            print('No')
            return

        for i, point in enumerate(self.points):
            if point.isClick(self, XEvent, YEvent):
                point.hide(self)
                self.points.pop(i)

    def updateShowFlags(self):
        for point in self.points:
            point.ShowComments = self.ShowComments
        for circle in self.circles:
            circle.ShowComments = self.ShowComments


class PolygonField(CartesianField):
    def __init__(self, rootFrame, root, **kwargs):
        super(PolygonField, self).__init__(rootFrame, root, **kwargs)

        self.colorNowPol = Settings.COLOR_LINE
        self.polygons = [CanvasPolLine([], self.colorNowPol)]

        self.fillPoint = None
        self.rotatePoint = CanvasPoint(0, 0)
        self.undo_list = []

    def showCoords(self, event):
        super(PolygonField, self).showCoords(event)
        if event.x and event.y:
            if self.fillPoint:
                self.fillPoint.hideHightlight(self)

            self.fillPoint = self.pointInPolWithPoint(float(event.x), float(event.y))

            if self.fillPoint:
                self.fillPoint.highlight(self)
            self.update()

    def clear(self):
        for pol in self.polygons:
            pol.hide(self)
        self.polygons = [CanvasPolLine([], self.colorNowPol)]

    def clearResult(self):
        self.clear()

    def update(self):
        super(PolygonField, self).update()
        for pol in self.polygons:
            pol.reShow(self)

        ''' РАСКОММЕНТИРОВАТЬ ЭТУ СТРОКУ ДЛЯ ПОКАЗА ТОЧКИ ПОВОРОТА '''
        self.rotatePoint.reShow(self)


    def loadCanva(self, f):
        try:
            polygons = pickle.load(f)
        except:
            print('Ошибка загрузки полигона')
            return Tools.EXIT_FAILURE

        self.clear()

        self.polygons = polygons
        self.update()
        return Tools.EXIT_SUCCESS

    def updateShowFlags(self):
        super(PolygonField, self).updateShowFlags()
        for pol in self.polygons:
            pol.updateShowFlag(self.ShowComments)

    def rightClick(self, XEvent, YEvent):
        for pol in self.polygons:
            for i, point in enumerate(pol.points):
                if point.isClick(self, XEvent, YEvent):
                    point.hide(self)
                    pol.points.pop(i)

        self.update()

    def changeColor(self, XEvent, YEvent):
        color = askcolor()[1]
        if not color:
            return

        for pol in self.polygons:
            for i, point in enumerate(pol.points):
                if point.isClick(self, XEvent, YEvent):
                    pol.changeColor(color, color)

        self.update()

    def startNewPolygon(self, event):
        self.polygons.append(CanvasPolLine([], color=self.colorNowPol))

    def startNewPolygonClose(self, event):
        try:
            lastPoint = CanvasPoint(self.polygons[-1].points[0].x, self.polygons[-1].points[0].y,
                                    color=self.colorNowPol)
            self.polygons[-1].addPoint(self, lastPoint)
        except:
            pass
        self.startNewPolygon(event)

    def updatePoints(self):
        self.points = []
        for pol in self.polygons:
            for i in pol.points:
                self.points.append(i)

    def isPointInPol(self, X, Y):
        for pol in self.polygons:
            if pol.isPointOn(self, X, Y):
                return True
        return False

    def pointInPolWithPoint(self, X, Y):
        for pol in self.polygons:
            p = pol.PointOnWithPoint(self, X, Y)
            if p:
                return p
        return None

    def showPoint(self, x, y, color=Settings.COLOR_NEW_POINT):
        point = CanvasPoint(float(x), float(y), showComments=self.ShowComments, color=self.colorNowPol)
        self.polygons[-1].addPoint(self, point)

    def delPoint(self, point):
        wasDel = False
        for pol in self.polygons:
            wasDel += pol.delPoint(self, point)

        self.update()
        return wasDel

    def rotate(self, pointerCenter, alpha, track=True):
        if track:
            undo_obj = UndoObject(func=self.rotate, args=[pointerCenter, -alpha], kwargs={'track': False})
            self.undo_list.append(undo_obj)
        for pol in self.polygons:
            pol.hide(self)
            pol.rotatePol(pointerCenter, alpha)

        self.rotatePoint = pointerCenter
        self.update()

    def shift(self, xShift, yShift, track=True):
        if track:
            undo_obj = UndoObject(func=self.shift, args=[-xShift, -yShift], kwargs={'track': False})
            self.undo_list.append(undo_obj)
        for pol in self.polygons:
            pol.hide(self)
            pol.shiftPol(xShift, yShift)

        self.update()

    def scale(self, kx, ky, track=True):
        if track:
            undo_obj = UndoObject(func=self.scale, args=[1 / kx, 1 / ky], kwargs={'track': False})
            self.undo_list.append(undo_obj)
        for pol in self.polygons:
            pol.hide(self)
            pol.scalePol(self.rotatePoint.x, self.rotatePoint.y, kx, ky)

        self.update()

    def undo(self):
        if not self.undo_list:
            return
        undo_obj = self.undo_list.pop()
        undo_obj.func(*undo_obj.args, **undo_obj.kwargs)

    def mouseRotate(self, mode):
        if mode == 'r':
            self.rotate(self.rotatePoint, -15)
        elif mode == 'l':
            self.rotate(self.rotatePoint, 15)

    def changeRotatePoint(self, x, y, track=True):
        if track:
            x_prev = self.XShiftPC(self.rotatePoint.x)
            y_prev = self.YShiftPC(self.rotatePoint.y)
            undo_obj = UndoObject(func=self.changeRotatePoint,
                                  args=[x_prev, y_prev], kwargs={'track': False})
            self.undo_list.append(undo_obj)
        x = int(self.XShiftCP(x))
        y = int(self.YShiftCP(y))
        self.rotatePoint.hide(self)
        self.rotatePoint = CanvasPoint(x, y,
                                             'red', showComments=self.ShowComments)
        if track:
            showinfo('Info', 'Новый центр поворота установлен успешно.\n\n'
                             f'X: {x}\n'
                             f'Y: {y}\n')
        self.update()


class WrapCanva:
    def __init__(self, window, Canva=PolygonField, **kwargs):
        self.window = window

        self.frame = Frame(window)
        self.canva = Canva(self.frame, self.window, showArrows=False, **kwargs)
        self.frame.bind('<Configure>', self.resize, '+')
        self.canva.place(x=0, y=0)

        self.pointMenu = None
        self.Xevent, self.Yevent = None, None
        self.bind()

    def bind(self):
        self.window.bind("<Right>", lambda event: self.canva.shift(15, 0))
        self.window.bind("<Left>", lambda event: self.canva.shift(-15, 0))
        self.window.bind("<Up>", lambda event: self.canva.shift(0, 15))
        self.window.bind("<Down>", lambda event: self.canva.shift(0, -15))

        self.window.bind("<Control-equal>", lambda event: self.canva.scale(2, 2))
        self.window.bind("<Control-minus>", lambda event: self.canva.scale(0.5, 0.5))

        self.window.bind("<Control-z>", lambda event: self.canva.undo())
        self.window.bind("<Control-p>", lambda event: self.canva.rotate(self.canva.rotatePoint, -15))
        self.window.bind("<Control-o>", lambda event: self.canva.rotate(self.canva.rotatePoint, 15))

        self.pointMenu = Menu(self.canva, tearoff=0)
        self.pointMenu.add_command(label="Установить точку-якорь", command=lambda: self.changeRotatePoint())

        self.mainMenu = Menu(self.canva, tearoff=0)
        self.mainMenu.add_command(label="Установить точку-якорь", command=lambda: self.changeRotatePoint())

        self.window.bind("<Button-3>", lambda event: self.rightClick(event), '+')

    def changeRotatePoint(self, track=True):
        self.canva.changeRotatePoint(self.Xevent, self.Yevent)

    def action(self, frame):
        z = Toplevel(self.window)
        z.geometry('200x200')
        z.title('')
        z['bg'] = Settings.COLOR_MAIN_BG
        z.resizable(0, 0)
        f = frame(z, 200, 200, self)
        f.show()

    def rightClick(self, event):
        self.Xevent = event.x
        self.Yevent = event.y

        isPointHere = self.canva.isPointInPol(self.Xevent, self.Yevent)

        if isPointHere:
            self.pointMenu.post(event.x_root, event.y_root)
        else:
            self.mainMenu.post(event.x_root, event.y_root)

    def resize(self, event):
        self.canva.resize(event)

    def show(self, x, y, relwidth, relheight):
        self.frame.place(x=x, y=y, relwidth=relwidth, relheight=relheight)

    def clear(self):
        self.canva.clear()

    def getPoints(self):
        return [point for p in self.canva.polygons for point in p.points]

    def radioShowComments(self):
        self.canva.ShowComments = not self.canva.ShowComments
        self.canva.update()

    def changeColorNewPol(self):
        color = askcolor()[1]
        if not color:
            return

        self.canva.colorNowPol = color
        self.canva.polygons[-1].changeColor(color, color)

        self.canva.update()
