import sys
from random import random

from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QSpacerItem, QSizePolicy, \
    QLabel, QLineEdit, QPushButton
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter, QColor, QPen
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
import mainSolve
from matplotlib.figure import Figure
from mainSolve import sol
import numpy as np

i = 0
main_window = None
solution = None
GraphicWindow0 = None
GraphicWindow1 = None
GraphicWindow2 = None
GraphicWindow3 = None
GraphicWindow4 = None


class MplCanvas(FigureCanvas):

    def __init__(self, parent=None, width=10, height=4, dpi=100):
        fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = fig.add_subplot(111)
        super(MplCanvas, self).__init__(fig)


class GraphicWindow(QWidget):

    def __init__(self, flag: int):
        super().__init__()
        self.flag = flag
        self.setWindowTitle('PySide2 Matplotlib Example')

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.canvas = MplCanvas(self, width=5, height=4, dpi=100)
        layout.addWidget(self.canvas)
        self.plot_data()

    def plot_data(self):
        sol = mainSolve.solveDiffEq()
        t = sol.t
        print('update ', sol.y[0][0], ' ', sol.y[2][0])
        y = None
        label_title = "Ec(t)"
        label_x = "t"
        label_y = "Ec"
        if self.flag == 0:
            y = np.array(mainSolve.potential_energy())
            label_title = "Ep(t)"
            label_x = "t"
            label_y = "Ep"
        elif self.flag == 1:
            y = np.array(mainSolve.cinetic_energu())
        elif self.flag == 2:
            # y = np.zeros(len(mainSolve.cinetic_energu()))
            pot_en = mainSolve.potential_energy()
            cin_en = mainSolve.cinetic_energu()
            print(pot_en[0], cin_en[0])
            y = [0] * len(pot_en)
            for i in range(0, 2000):
                y[i] = round(pot_en[i] + cin_en[i], 1)
            print(y[0])
            y = np.array(y)
            print(y[0])
            label_title = "Eabs(t)"
            label_x = "t"
            label_y = "Eabs"
        elif self.flag == 3:
            y = mainSolve.solveDiffEq().y[0]
            label_title = "x(t)"
            label_x = "t"
            label_y = "x"
        elif self.flag == 4:
            y = mainSolve.solveDiffEq().y[2]
            label_title = "y(t)"
            label_x = "t"
            label_y = "y"
        self.canvas.axes.clear()
        self.canvas.axes.plot(t[:2000], y[:2000])
        self.canvas.axes.set_title(label_title)
        self.canvas.axes.set_xlabel(label_x)
        self.canvas.axes.set_ylabel(label_y)
        self.canvas.draw()

    def update_plot(self):
        print('update - ', self)
        sol = mainSolve.solveDiffEq()
        t = sol.t
        print('update ', sol.y[0][0], ' ', sol.y[2][0])
        y = None
        label_title = "Ec(t)"
        label_x = "t"
        label_y = "Ec"
        if self.flag == 0:
            y = np.array(mainSolve.potential_energy())
            label_title = "Ep(t)"
            label_x = "t"
            label_y = "Ep"
        elif self.flag == 1:
            y = np.array(mainSolve.cinetic_energu())
        elif self.flag == 2:
            # y = np.zeros(len(mainSolve.cinetic_energu()))
            pot_en = mainSolve.potential_energy()
            cin_en = mainSolve.cinetic_energu()
            y = [0] * len(pot_en)
            for i in range(0, len(pot_en)):
                y[i] = round(pot_en[i] + cin_en[i], 1)
            y = np.array(y)
            label_title = "Eabs(t)"
            label_x = "t"
            label_y = "Eabs"
        elif self.flag == 3:
            y = mainSolve.solveDiffEq().y[0]
            label_title = "x(t)"
            label_x = "t"
            label_y = "x"
        elif self.flag == 4:
            y = mainSolve.solveDiffEq().y[2]
            label_title = "y(t)"
            label_x = "t"
            label_y = "y"
        self.canvas.axes.clear()
        self.canvas.axes.plot(t[:2000], y[:2000])
        self.canvas.axes.set_title(label_title)
        self.canvas.axes.set_xlabel(label_x)
        self.canvas.axes.set_ylabel(label_y)
        self.canvas.draw()


def start_calculate():
    mainSolve.k1 = float(main_window.k1_text_input.text())
    mainSolve.k2 = float(main_window.k2_text_input.text())
    mainSolve.l = float(main_window.l_text_input.text())
    # print(int(main_window.l_text_input.text()))
    mainSolve.x_0 = float(main_window.x0_text_input.text())
    mainSolve.y_0 = float(main_window.y0_text_input.text())
    mainSolve.vx_ = float(main_window.vx_text_input.text())
    mainSolve.vy_ = float(main_window.vy_text_input.text())
    global solution, GraphicWindow1
    solution = mainSolve.solveDiffEq()
    GraphicWindow0.update_plot()
    GraphicWindow1.update_plot()
    GraphicWindow2.update_plot()
    GraphicWindow3.update_plot()
    GraphicWindow4.update_plot()
    area = main_window.get_area()
    area.timer.start(10)

    print('Start')


