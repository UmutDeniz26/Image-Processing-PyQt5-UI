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
        self.bgr_2_hsv.clicked.connect(self.convert_to_hsv)
        
        # Connect menu items
        self.source_folder_menu.triggered.connect(self.source_folder.click)
        self.output_save_menu.triggered.connect(self.output_save.click)
        self.output_save_as_menu.triggered.connect(self.output_save_as.click)
        self.exit_menu.triggered.connect(self.exit_app)
        self.source_clear_menu.triggered.connect(self.clear_source_image)


        # Button lists
        self.all_buttons = [
            self.source_folder, self.source_folder_menu, self.source_export_menu, self.source_clear_menu
            ,self.output_save, self.output_save_as,self.output_undo_menu,self.output_save_menu, self.output_save_as_menu, self.output_export_menu,self.output_clear_menu,self.output_redo_menu
            ,self.bgr_2_gray, self.bgr_2_hsv
            ,self.exit_menu
        ]

        # Tools buttons
        self.tools_buttons = [
           self.source_folder, self.output_save, self.bgr_2_gray, self.bgr_2_hsv
        ]

        # Always display buttons
        self.always_display_buttons = [
            self.source_folder,self.source_folder_menu, self.exit_menu
        ]

        # Disable the buttons
        self.change_button_state(self.all_buttons, False)












    #############################################################

    ###################### File Operations ######################

    def load_image_button(self):
        
        # Get the image path
        image_path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Image files (*.jpg *.png)")[0]
        
        # If the image path is not empty, set the source image
        if image_path:
            # Name of the label of the source image is sourceImage
            self.image_operator.set_source_image(image_path)            
            self.update_source_image(label_size=(self.source_image.width(), self.source_image.height()))

            # Assign the source image path
            self.source_image_path = image_path

            # Enable the buttons
            self.change_button_state(self.all_buttons, True)
    
    def save_output_image(self):
        # If the folder path is not empty, save the output image
        if self.source_image_path:
            self.image_operator.get_output_image().save_image(self.source_image_path)

    def save_as_output_image(self):
        # Get the folder path
        image_save_path = QtWidgets.QFileDialog.getSaveFileName(
            self, 'Save file', "output.jpg", "Image files (*.jpg *.png)")[0]

        # If the folder path is not empty, save the output image
        if image_save_path:
            self.image_operator.get_output_image().save_image(image_save_path)













    ##############################################################

    ###################### Image Operations ######################

    # Function to update the source image
    def update_source_image(self, label_size=(400, 400)):
        self.source_image.setPixmap(
            QPixmap.fromImage(
                self.image_operator.get_source_image().get_QImage()
            ).scaled(label_size[0], label_size[1])
        )
        self.source_image.setAlignment(Qt.AlignCenter)
    
    # Function to update the output image
    def update_output_image(self, label_size=(400, 400)):
        self.output_image.setPixmap(
            QPixmap.fromImage(
                self.image_operator.get_output_image().get_QImage()
            ).scaled(label_size[0], label_size[1])
        )
        self.output_image.setAlignment(Qt.AlignCenter)

    def convert_to_gray(self):
        self.image_operator.convesion_actions(method='gray')
        self.update_output_image(label_size=(self.output_image.width(), self.output_image.height()))

    def convert_to_hsv(self):
        self.image_operator.convesion_actions(method='hsv')
        self.update_output_image(label_size=(self.output_image.width(), self.output_image.height()))

    def clear_source_image(self):
        self.image_operator.set_source_image(None)
        self.source_image_path = None
        self.change_button_state(self.all_buttons, False)
        self.source_image.clear()











    ##############################################################

    ###################### Common Operations #####################

    def exit_app(self):
        sys.exit()
       
    def change_button_state(self, button, state):
        for button in self.all_buttons:
            if button not in self.always_display_buttons:
                button.setDisabled(False) if state else button.setDisabled(True)


if __name__ == '__main__':
    print("Testing PyqtUI class")

    app = QtWidgets.QApplication(sys.argv)
    window = PyqtUI()
    sys.exit(app.exec_())
