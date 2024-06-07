# Read PyqtUI.ui file and show the window
from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

import sys
import cv2
import numpy as np
import os
import Image_Operations

class PyqtUI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi('pyqtUI_design.ui', self)
        self.show()

        self.image_operator = Image_Operations.Image_Operations()
        
        ###################### Side Bar #############################

        self.full_menu_widget.setVisible(False)
        self.side_menu_buttons = [ self.source_side, self.output_side, self.conversion_side, self.segmentation_side, self.edge_detection_side ]
        for button in self.side_menu_buttons:
            button.clicked.connect(self.sidebar_button_clicked)
        
        self.init_buttons()
        

        ###################### MENU OPERATIONS ######################

        ###################### File Operations ######################
    
        # Source operations
        self.source_folder_menu.triggered.connect(self.load_image_button)
        self.source_export_menu.triggered.connect(self.export_source_image)

        # Output operations
        self.output_save_menu.triggered.connect(self.save_output_image)
        self.output_save_as_menu.triggered.connect(self.save_as_output_image)
        self.output_export_menu.triggered.connect(self.export_output_image)
        
        
        ###################### Common Operations #####################
        self.output_undo_menu.triggered.connect(self.undo_output_image)
        self.output_redo_menu.triggered.connect(self.redo_output_image)
                        
        
        # Button lists
        self.all_buttons = [
            self.source_folder_menu, self.source_export_menu, self.source_clear_menu,
                    
            self.output_undo_menu,self.output_save_menu, self.output_save_as_menu, self.output_export_menu,self.output_clear_menu,self.output_redo_menu

            ,self.exit_menu
        ]

        self.menu_buttons = [
            self.source_folder_menu, self.source_export_menu, self.source_clear_menu, 
            self.output_save_menu, self.output_save_as_menu, self.output_export_menu, self.output_clear_menu, self.output_undo_menu, self.output_redo_menu
        ]


        # Always display buttons
        self.always_display_buttons = [
            self.source_folder_menu, self.exit_menu
        ]

        # Disable the buttons
        self.change_button_state(self.all_buttons, False)



    def admin_print(self):
        print("Histories. \nSource")
        print(self.image_operator.source_image_history)

        print("Output")
        print(self.image_operator.output_image_history)



    ###################### Side Bar #############################
    
    def sidebar_button_clicked(self):
        sender = self.sender()

        if not hasattr(self, 'hold_sender') or self.hold_sender != sender or not self.full_menu_widget.isVisible():
            self.full_menu_widget.setVisible(True)
        else:
            self.full_menu_widget.setVisible(False)

        self.edit_full_menu_buttons(sender)    
        
        self.hold_sender = sender

    def init_buttons(self):
        button_names = [["Open", "Save", "Export", "Undo", "Redo", "Clear"],
                        ["Save", "Save As", "Export", "Undo", "Redo", "Clear"],
                        ['Gray', 'HSV'], 
                        ['Multi Otsu', 'Chan Vese', 'Morph Snakes'],
                        ['Roberts', 'Sobel', 'Scharr', 'Prewitt']]
        
        button_object_names = [["source_open", "source_save", "source_export", "source_undo", "source_redo", "source_clear"],
                                 ["output_save", "output_save_as", "output_export", "output_undo", "output_redo", "output_clear"],
                                 ['bgr_2_gray', 'bgr_2_hsv'], 
                                 ['segment_multi_otsu', 'segment_chan_vese', 'segment_moprh_snakes'],
                                 ['edge_roberts', 'edge_sobel', 'edge_scharr', 'edge_prewitt']]
        
        button_icons = [["src/icons/open.svg", "src/icons/save.svg", "src/icons/export.svg", "src/icons/undo.svg", "src/icons/redo.svg", "src/icons/clear.svg"],
                        ["src/icons/save.svg", "src/icons/save_as.svg", "src/icons/export.svg", "src/icons/undo.svg", "src/icons/redo.svg", "src/icons/clear.svg"],
                        ["src/icons/conversion.svg", "src/icons/conversion.svg"], 
                        ["src/icons/segmentation.svg", "src/icons/segmentation.svg", "src/icons/segmentation.svg"],
                        ["src/icons/edge_detection.svg", "src/icons/edge_detection.svg", "src/icons/edge_detection.svg", "src/icons/edge_detection.svg"]]
        
        button_functions = [[self.load_image_button, lambda:print(), self.export_source_image, lambda:print(), lambda:print(), self.clear_source_image],
                            [self.save_output_image, self.save_as_output_image, self.export_output_image, self.undo_output_image, self.redo_output_image, self.clear_output_image],
                            [self.convert_to_gray, self.convert_to_hsv], 
                            [self.segment_multi_otsu_f, self.segment_chan_vese_f, self.segment_moprh_snakes_f],
                            [self.edge_roberts_f, self.edge_sobel_f, self.edge_scharr_f, self.edge_prewitt_f]] 
                             

        
        for i, (button_name, button_object_name, button_icon, button_functions) in enumerate(zip(button_names, button_object_names, button_icons, button_functions)):
            for j, (name, object_name, icon, function) in enumerate(zip(button_name, button_object_name, button_icon,button_functions)):
                button = QtWidgets.QPushButton(name)
                button.setObjectName(object_name)
                button.setIcon(QtGui.QIcon(icon))
                button.clicked.connect(function)
                self.toolbox_layout.addWidget(button)

    def edit_full_menu_buttons(self, sender):
        # Hide all the buttons not
        for i in reversed(range(self.toolbox_layout.count())):
            self.toolbox_layout.itemAt(i).widget().setVisible(False)
        
        if sender == self.source_side:
            # Buttons to show
            button_object_names = ["source_open", "source_save", "source_export", "source_undo", "source_redo", "source_clear"]
            
            # Show buttons to the container
            for i,button_name in enumerate(button_object_names):
                self.toolbox_layout.itemAt(
                    self.toolbox_layout.indexOf(self.findChild(QtWidgets.QPushButton, button_name))
                ).widget().setVisible(True)

        elif sender == self.output_side:
            # Buttons to show
            button_object_names = ["output_save", "output_save_as", "output_export", "output_undo", "output_redo", "output_clear"]
            
            # Show buttons to the container
            for i,button_name in enumerate(button_object_names):
                self.toolbox_layout.itemAt(
                    self.toolbox_layout.indexOf(self.findChild(QtWidgets.QPushButton, button_name))
                ).widget().setVisible(True)

        elif sender == self.conversion_side:
            # Buttons to show
            button_object_names = ["bgr_2_gray", "bgr_2_hsv"]
            
            # Show buttons to the container
            for i,button_name in enumerate(button_object_names):
                self.toolbox_layout.itemAt(
                    self.toolbox_layout.indexOf(self.findChild(QtWidgets.QPushButton, button_name))
                ).widget().setVisible(True)

        elif sender == self.segmentation_side:
            # Buttons to show
            button_object_names = ["segment_multi_otsu", "segment_chan_vese", "segment_moprh_snakes"]
            
            # Show buttons to the container
            for i,button_name in enumerate(button_object_names):
                self.toolbox_layout.itemAt(
                    self.toolbox_layout.indexOf(self.findChild(QtWidgets.QPushButton, button_name))
                ).widget().setVisible(True)

        elif sender == self.edge_detection_side:
            # Buttons to show
            button_object_names = ["edge_roberts", "edge_sobel", "edge_scharr", "edge_prewitt"]
            
            # Show buttons to the container
            for i,button_name in enumerate(button_object_names):
                self.toolbox_layout.itemAt(
                    self.toolbox_layout.indexOf(self.findChild(QtWidgets.QPushButton, button_name))
                ).widget().setVisible(True)
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

        while True:
            # Get the folder path
            image_save_path = QtWidgets.QFileDialog.getSaveFileName(
                self, 'Save file', "output.jpg", "Image files (*.jpg)")[0]

            if not image_save_path:
                break

            # If the folder path is not empty, save the output image, check extension is jpg
            if image_save_path.endswith('.jpg'):
                self.image_operator.get_output_image().save_image(image_save_path)
                break
            else:
                print("Please select a valid path with .jpg extension")

    def export_output_image(self):
        while True:
            # Custom extension choice (jpg, png, bmp)
            image_save_path = QtWidgets.QFileDialog.getSaveFileName(
                self, 'Save file', "output.jpg", "Image files (*.jpg *.png *.bmp)")[0]
            
            if not image_save_path:
                break

            # If the folder path is not empty, save the output image, check extension is jpg or png or bmp
            if (image_save_path.endswith('.jpg') or image_save_path.endswith('.png') or image_save_path.endswith('.bmp')):
                self.image_operator.get_output_image().save_image(image_save_path)
                break
            else:
                print("Please select a valid path with .jpg or .png or .bmp extension : ", image_save_path)



    def export_source_image(self):
        while True:
            # Custom extension choice (jpg, png, bmp)
            image_save_path = QtWidgets.QFileDialog.getSaveFileName(
                self, 'Save file', "source.jpg", "Image files (*.jpg *.png *.bmp)")[0]
            
            # If the folder path is not empty, save the output image
            if not image_save_path:
                break

            # If the folder path is not empty, save the output image, check extension is jpg or png or bmp
            if (image_save_path.endswith('.jpg') or image_save_path.endswith('.png') or image_save_path.endswith('.bmp')):
                self.image_operator.get_source_image().save_image(image_save_path)
                break
            else:
                print("Please select a valid path with .jpg or .png or .bmp extension : ", image_save_path)













    ##############################################################

    ###################### Image Operations ######################


    # Display functions
    def update_source_image(self, label_size=(400, 400)):
        self.source_image.setPixmap(
            QPixmap.fromImage(
                self.image_operator.get_source_image().get_QImage()
            ).scaled(label_size[0], label_size[1])
        )
        self.source_image.setAlignment(Qt.AlignCenter)
    
    def update_output_image(self, label_size=(400, 400)):
        try:
            self.output_image.setPixmap(
                QPixmap.fromImage(
                    self.image_operator.get_output_image().get_QImage()
                ).scaled(label_size[0], label_size[1])
            )
            self.output_image.setAlignment(Qt.AlignCenter)
        except:
            if len (self.image_operator.get_output_image().get_nd_image().shape) < 2:
                # it means img is numpy array that comes from segmentation
                self.output_image.setPixmap(
                    QPixmap.fromImage(
                        self.image_operator.get_output_image().get_nd_image()
                    ).scaled(label_size[0], label_size[1])
                )
                self.output_image.setAlignment(Qt.AlignCenter)
            else:
                print("Error in update_output_image, image shape: ", self.image_operator.get_output_image().get_nd_image().shape)
            

    # Conversion functions
    def convert_to_gray(self):
        img = self.image_operator.convesion_actions(method='gray')
        self.image_operator.set_output_image(img)
        self.update_output_image(label_size=(self.output_image.width(), self.output_image.height()))

    def convert_to_hsv(self):
        img = self.image_operator.convesion_actions(method='hsv')
        self.image_operator.set_output_image(img)
        self.update_output_image(label_size=(self.output_image.width(), self.output_image.height()))


    # Clear functions
    def clear_source_image(self):
        
        self.image_operator.set_source_image(None);self.source_image_path = None
        self.image_operator.source_image_history = {"image_history":[], "current_index":-1}

        self.change_button_state(self.all_buttons, False)
        self.source_image.clear()

    def clear_output_image(self):
        self.image_operator.output_image_history = {"image_history":[], "current_index":-1}
        self.output_image.clear()


    # Segmentation functions
    def segment_multi_otsu_f(self):
        img = self.image_operator.segment_image(method='multi_otsu')
        self.image_operator.set_output_image(img)
        self.update_output_image(label_size=(self.output_image.width(), self.output_image.height()))

    def segment_chan_vese_f(self):
        img = self.image_operator.segment_image(method='chan_vese')
        self.image_operator.set_output_image(img)
        self.update_output_image(label_size=(self.output_image.width(), self.output_image.height()))

    def segment_moprh_snakes_f(self):
        img = self.image_operator.segment_image(method='morph_snakes')
        self.image_operator.set_output_image(img)
        self.update_output_image(label_size=(self.output_image.width(), self.output_image.height()))


    # Edge detection functions
    def edge_roberts_f(self):
        img = self.image_operator.edge_detection_actions(method='roberts')
        self.image_operator.set_output_image(img)
        self.update_output_image(label_size=(self.output_image.width(), self.output_image.height()))

    def edge_sobel_f(self):
        img = self.image_operator.edge_detection_actions(method='sobel')
        self.image_operator.set_output_image(img)
        self.update_output_image(label_size=(self.output_image.width(), self.output_image.height()))

    def edge_scharr_f(self):
        img = self.image_operator.edge_detection_actions(method='scharr')
        self.image_operator.set_output_image(img)
        self.update_output_image(label_size=(self.output_image.width(), self.output_image.height()))

    def edge_prewitt_f(self):
        img = self.image_operator.edge_detection_actions(method='prewitt')
        self.image_operator.set_output_image(img)
        self.update_output_image(label_size=(self.output_image.width(), self.output_image.height()))






    ##############################################################

    ###################### Common Operations #####################

    def exit_app(self):
        sys.exit()
       
    def change_button_state(self, button, state):
        for button in self.all_buttons:
            if button not in self.always_display_buttons:
                button.setDisabled(False) if state else button.setDisabled(True)

    def undo_output_image(self):
        self.image_operator.undo_output_image()
        self.update_output_image(label_size=(self.output_image.width(), self.output_image.height()))

    def redo_output_image(self):
        self.image_operator.redo_output_image()
        self.update_output_image(label_size=(self.output_image.width(), self.output_image.height()))


if __name__ == '__main__':
    print("Testing PyqtUI class")

    app = QtWidgets.QApplication(sys.argv)
    window = PyqtUI()
    sys.exit(app.exec_())
