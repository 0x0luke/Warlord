from PySide2 import QtCore, QtWidgets, QtGui
import sys

class WebAppWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Web App Testing")
        self.resize(1280,720)
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)


class BinaryWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Binary Testing")
        self.resize(1280,720)
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)

class CreditWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Credits")
        self.resize(800,800)
        layout = QtWidgets.QVBoxLayout()
        self.setLayout(layout)


class Window(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.setWindowTitle("Welcome")
        self.resize(270,110)
        self.WebButton = QtWidgets.QPushButton("Web App Testing")
        self.BinaryButton = QtWidgets.QPushButton("Binary Testing")
        self.CreditButton = QtWidgets.QPushButton("Credits")
        
        
        self.layout = QtWidgets.QVBoxLayout()
        self.layout.addWidget(self.WebButton)
        self.layout.addWidget(self.BinaryButton)
        self.layout.addWidget(self.CreditButton)
        self.setLayout(self.layout)

        self.WebButton.clicked.connect(self.web)
        self.BinaryButton.clicked.connect(self.binary)
        self.CreditButton.clicked.connect(self.credit)

    def binary(self):
        self.w = BinaryWindow()
        self.w.show()
        self.hide()

    def web(self):
        self.w = WebAppWindow()
        self.w.show()
        self.hide()

    def credit(self):
        self.w = CreditWindow()
        self.w.show()
        self.hide()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())