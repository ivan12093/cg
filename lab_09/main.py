import sys

from PyQt5.uic import loadUi
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QColorDialog, QMessageBox, QGraphicsScene, QWidget, QListWidget, QListWidgetItem
from PyQt5.QtGui import QColor, QPen, QPixmap, QBrush, QImage, QPainter, QTransform
from PyQt5.QtCore import QRect, QCoreApplication, QEventLoop, QPointF, QTimerEvent
from math import sqrt, pow
from copy import deepcopy


from mainwindow_ui import *
EPS = 1e-6

class myList(QtWidgets.QListWidget):
    def __init__(self, a, win):
        super().__init__(a)
        self.itemClicked.connect(self.listwidgetclicked)

    def listwidgetclicked(self, item):
        if item.text() != "Ребра отсекателя":
            win.set_chosen(item)
        else:
            win.redraw_all()

    

class myScene(QtWidgets.QGraphicsScene):
    def __init__(self, a, b, c, d, win):
        super().__init__(a, b, c, d)
        self.close_clip = None
        self.close_polygon = None
        self.vert = False
        self.horiz = False
        self.last_clip = None
        self.last_polygon = None
        self.placement = False

    def clear(self):
        super().clear()

    def hard_clear(self):
        super().clear()
        self.close_clip = None
        self.close_polygon = None
        self.vert = False
        self.horiz = False
        self.last_clip = None
        self.last_polygon = None
        self.placement = False

    def mousePressEvent(self, e):
        if e.button() == 1: #ЛКМ
            if self.close_polygon == None:
                t = win.item
                win.polygon = []
                self.clear()
                self.close_polygon = None
                win.redraw_clip()
                if t!=None:
                    win.set_chosen(t)
            if win.checkBox_on_clip.isChecked():
                self.add_on_clip(round(e.scenePos().x()), round(e.scenePos().y()))
            else:
                self.add_point(round(e.scenePos().x()), round(e.scenePos().y()), win.pen, mode = "polygon")
        elif e.button() == 2: #ПКМ
            if self.close_clip == None:
                self.clear()
                self.close_clip = None
                win.redraw_polygon()
                win.clip = []
                win.listWidget.clear()
                win.listWidget.addItem("Ребра отсекателя")
                win.chosen = None
                win.checkBox_on_clip.setChecked(0)
            self.add_point(round(e.scenePos().x()), round(e.scenePos().y()), win.pen, mode = "clip")


    def keyPressEvent(self, e):
        # 16777248 shift горизонт
        # 16777249 ctrl вертик
        if not e.isAutoRepeat():
            if e.key() == 16777248:
                self.horiz = True
            elif e.key() == 16777249:
                self.vert = True

    def keyReleaseEvent(self, e):
        # 16777248 shift горизонт
        # 16777249 ctrl вертик
        if not e.isAutoRepeat():
            if e.key() == 16777248:
                self.horiz = False
            elif e.key() == 16777249:
                self.vert = False
        
        

