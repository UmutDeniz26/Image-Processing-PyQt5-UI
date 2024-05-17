
# Read PyqtUI.ui file and show the window
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt

import sys
import cv2
import numpy as np

import Image_Operations

class PyqtUI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('pyqtUI_design.ui', self)
        self.show()

        self.image_operator = Image_Operations.Image_Operations()
        
        # Connect the buttons
        self.sourceFolder.clicked.connect(self.load_image)

    def update_source_image(self, label_size = (400, 400) ):
        """
        Function to update the source image in the UI
        
        Arguments:
            label_size: tuple, (int, int) - The size of the label to display the image
        Returns:
            None
        """

        self.sourceImage.setPixmap(
            QPixmap.fromImage(
                self.image_operator.get_source_image().get_QImage()
            ).scaled(label_size[0], label_size[1])
        )
        self.sourceImage.setAlignment(Qt.AlignCenter)
    
    def update_output_image(self, label_size = (400, 400) ):
        self.outputImage.setPixmap(
            QPixmap.fromImage(
                self.image_operator.get_output_image().get_QImage()
            ).scaled(label_size[0], label_size[1])
        )
        self.outputImage.setAlignment(Qt.AlignCenter)

    def load_image(self):
        
        # Get the image path
        image_path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Image files (*.jpg *.png)")[0]
        
        # If the image path is not empty, set the source image
        if image_path:
            self.image_operator.set_source_image(image_path)            

            # Name of the label of the source image is sourceImage
            self.update_source_image( label_size = ( self.sourceImage.width(), self.sourceImage.height() ) )
    

if __name__ == '__main__':
    print("Testing PyqtUI class:")

    app = QtWidgets.QApplication(sys.argv)
    window = PyqtUI()
    sys.exit(app.exec_())