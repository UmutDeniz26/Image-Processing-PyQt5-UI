from PyQt5 import QtWidgets, uic
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
from PyQt5 import QtGui

import sys
import cv2
import numpy as np
import time
import os
from Image_Operations import Image_Operations

from functools import wraps

# Define the decorator for the progress bar
def progress_bar_decorator(time_delay):
    def decorator(func):
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            # Temporary progress bar generation
            layout = QtWidgets.QVBoxLayout()
            progress_bar = QtWidgets.QProgressBar()
            progress_bar.setRange(0, 100)
            progress_bar.setFixedHeight(15)
            layout.addWidget(progress_bar)
            
            # Add progress bar to the status bar
            self.statusBar().addPermanentWidget(progress_bar)
            
            for i in range(101):
                time.sleep(time_delay / 100)
                progress_bar.setValue(i)
            self.statusBar().removeWidget(progress_bar)
            
            
            return func(self, *args, **kwargs)
        return wrapper
    return decorator


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

        # Disable the buttons
        self.change_buttons_state("default",True)

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

        buttons.append(self.output_save_menu);buttons.append(self.output_save_as_menu)
        buttons.append(self.output_export_menu);buttons.append(self.output_clear_menu)
        buttons.append(self.output_undo_menu);buttons.append(self.output_redo_menu)

        return buttons


    def change_buttons_state(self, state = "default", visible = True):
        """
        @brief Changes the enabled state of buttons.
        @param state The state to set the buttons to. Can be "full", "source_opened" or "default".
        """


        if state == "source_opened":
            edit_buttons = [
                self.output_side, 
                self.output_save_menu, self.output_save_as_menu, self.output_export_menu, 
                self.output_clear_menu, self.output_undo_menu, self.output_redo_menu,
            ]
        elif state == "default":
            edit_buttons = [
                self.source_folder_menu, self.exit_menu, self.exit_button, self.source_side,
                self.findChild(QtWidgets.QPushButton, "source_open"), self.source_folder_menu, self.menuFile
            ]
        elif state == "full":
            edit_buttons = []
            
        for button in self.get_buttons():
            if button in edit_buttons:
                button.setEnabled(visible)
            else:
                button.setEnabled(not visible)

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

        buttons = [
            {"name": "Open", "object_name": "source_open", "icon": "src/icons/open.svg", "function": self.load_image_button},
            {"name": "Export", "object_name": "source_export", "icon": "src/icons/export.svg", "function": self.export_source_image},
            {"name": "Clear", "object_name": "source_clear", "icon": "src/icons/clear.svg", "function": self.image_edit_operations},

            {"name": "Save", "object_name": "output_save", "icon": "src/icons/save.svg", "function": self.save_output_image},
            {"name": "Save As", "object_name": "output_save_as", "icon": "src/icons/save_as.svg", "function": self.save_as_output_image},
            {"name": "Export", "object_name": "output_export", "icon": "src/icons/export.svg", "function": self.export_output_image},
            {"name": "Undo", "object_name": "output_undo", "icon": "src/icons/undo.svg", "function": self.image_edit_operations},
            {"name": "Redo", "object_name": "output_redo", "icon": "src/icons/redo.svg", "function": self.image_edit_operations},
            {"name": "Clear", "object_name": "output_clear", "icon": "src/icons/clear.svg", "function": self.image_edit_operations},

            {"name": "Gray", "object_name": "bgr_2_gray", "icon": "src/icons/conversion.svg", "function": self.conversion_handler},
            {"name": "HSV", "object_name": "bgr_2_hsv", "icon": "src/icons/conversion.svg", "function": self.conversion_handler},

            {"name": "Multi Otsu", "object_name": "segment_multi_otsu", "icon": "src/icons/segmentation.svg", "function": self.segmentation_handler},
            {"name": "Chan Vese", "object_name": "segment_chan_vese", "icon": "src/icons/segmentation.svg", "function": self.segmentation_handler},
            {"name": "Morph Snakes", "object_name": "segment_moprh_snakes", "icon": "src/icons/segmentation.svg", "function": self.segmentation_handler},

            {"name": "Roberts", "object_name": "edge_roberts", "icon": "src/icons/edge_detection.svg", "function": self.edge_detection_handler},
            {"name": "Sobel", "object_name": "edge_sobel", "icon": "src/icons/edge_detection.svg", "function": self.edge_detection_handler},
            {"name": "Scharr", "object_name": "edge_scharr", "icon": "src/icons/edge_detection.svg", "function": self.edge_detection_handler},
            {"name": "Prewitt", "object_name": "edge_prewitt", "icon": "src/icons/edge_detection.svg", "function": self.edge_detection_handler},
        ]
        for button_dict in buttons:

            button = QtWidgets.QPushButton(button_dict['name'])
            button.setObjectName(button_dict['object_name'])
            button.clicked.connect(button_dict['function'])
            button.setIcon(QtGui.QIcon(button_dict['icon']))

            self.toolbox_layout.addWidget(button)
        
            # Connect Menu buttons
            menu_button = self.findChild(QtWidgets.QAction, button_dict['object_name'] + "_menu")
            if menu_button:
                menu_button.triggered.connect(button_dict['function'])

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
        # Get the image path jpg or png
        image_path = QtWidgets.QFileDialog.getOpenFileName(self, 'Open file', '', "Image files (*.jpg *.png)")[0]
        
        # If the image path is not empty, set the source image
        if image_path:

            self.set_source_image(image_path)            
            self.update_source_image()

            # Assign the source image path
            self.source_image_path = image_path

            # Enable the buttons
            self.change_buttons_state("source_opened", False)

    def save_output_image(self):
        """
        @brief Saves the output image to the source image path.
        """
        if self.source_image_path:
            self.get_output_image().save_image(self.source_image_path)

            # UX - Clear the output image and update the source image
            self.findChild(QtWidgets.QPushButton, "output_clear").click()
            self.set_source_image(self.source_image_path)
            self.update_source_image()


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

    @progress_bar_decorator(0.4)
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
    
    @progress_bar_decorator(0.4)
    def update_output_image(self):
        """
        @brief Updates the output image display in the UI.
        """
        label_size = (self.output_image_frame.width(), self.output_image_frame.height())
        
        self.output_image_frame.setPixmap(
            QPixmap.fromImage(
                self.get_output_image().get_QImage()
            ).scaled(label_size[0], label_size[1])
        )
        self.output_image_frame.setAlignment(Qt.AlignCenter)

        self.change_buttons_state("full", False)
        

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
        """,
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
            self.change_buttons_state("default", True)
            self.source_image_frame.clear()

        elif object_name == "output_clear":
            self.output_image_history = {"image_history":[], "current_index":0}
            self.change_buttons_state("source_opened", False)
            self.source_side.click()
            self.output_image_frame.clear()
        

if __name__ == '__main__':
    """
    @brief Main entry point of the application. Creates an instance of UI_Interface and runs the application.
    """
    print("Testing UI_Interface class")

    app = QtWidgets.QApplication(sys.argv)
    window = UI_Interface()
    sys.exit(app.exec_())