def stopCalculate():
    area = main_window.get_area()
    area.timer.stop()
    print("Stop!!")
    main_window.red_area = MovingRectangleWidget()


def open_new_window(self):
    global main_window
    main_window.close()
    new_window = MainWindow()
    new_window.show()
    main_window = new_window


class MovingRectangleWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.rect_x1 = 250
        self.rect_y1 = 50
        self.trace_x1 = []
        self.trace_y1 = []
        self.rect_width = 10
        self.rect_height = 10
        self.dx = 2
        self.dy = 2

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_position)

    def update_position(self):
        global i, solution
        sol = solution
        # print(sol.y[0][i], sol.y[1][i])
        self.rect_x1 = int(sol.y[0][i] * 100) + 145
        self.rect_y1 = -int(sol.y[2][i] * 100) + 145
        self.trace_x1.append(self.rect_x1 + 5)
        self.trace_y1.append(self.rect_y1 + 5)

        i += 1
        # print(self.rect_x, self.rect_y)

        self.update()

    def paintCube(self):
        pass

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.setBrush(QColor(255, 255, 255))
        painter.setPen(QPen(Qt.black, 2, Qt.SolidLine))
        painter.drawRect(0, 0, self.width(), self.height())
        painter.setBrush(QColor(0, 0, 255))
        painter.drawRect(self.rect_x1, self.rect_y1, self.rect_width, self.rect_height)
        painter.drawLine(0, self.height() // 2, int(self.width()), self.height() // 2)
        painter.drawLine(self.width() // 2, 0, self.width() // 2, int(self.height()))
        pen = QPen(QColor(200, 200, 200), 5)
        painter.setPen(pen)
        # painter.drawPoint(self.trace_x1[0], self.trace_y1[0])
        # painter.drawPoint(145, 145)
        for j in range(len(self.trace_x1)):
            # print('trace x -', int(self.trace_x1[j]), int(self.trace_y1[j]))
            painter.drawPoint(int(self.trace_x1[j]), int(self.trace_y1[j]))


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        # super().showMaximized()
        self.setWindowTitle('Модель физической задачи (тело находиться между двумя пружинами)')
        # self.setGeometry(50, 50, 1500, 1000)

        # Создание основного виджета
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Создание красной области для движущегося прямоугольника
        self.red_area = MovingRectangleWidget()
        self.red_area.setFixedSize(300, 300)

        # Создание макета для основного виджета
        layout_first = QHBoxLayout()

        # Добавление красной области и заполнителей для позиционирования
        left_spacer = QSpacerItem(2, 0, QSizePolicy.Minimum, QSizePolicy.Expanding)
        layout_first.addItem(left_spacer)
        layout_first.addWidget(self.red_area)
        # right_spacer = QSpacerItem(0, 0, QSizePolicy.Expanding, QSizePolicy.Expanding)
        # layout.addItem(right_spacer)
        v_layout = QVBoxLayout()
        v_layout.setSpacing(0)

        h_m_layout = QHBoxLayout()
        self.m_input = QLabel("m = ")
        self.m_text_input = QLineEdit()
        self.m_text_input.setText(str(5))
        self.m_text_input.setFixedWidth(100)
        h_m_layout.addWidget(self.m_input)
        h_m_layout.addWidget(self.m_text_input)

        container_m = QWidget()
        container_m.setLayout(h_m_layout)

        k1_layout = QHBoxLayout()
        self.k1_input = QLabel("k1 = ")
        self.k1_text_input = QLineEdit()
        self.k1_text_input.setText(str(7))
        self.k1_text_input.setFixedWidth(100)
        k1_layout.addWidget(self.k1_input)
        k1_layout.addWidget(self.k1_text_input)

        container_k1 = QWidget()
        container_k1.setLayout(k1_layout)

        k2_layout = QHBoxLayout()
        self.k2_input = QLabel("k2 = ")
        # self.k2_input.setFixedSize(100)
        self.k2_text_input = QLineEdit()
        self.k2_text_input.setText(str(7))
        self.k2_text_input.setFixedWidth(100)
        # self.k2_text_input.setStyleSheet("QLineEdit { width: 10px; }")
        k2_layout.addWidget(self.k2_input)
        k2_layout.addWidget(self.k2_text_input)

        container_k2 = QWidget()
        container_k2.setLayout(k2_layout)

        l_layout = QHBoxLayout()
        self.l_input = QLabel("l = ")
        self.l_text_input = QLineEdit()
        self.l_text_input.setText(str(3))
        self.l_text_input.setFixedWidth(100)
        l_layout.addWidget(self.l_input)
        l_layout.addWidget(self.l_text_input)

        container_l = QWidget()
        container_l.setLayout(l_layout)

        x0_layout = QHBoxLayout()
        self.x0_input = QLabel("x0 = ")
        self.x0_text_input = QLineEdit()
        self.x0_text_input.setText(str(1))
        self.x0_text_input.setFixedWidth(100)
        x0_layout.addWidget(self.x0_input)
        x0_layout.addWidget(self.x0_text_input)

        container_x0 = QWidget()
        container_x0.setLayout(x0_layout)

        y0_layout = QHBoxLayout()
        self.y0_input = QLabel("y0 = ")
        self.y0_text_input = QLineEdit()
        self.y0_text_input.setText(str(1))
        self.y0_text_input.setFixedWidth(100)
        y0_layout.addWidget(self.y0_input)
        y0_layout.addWidget(self.y0_text_input)

        container_y0 = QWidget()
        container_y0.setLayout(y0_layout)

        vx_layout = QHBoxLayout()
        self.vx_input = QLabel("vx = ")
        self.vx_text_input = QLineEdit()
        self.vx_text_input.setText(str(0))
        self.vx_text_input.setFixedWidth(100)
        # self.vx_text_input.setAlignment(Qt.AlignLeft)
        vx_layout.addWidget(self.vx_input)
        vx_layout.addWidget(self.vx_text_input)

        container_vx = QWidget()
        container_vx.setLayout(vx_layout)

        vy_layout = QHBoxLayout()
        self.vy_input = QLabel("vy = ")
        self.vy_text_input = QLineEdit()
        self.vy_text_input.setText(str(0))
        self.vy_text_input.setFixedWidth(100)
        vy_layout.addWidget(self.vy_input)
        vy_layout.addWidget(self.vy_text_input)

        container_vy = QWidget()
        container_vy.setLayout(vy_layout)

        start_btn_layout = QHBoxLayout()
        self.start_btn = QPushButton('Start!')
        start_btn_layout.addWidget(self.start_btn)
        self.start_btn.clicked.connect(start_calculate)

        stop_btn_layout = QHBoxLayout()
        self.stop_btn = QPushButton('Stop!')
        stop_btn_layout.addWidget(self.stop_btn)
        self.stop_btn.clicked.connect(stopCalculate)

        reset_btn_layout = QHBoxLayout()
        self.reset_btn = QPushButton('Reset')
        reset_btn_layout.addWidget(self.reset_btn)
        self.reset_btn.clicked.connect(open_new_window)

        container_start_btn = QWidget()
        container_start_btn.setLayout(start_btn_layout)
        container_stop_btn = QWidget()
        container_stop_btn.setLayout(stop_btn_layout)
        container_reset_btn = QWidget()
        container_reset_btn.setLayout(reset_btn_layout)
        global GraphicWindow0, GraphicWindow1, GraphicWindow2, GraphicWindow3, GraphicWindow4
        GraphicWindow0 = GraphicWindow(0)
        GraphicWindow1 = GraphicWindow(1)
        GraphicWindow2 = GraphicWindow(2)
        GraphicWindow3 = GraphicWindow(3)
        GraphicWindow4 = GraphicWindow(4)
        potential_graph = GraphicWindow0
        cinetic_graph = GraphicWindow1
        absalut_graph = GraphicWindow2
        x_t_graph = GraphicWindow3
        y_t_graph = GraphicWindow4
        graph_layout = QHBoxLayout()
        graph_layout.addWidget(potential_graph)
        graph_layout.addWidget(cinetic_graph)
        # graph_layout.addWidget(absalut_graph)
        graph_layout.addWidget(x_t_graph)
        graph_layout.addWidget(y_t_graph)

        v_layout.addWidget(container_m)
        v_layout.addWidget(container_k1)
        v_layout.addWidget(container_k2)
        v_layout.addWidget(container_l)
        v_layout.addWidget(container_x0)
        v_layout.addWidget(container_y0)
        v_layout.addWidget(container_vx)
        v_layout.addWidget(container_vy)
        v_layout.addWidget(container_start_btn)
        v_layout.addWidget(container_stop_btn)
        v_layout.addWidget(container_reset_btn)
        # v_layout.set

        container1 = QWidget()
        container1.setLayout(v_layout)
        container1.setFixedWidth(200)

        layout_first.addWidget(container1)
        layout_first.addWidget(absalut_graph)
        container_first = QWidget()
        container_first.setLayout(layout_first)
        container_graph = QWidget()
        container_graph.setLayout(graph_layout)

        main_layout = QVBoxLayout()
        main_layout.addWidget(container_first)
        main_layout.addWidget(container_graph)

        central_widget.setLayout(main_layout)

    def get_area(self):
        return self.red_area


if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_window = MainWindow()
    main_window.showMaximized()
    sys.exit(app.exec_())
