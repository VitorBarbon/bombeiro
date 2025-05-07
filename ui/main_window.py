from PySide6.QtWidgets import QMainWindow, QLabel

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sistema de Gestão")
        self.setMinimumSize(600, 400)  
        self.resize(800, 600)          

        label = QLabel("Bem-vindo ao sistema!", self)
        label.move(300, 280)
        label.adjustSize()