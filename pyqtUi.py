
# Read PyqtUI.ui file and show the window
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

import sys
import cv2
import numpy as np

import image_operator

class PyqtUI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('pyqtUI_design.ui', self)
        self.show()

        self.image_operator = image_operator.image_operator()
        
        # Connect the buttons
        self.sourceFolder.clicked.connect(self.load_image)

    def load_image(self):
        
        print("Loading image...")

        image_path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Image files (*.jpg *.png)")[0]

        if image_path:
            print("Image path: ", image_path)
            self.image_operator.set_source_image(image_path)
            self.image_operator.show_output_image()

        """
        if image_path:
            image = cv2.imread(image_path)
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = cv2.resize(image, (self.label.width(), self.label.height()))
            qimage = QPixmap.fromImage(QImage(image.data, image.shape[1], image.shape[0], image.strides[0], QImage.Format_RGB888))
            self.label.setPixmap(qimage)
            self.label.setAlignment(Qt.AlignCenter)
        """
    

if __name__ == '__main__':
    print("Testing PyqtUI class:")

    app = QtWidgets.QApplication(sys.argv)
    window = PyqtUI()
    sys.exit(app.exec_())