class Window(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.chosen = None

        self.color_clipped = QColor() 
        self.color_line = QColor() 
        self.color_edge = QColor()

        self.color_edge_def()
        self.color_clipped_def()
        self.color_line_def()

        self.rad_clip.setChecked(1)
        self.pen = QPen(self.color_edge)

        self.polygon = []
        self.clip = []
        self.rcontent = self.graphicsView.contentsRect()
        self.scene = myScene(0, 0, self.rcontent.width(), self.rcontent.height(), self)
        self.graphicsView.setScene(self.scene)
        self.msg = QMessageBox()
        self.msg.setIcon(QMessageBox.Critical)
        self.msg.setWindowTitle("Ошибка ввода")
        self.item = None

        font = QtGui.QFont()
        font.setPointSize(11)
        tmp = self.listWidget.geometry()
        self.listWidget.hide()
        self.listWidget = myList(self.centralwidget, self)
        self.listWidget.setGeometry(tmp)
        self.listWidget.setObjectName("listWidget")
        self.listWidget.addItem("Ребра отсекателя")

        self.bind()
        self.clear()

    def close_clip(self):
        if self.scene.close_clip == None:
            self.msg.setText("Операция невозможна: отсекатель уже замкнут или не введено еще ни одной точки")
            self.msg.show()
            return
        self.scene.add_point(self.scene.close_clip[0], self.scene.close_clip[1], self.pen, mode = "clip")
        self.scene.close_clip = None
        self.centre = self.find_centre()

    def find_centre(self):
        x0 = self.clip[0][0][0]
        x1 = self.clip[0][0][0]
        y0 =  self.clip[0][0][1]
        y1 = self.clip[0][0][1]
        for i in self.clip:
            if i[0][0] > x1:
                x1 = i[0][0]
            if i[0][0] < x0:
                x0 = i[0][0]
            if i[0][1] > y1:
                y1 = i[0][1]
            if i[0][1] < y0:
                y0 = i[0][1]
        return [(x1 + x0)/2, (y1 + y0)/2]
    
    def close_polygon(self):
        if self.scene.close_polygon == None:
            self.msg.setText("Операция невозможна: отсекаемый многоугольник уже замкнут или не введено еще ни одной точки")
            self.msg.show()
            return
        self.scene.add_point(self.scene.close_polygon[0], self.scene.close_polygon[1], self.pen, mode = "polygon")
        self.scene.close_polygon = None

    def choose_color_clipped(self):
        self.color_clipped = QColorDialog.getColor()
        self.color_ind_clipped.setStyleSheet("background-color:" + self.color_clipped.name() + ";border: 1px solid black;")

    def choose_color_edge(self):
        self.color_edge = QColorDialog.getColor()
        self.color_ind_edge.setStyleSheet("background-color:" + self.color_edge.name() + ";border: 1px solid black;")

    def choose_color_line(self):
        self.color_line = QColorDialog.getColor()
        self.color_ind_line.setStyleSheet("background-color:" + self.color_line.name() + ";border: 1px solid black;")
        
    def color_clipped_def(self):
        self.color_clipped.setRgb(0, 0, 255)
        self.color_ind_clipped.setStyleSheet("background-color:" + self.color_clipped.name() + ";border: 1px solid black;")

    def color_edge_def(self):
        self.color_edge.setRgb(0, 0, 0)
        self.color_ind_edge.setStyleSheet("background-color:" + self.color_edge.name() + ";border: 1px solid black;")

    def color_line_def(self):
        self.color_line.setRgb(255, 0, 0)
        self.color_ind_line.setStyleSheet("background-color:" + self.color_line.name() + ";border: 1px solid black;")

    def redraw_polygon(self):
        self.pen.setColor(self.color_line)
        for i in range(len(self.polygon) - 1):
            self.scene.addLine(self.polygon[i][0], self.polygon[i][1], self.polygon[i + 1][0], self.polygon[i + 1][1], self.pen)

    def redraw_clip(self):
        self.pen.setColor(self.color_edge)
        for i in self.clip:
            self.scene.addLine(i[0][0], i[0][1], i[1][0], i[1][1], self.pen)
    
    def redraw_all(self):
        self.scene.clear()
        self.redraw_clip()
        self.redraw_polygon()

    def clear(self):
        self.scene.hard_clear()
        self.listWidget.clear()
        self.listWidget.addItem("Ребра отсекателя")
        self.polygon = []
        self.clip = []
        self.last_dot = None
        self.item = None
        self.length = None
   
    def init_dot_add(self):
        x,y = self.get_dot_vals()
        if x >= 0:
            st = "clip" if self.rad_clip.isChecked() else "polygon" 
            self.scene.add_point(x, y, self.pen, mode = st)

    
    def get_dot_vals(self):
        try:
            x= int(self.line_x.text().strip())
            if (x < 0):
                self.msg.setText("Ошибка ввода в поле координаты X. Необходимо ввести ровно одно целое неотрицательное число.")
                self.msg.show() 
                return -1, -1
        except:
            self.msg.setText("Ошибка ввода в поле координаты X. Необходимо ввести ровно одно целое неотрицательное число.")
            self.msg.show()
            return -1, -1

        try:
            y= int(self.line_y.text().strip())
            if (y < 0):
                self.msg.setText("Ошибка ввода в поле координаты Y. Необходимо ввести ровно одно целое неотрицательное число.")
                self.msg.show() 
                return -1, -1
        except:
            self.msg.setText("Ошибка ввода в поле координаты Y. Необходимо ввести ровно одно целое неотрицательное число.")
            self.msg.show()
            return -1, -1
        return x, y

    def set_chosen(self, item):
        s1, s2, s3, s4= item.text().split()
        x1, y1, x2, y2 = map(int, [s1[1:-1], s2[:-1], s3[1:-1], s4[:-1]])

        self.chosen = [x1, y1, x2, y2]
        self.redraw_all()
        self.pen.setColor(QColor(0, 255,0))
        self.pen.setWidth(2)
        self.scene.addLine(x1, y1, x2, y2, self.pen)
        self.pen.setWidth(1)
        self.item = item
        
    def bind(self):
        self.but_clear.clicked.connect(self.clear)
        self.but_close_clip.clicked.connect(self.close_clip)
        self.but_close_polygon.clicked.connect(self.close_polygon)
        self.but_add_dot.clicked.connect(self.init_dot_add)
        self.but_clip.clicked.connect(self.cut)
        self.but_color_clipped.clicked.connect(self.choose_color_clipped)
        self.but_color_edge.clicked.connect(self.choose_color_edge)
        self.but_color_line.clicked.connect(self.choose_color_line)
        self.but_color_clipped_def.clicked.connect(self.color_clipped_def)
        self.but_color_line.clicked.connect(self.color_line_def)
        self.but_color_edge_def.clicked.connect(self.color_edge_def)

    
    def cut(self):
        pass


    def sh_cut(self, poly, cl, centre):
        pass
            
    
    def draw_edges(self, poly):
        for i in range(len(poly) - 1):
            self.scene.addLine(poly[i][0], poly[i][1], poly[i + 1][0], poly[i + 1][1], self.pen)


# точка пересечения отрезка и прямой (none, если не пересекаются)
def segment_and_line_intersection(sp1, sp2, edge):
    segment = find_line_by_2points(sp1, sp2)
    line = find_line_by_2points(edge[0], edge[1])
    intersection = find_lines_intersection(segment, line)
    if intersection and check_fit(intersection, sp1, sp2):
        return intersection
    return None
    
# найти точку пересечения 2 прямых line1 и line2
def find_lines_intersection(line1, line2):
    # параллельные
    if abs(line1['a'] * line2['b'] - line2['a'] * line1['b']) < EPS:
        return None
    if abs(line1['a']) < EPS and abs(line1['b']) < EPS:
        return None
    # точка должна принадлежать обеим прямым, поэтому получаем систему
    # a1x + b1y + c1 = 0
    # a2x + b2y + c2 = 0
    # если первая прямая параллельна оси ox
    if abs(line1['a']) < EPS:
        y0 = -1 * line1['c'] / line1['b']
        x0 = ((line2['b'] * line1['c'] - line1['b'] * line2['c']) /
              (line1['b'] * line2['a']))
    else:
        y0 = ((line2['a'] * line1['c'] - line1['a'] * line2['c']) /
              (line1['a'] * line2['b'] - line2['a'] * line1['b']))
        x0 = -1 * (line1['b'] * y0 + line1['c']) / line1['a']
    dot = [x0, y0]
    return dot

# проверка видимости точки dot относительно ребра 
# с помощью скалярного произведения нормали и вектора от point1 до точки
def is_visible(dot, edge, centre):
    point1, point2 = edge
    normal = inner_normal(edge, centre)
    vector = [dot[0] - point1[0], dot[1] - point1[1]]
    if scalar_mult_sign(normal, vector) >= 0:
        return True
    return False

# внутренняя нормаль к стороне
def inner_normal(edge, central):
    point1, point2 = edge
    i = point2[0] - point1[0]
    j = point2[1] - point1[1]

    if j == 0:
        normal = [0, 1]
    else:
        normal = [j, -i]

    if scalar_mult_sign(normal, [central[0] - point2[0], central[1] - point2[1]]) < 0:
        normal[0] *= -1
        normal[1] *= -1
    return normal


def scalar_mult_sign(vec1, vec2):
    sm = scalar_mult(vec1, vec2)
    if sm > 0:
        return 1
    elif sm < 0:
        return -1
    return 0

# принадлежность точки прямой отрезку
def check_fit(dot, point1, point2):
    if ((min(point1[0], point2[0]) <= dot[0] <= max(point1[0], point2[0])) and
            (min(point1[1], point2[1]) <= dot[1] <= max(point1[1], point2[1]))):
        return True
    return False

   # скалярное произведение векторов vec1 и vec2
def scalar_mult(vec1, vec2):
    return vec1[0] * vec2[0] + vec1[1] * vec2[1]

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = Window()
    win.show()
    sys.exit(app.exec())
