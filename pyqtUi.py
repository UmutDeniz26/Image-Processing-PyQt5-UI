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
        self.source_folder.clicked.connect(self.load_image_button)
        self.output_save.clicked.connect(self.save_output_image)
        self.output_save_as.clicked.connect(self.save_as_output_image)
        self.bgr_2_gray.clicked.connect(self.convert_to_gray)
        self.multi_otsu.clicked.connect(self.segment_multi_otsu)
        
        # Connect menu items
        self.source_folder_menu.triggered.connect(self.source_folder.click)
        self.output_save_menu.triggered.connect(self.output_save.click)
        self.output_save_as_menu.triggered.connect(self.output_save_as.click)
        self.exit_menu.triggered.connect(self.exit_app)

        # Button lists
        self.menu_buttons = [
            self.source_folder_menu, self.exit_menu,
            self.output_save_menu, self.output_save_as_menu, self.output_export_menu, self.source_export_menu,
            self.source_clear_menu, self.output_clear_menu, self.output_undo_menu, self.output_redo_menu,
        ]

        # Tools buttons
        self.tools_buttons = [
           self.source_folder, self.output_save, self.bgr_2_gray
        ]

        # Always display buttons
        self.always_display_buttons = [
            self.source_folder_menu, self.exit_menu
        ]

        # Disable the buttons
        self.disable_buttons()
        


    def display_buttons(self):
        """
        Function to display the buttons in the UI
        
        Arguments:
            None
        Returns:
            None
        """
        for button in self.menu_buttons:
            if button not in self.always_display_buttons:
                button.setDisabled(False)

    def disable_buttons(self):
        """
        Function to disable the buttons in the UI
        
        Arguments:
            None
        Returns:
            None
        """
        for button in self.menu_buttons:
            if button not in self.always_display_buttons:
                button.setDisabled(True)


    def update_source_image(self, label_size=(400, 400)):
        """
        Function to update the source image in the UI
        
        Arguments:
            label_size: tuple, (int, int) - The size of the label to display the image
        Returns:
            None
        """

        self.source_image.setPixmap(
            QPixmap.fromImage(
                self.image_operator.get_source_image().get_QImage()
            ).scaled(label_size[0], label_size[1])
        )
        self.source_image.setAlignment(Qt.AlignCenter)
    
    def update_output_image(self, label_size=(400, 400)):
        """
        Function to update the output image in the UI

        Arguments:
            label_size: tuple, (int, int) - The size of the label to display the image

        Returns:
            None
        """ 
        self.output_image.setPixmap(
            QPixmap.fromImage(
                self.image_operator.get_output_image().get_QImage()
            ).scaled(label_size[0], label_size[1])
        )
        self.output_image.setAlignment(Qt.AlignCenter)

    def load_image_button(self):
        
        # Get the image path
        image_path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Image files (*.jpg *.png)")[0]
        
        # If the image path is not empty, set the source image
        if image_path:
            self.image_operator.set_source_image(image_path)            

            # Name of the label of the source image is sourceImage
            self.update_source_image(label_size=(self.source_image.width(), self.source_image.height()))

            # Assign the source image path
            self.source_image_path = image_path

            # Enable the buttons
            self.display_buttons()
    
    def save_output_image(self):

        # Get the folder path
        #folder_path = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select folder')

        # If the folder path is not empty, save the output image
        if self.source_image_path:
            self.image_operator.get_output_image().save_image(self.source_image_path)

    def save_as_output_image(self):
        # Get the folder path
        image_path = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', "output.jpg", "Image files (*.jpg *.png)"
        )[0]

        # If the folder path is not empty, save the output image
        if image_path:
            self.image_operator.get_output_image().save_image(image_path)

    def exit_app(self):
        sys.exit()


    def convert_to_gray(self):
        self.image_operator.convert_to_gray()
        self.update_output_image(label_size=(self.output_image.width(), self.output_image.height()))

    def segment_multi_otsu(self):
        self.image_operator.segment_image(method='multi_otsu')

        self.image_operator.set_output_image(self.image_operator.get_output_image().get_nd_image().astype(np.uint8))
        
        self.update_output_image(label_size=(self.output_image.width(), self.output_image.height()))


if __name__ == '__main__':
    print("Testing PyqtUI class")

    app = QtWidgets.QApplication(sys.argv)
    window = PyqtUI()
    sys.exit(app.exec_())
