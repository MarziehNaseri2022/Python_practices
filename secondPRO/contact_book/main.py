
from PyQt5.QtWidgets import QApplication
from PyQt5.QtGui import QIcon, QPixmap, QPainter
import sys
from uni.main_window import MainWindow

app = QApplication(sys.argv)
window = MainWindow()

window.show()
sys.exit(app.exec_())

