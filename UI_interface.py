from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

import sys
import cv2
import numpy as np
import os
from Image_Operations import Image_Operations

class UI_Interface(QMainWindow, Image_Operations):
    """
    @brief Main UI class for the interface, inheriting from QMainWindow and Image_Operations.
    """
    def __init__(self):
        """
        @brief Constructor for the UI_Interface class. Initializes the UI and sets up signal-slot connections.
        """
        super().__init__()
        uic.loadUi('UI_Interface_design.ui', self)
        self.show()

        ###################### Side Bar #############################

        self.full_menu_widget.setVisible(False)
        self.side_menu_buttons = [self.source_side, self.output_side, self.conversion_side, self.segmentation_side, self.edge_detection_side]
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
        self.exit_button.clicked.connect(self.exit_app)
        self.exit_menu.triggered.connect(self.exit_app)

        self.menu_buttons = [
            self.source_folder_menu, self.source_export_menu, self.source_clear_menu, 
            self.output_save_menu, self.output_save_as_menu, self.output_export_menu, self.output_clear_menu, self.output_undo_menu, self.output_redo_menu
        ]

        # Always display buttons
        self.always_display_buttons = [
            self.source_folder_menu, self.exit_menu, self.exit_button, self.source_side,
            self.findChild(QtWidgets.QPushButton, "source_open"), self.source_folder_menu, self.menuFile
        ]

        # Disable the buttons
        self.change_buttons_state(False)

    ###################### UI Operations ######################

    def get_buttons(self):
        """
        @brief Retrieves all buttons in the UI.
        @return List of QPushButton and QMenu objects.
        """
        buttons = []

        for button in self.findChildren(QtWidgets.QPushButton):
            buttons.append(button)
        for button in self.findChildren(QtWidgets.QMenu):
            buttons.append(button)

        buttons.append(self.output_save_menu)
        buttons.append(self.output_save_as_menu)

        return buttons

    ###################### Side Bar #############################

    def sidebar_button_clicked(self):
        """
        @brief Slot function called when a sidebar button is clicked. Toggles the visibility of the full menu widget.
        """
        sender = self.sender()

        if not hasattr(self, 'hold_sender') or self.hold_sender != sender or not self.full_menu_widget.isVisible():
            self.full_menu_widget.setVisible(True)
        else:
            self.full_menu_widget.setVisible(False)

        self.edit_full_menu_buttons(sender)
        
        self.hold_sender = sender

    def init_buttons(self):
        """
        @brief Initializes the buttons in the sidebar and connects them to their respective functions.
        """
        button_names = [["Open", "Export", "Clear"],
                        ["Save", "Save As", "Export", "Undo", "Redo", "Clear"],
                        ['Gray', 'HSV'], 
                        ['Multi Otsu', 'Chan Vese', 'Morph Snakes'],
                        ['Roberts', 'Sobel', 'Scharr', 'Prewitt']]
        
        button_object_names = [["source_open", "source_export", "source_clear"],
                                 ["output_save", "output_save_as", "output_export", "output_undo", "output_redo", "output_clear"],
                                 ['bgr_2_gray', 'bgr_2_hsv'], 
                                 ['segment_multi_otsu', 'segment_chan_vese', 'segment_moprh_snakes'],
                                 ['edge_roberts', 'edge_sobel', 'edge_scharr', 'edge_prewitt']]
        
        button_icons = [["src/icons/open.svg", "src/icons/export.svg", "src/icons/clear.svg"],
                        ["src/icons/save.svg", "src/icons/save_as.svg", "src/icons/export.svg", "src/icons/undo.svg", "src/icons/redo.svg", "src/icons/clear.svg"],
                        ["src/icons/conversion.svg", "src/icons/conversion.svg"], 
                        ["src/icons/segmentation.svg", "src/icons/segmentation.svg", "src/icons/segmentation.svg"],
                        ["src/icons/edge_detection.svg", "src/icons/edge_detection.svg", "src/icons/edge_detection.svg", "src/icons/edge_detection.svg"]]
        
        button_functions = [[self.load_image_button, self.export_source_image, self.image_edit_operations],
                            [self.save_output_image, self.save_as_output_image, self.export_output_image, self.image_edit_operations, self.image_edit_operations, self.image_edit_operations],
                            [self.conversion_handler, self.conversion_handler],
                            [self.segmentation_handler, self.segmentation_handler, self.segmentation_handler],
                            [self.edge_detection_handler, self.edge_detection_handler, self.edge_detection_handler, self.edge_detection_handler]] 

        for i, (button_name, button_object_name, button_icon, button_functions) in enumerate(zip(button_names, button_object_names, button_icons, button_functions)):
            for j, (name, object_name, icon, function) in enumerate(zip(button_name, button_object_name, button_icon, button_functions)):
                
                button = QtWidgets.QPushButton(name)
                
                button.setObjectName(object_name)
                
                button.setIcon(QtGui.QIcon(icon))

                button.clicked.connect(function)
                
                self.toolbox_layout.addWidget(button)

                # Connect Menu buttons
                menu_button = self.findChild(QtWidgets.QAction, object_name + "_menu")
                if menu_button:
                    menu_button.triggered.connect(function)

    def edit_full_menu_buttons(self, sender):
        """
        @brief Edits the buttons displayed in the full menu based on the sidebar button clicked.
        @param sender The button that was clicked.
        """
        # Hide all the buttons
        for i in reversed(range(self.toolbox_layout.count())):
            self.toolbox_layout.itemAt(i).widget().setVisible(False)
        
        if sender == self.source_side:
            # Buttons to show
            button_object_names = ["source_open", "source_export", "source_clear"]
            
            # Show buttons to the container
            for i, button_name in enumerate(button_object_names):
                self.toolbox_layout.itemAt(
                    self.toolbox_layout.indexOf(self.findChild(QtWidgets.QPushButton, button_name))
                ).widget().setVisible(True)

        elif sender == self.output_side:
            # Buttons to show
            button_object_names = ["output_save", "output_save_as", "output_export", "output_undo", "output_redo", "output_clear"]
            
            # Show buttons to the container
            for i, button_name in enumerate(button_object_names):
                self.toolbox_layout.itemAt(
                    self.toolbox_layout.indexOf(self.findChild(QtWidgets.QPushButton, button_name))
                ).widget().setVisible(True)

        elif sender == self.conversion_side:
            # Buttons to show
            button_object_names = ["bgr_2_gray", "bgr_2_hsv"]
            
            # Show buttons to the container
            for i, button_name in enumerate(button_object_names):
                self.toolbox_layout.itemAt(
                    self.toolbox_layout.indexOf(self.findChild(QtWidgets.QPushButton, button_name))
                ).widget().setVisible(True)

        elif sender == self.segmentation_side:
            # Buttons to show
            button_object_names = ["segment_multi_otsu", "segment_chan_vese", "segment_moprh_snakes"]
            
            # Show buttons to the container
            for i, button_name in enumerate(button_object_names):
                self.toolbox_layout.itemAt(
                    self.toolbox_layout.indexOf(self.findChild(QtWidgets.QPushButton, button_name))
                ).widget().setVisible(True)

        elif sender == self.edge_detection_side:
            # Buttons to show
            button_object_names = ["edge_roberts", "edge_sobel", "edge_scharr", "edge_prewitt"]
            
            # Show buttons to the container
            for i, button_name in enumerate(button_object_names):
                self.toolbox_layout.itemAt(
                    self.toolbox_layout.indexOf(self.findChild(QtWidgets.QPushButton, button_name))
                ).widget().setVisible(True)

    ###################### File Operations ######################

    def load_image_button(self):
        """
        @brief Opens a file dialog to load an image and sets it as the source image.
        """
        # Get the image path
        image_path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', 'c:\\', "Image files (*.jpg *.png)")[0]
        
        # If the image path is not empty, set the source image
        if image_path:
            self.set_source_image(image_path)            
            self.update_source_image()

            # Assign the source image path
            self.source_image_path = image_path

            # Enable the buttons
            self.change_buttons_state(True)

    def save_output_image(self):
        """
        @brief Saves the output image to the source image path.
        """
        if self.source_image_path:
            self.get_output_image().save_image(self.source_image_path)

    def save_as_output_image(self):
        """
        @brief Opens a file dialog to save the output image with a new name.
        """
        while True:
            # Get the folder path
            image_save_path = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', "output.jpg", "Image files (*.jpg)")[0]

            if not image_save_path:
                break

            # If the folder path is not empty, save the output image, check extension is jpg
            if image_save_path.endswith('.jpg'):
                self.get_output_image().save_image(image_save_path)
                break
            else:
                print("Please select a valid path with .jpg extension")

    def export_output_image(self):
        """
        @brief Opens a file dialog to export the output image in different formats.
        """
        while True:
            # Custom extension choice (jpg, png, bmp)
            image_save_path = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', "output.jpg", "Image files (*.jpg *.png *.bmp)")[0]
            
            if not image_save_path:
                break

            # If the folder path is not empty, save the output image, check extension is jpg or png or bmp
            if (image_save_path.endswith('.jpg') or image_save_path.endswith('.png') or image_save_path.endswith('.bmp')):
                self.get_output_image().save_image(image_save_path)
                break
            else:
                print("Please select a valid path with .jpg or .png or .bmp extension : ", image_save_path)

    def export_source_image(self):
        """
        @brief Opens a file dialog to export the source image in different formats.
        """
        while True:
            # Custom extension choice (jpg, png, bmp)
            image_save_path = QtWidgets.QFileDialog.getSaveFileName(self, 'Save file', "source.jpg", "Image files (*.jpg *.png *.bmp)")[0]
            
            if not image_save_path:
                break

            # If the folder path is not empty, save the output image, check extension is jpg or png or bmp
            if (image_save_path.endswith('.jpg') or image_save_path.endswith('.png') or image_save_path.endswith('.bmp')):
                self.get_source_image().save_image(image_save_path)
                break
            else:
                print("Please select a valid path with .jpg or .png or .bmp extension : ", image_save_path)

    ###################### Image Operations ######################

    def update_source_image(self):
        """
        @brief Updates the source image display in the UI.
        """
        label_size = (self.source_image_frame.width(), self.source_image_frame.height())

        self.source_image_frame.setPixmap(
            QPixmap.fromImage(
                self.get_source_image().get_QImage()
            ).scaled(label_size[0], label_size[1])
        )
        self.source_image_frame.setAlignment(Qt.AlignCenter)
    
    def update_output_image(self):
        """
        @brief Updates the output image display in the UI.
        """
        label_size = (self.output_image_frame.width(), self.output_image_frame.height())
        try:
            self.output_image_frame.setPixmap(
                QPixmap.fromImage(
                    self.get_output_image().get_QImage()
                ).scaled(label_size[0], label_size[1])
            )
            self.output_image_frame.setAlignment(Qt.AlignCenter)
        except:
            if len(self.get_output_image().get_nd_image().shape) < 2:
                # it means img is numpy array that comes from segmentation
                self.output_image_frame.setPixmap(
                    QPixmap.fromImage(
                        self.get_output_image().get_nd_image()
                    ).scaled(label_size[0], label_size[1])
                )
                self.output_image_frame.setAlignment(Qt.AlignCenter)
            else:
                print("Error in update_output_image, image shape: ", self.get_output_image().get_nd_image().shape)

    def conversion_handler(self):
        """
        @brief Handles image conversion operations.
        """
        sender = self.sender()
        img = self.conversion_actions(method=sender.objectName())
        self.set_output_image(img)
        self.update_output_image()

    def segmentation_handler(self):
        """
        @brief Handles image segmentation operations.
        """
        sender = self.sender()
        img = self.segment_image(method=sender.objectName())
        self.set_output_image(img)
        self.update_output_image()

    def edge_detection_handler(self):
        """
        @brief Handles image edge detection operations.
        """
        sender = self.sender()
        img = self.edge_detection_actions(method=sender.objectName())
        self.set_output_image(img)
        self.update_output_image()

    ###################### Common Operations #####################

    def exit_app(self):
        """
        @brief Exits the application.
        """
        sys.exit()
       
    def change_buttons_state(self, visible=True):
        """
        @brief Changes the enabled state of buttons.
        @param visible Boolean to enable or disable buttons.
        """
        for button in self.get_buttons():
            if button in self.always_display_buttons:
                continue
            button.setDisabled( not visible)

    def image_edit_operations(self):
        """
        @brief Handles common image edit operations such as undo, redo, and clear.
        """
        sender = self.sender()
        object_name = sender.objectName().replace('_menu', '')

        # Undo - Redo operations
        if object_name == "output_undo":
            self.undo_output_image()
            self.update_output_image()

        elif object_name == "output_redo":
            self.redo_output_image()
            self.update_output_image()
        
        elif object_name == "source_clear":
            self.set_source_image(None)
            self.source_image_path = None
            self.change_buttons_state(False)
            self.source_image_frame.clear()

        elif object_name == "output_clear":
            self.output_image_history = {"image_history":[], "current_index":0}
            self.output_image_frame.clear()

if __name__ == '__main__':
    """
    @brief Main entry point of the application. Creates an instance of UI_Interface and runs the application.
    """
    print("Testing UI_Interface class")

    app = QtWidgets.QApplication(sys.argv)
    window = UI_Interface()
    sys.exit(app.exec_())
