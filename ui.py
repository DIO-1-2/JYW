# coding=gbk
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtGui import QPalette, QBrush, QPixmap, QColor
import sys
from PyQt5.QtWidgets import QWidget, QLabel, QLineEdit, QApplication, QPushButton, QTextEdit, QMainWindow
from numpy import double

from IR_code.MLE import MLE_uni, post, dis, MLE_bi
from IR_code.query import out_search


class Search(QWidget):

    def __init__(self):
        super().__init__()
        self.b1 = QPushButton('MLE-unigram', self)  # ���ð�ť
        self.b2 = QPushButton('MLE-bigram', self)
        self.b3 = QPushButton('BM', self)
        self.d = QLineEdit(self)
        self.h = QLineEdit(self)
        self.c = QLabel(self)
        self.b_theme = QLineEdit(self)
        self.b_content = QLineEdit(self)
        self.b_hint = QLabel(self)
        self.a = QLabel(self)
        self.e = QTextEdit(self)
        self.f = QTextEdit(self)
        self.g = QTextEdit(self)
        self.settings()

    def settings(self):
        self.setGeometry(0, 0, 2000, 1000)  # ���ý����С
        self.setWindowTitle('��ѯ')
        palette = QPalette()  # ���ñ���ͼƬ
        pix = QtGui.QPixmap("wd.jpg")
        pix = pix.scaled(self.width(), self.height())
        palette.setBrush(QtGui.QPalette.Background, QtGui.QBrush(pix))
        self.setPalette(palette)

        self.a.setText('������ѯ��')
        self.a.move(50, 150)
        self.a.setStyleSheet("QLabel{background-color: orange}"
                             "QLabel{font-size:25px}"
                             "QLabel{font-family:'����'}")

        self.b_theme.setPlaceholderText('�������ѯ��Ŀ����')  # �����ı���������
        self.b_theme.move(200, 150)
        self.b_theme.resize(300, 50)

        self.b_content.setPlaceholderText('�������ѯ��������')  # �����ı���������
        self.b_content.move(200, 200)
        self.b_content.resize(300, 50)

        '''self.b_hint.setText('��ʾ�������ʽӦΪ X and Y ')
        self.b_hint.move(200, 250)
        self.b_hint.setStyleSheet("QLabel{background-color: orange}"
                             "QLabel{font-size:20px}"
                             "QLabel{font-family:'����'}")'''

        self.c.setText('��Ȼ���Բ�ѯ��')
        self.c.setStyleSheet("QLabel{background-color: orange}"
                             "QLabel{font-size:25px}"
                             "QLabel{font-family:'����'}")
        self.c.move(800, 150)

        self.d.setPlaceholderText('�������ѯ����')
        self.d.move(1000, 150)
        self.d.resize(300, 50)

        self.h.setPlaceholderText('����ƽ������')
        self.h.move(1400, 200)
        self.h.resize(100, 50)

        self.e.move(1150, 300)
        self.e.resize(400, 700)  # BI_MLE������ڴ�С
        self.e.setFontFamily("����")
        self.e.setFontPointSize(10)

        self.f.move(750, 300)
        self.f.resize(400, 700)  # UI_MLE������ڴ�С
        self.f.setFontFamily("����")
        self.f.setFontPointSize(10)

        self.g.move(200, 300)
        self.g.resize(400, 700)  # BM������ڴ�С
        self.g.setFontFamily("����")
        self.g.setFontPointSize(10)

        self.b1.move(1600, 200)  # ����λ�ã�����Ϊ���£�ǰ��Ϊǰ��
        self.b1.resize(170, 50)
        self.b1.setStyleSheet("QPushButton{background-color: lightgreen}"
                              "QPushButton{font-size:25px}"
                              "QPushButton{font-family:Times New Roman}")  # ���ð�ť�ı�����ɫ�������С��������ʽ
        self.b1.clicked.connect(self.Clickedbutton1)

        self.b2.move(1600, 300)
        self.b2.resize(170, 50)
        self.b2.setStyleSheet("QPushButton{background-color: lightblue}"
                              "QPushButton{font-size:25px}"
                              "QPushButton{font-family:Times New Roman}")
        self.b2.clicked.connect(self.Clickedbutton2)

        self.b3.move(550, 150)
        self.b3.resize(170, 50)
        self.b3.setStyleSheet("QPushButton{background-color: lightyellow}"
                              "QPushButton{font-size:25px}"
                              "QPushButton{font-family:Times New Roman}")
        self.b3.clicked.connect(self.Clickedbutton3)
        self.show()

    def Clickedbutton1(self):  # MLE-UNI
        q1 = self.d.text()
        lam = double(self.h.text())
        l1 = MLE_uni(q1, post, lam)
        self.f.setText(dis(l1))

    def Clickedbutton2(self):  # MLE-BI
        q1 = self.d.text()
        r = double(self.h.text())
        l1 = MLE_bi(q1, post, r)
        self.e.setText(dis(l1))

    def Clickedbutton3(self):  # BM
        q1 = self.b_theme.text()
        q2 = self.b_content.text()
        l1 = out_search(q1, q2)
        self.g.setText(l1)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Search()
    sys.exit(app.exec_())
