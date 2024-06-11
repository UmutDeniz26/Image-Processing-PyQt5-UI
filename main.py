from UI_interface import UI_Interface
import Image_Operations

import cv2
import numpy as np
import sys
import skimage as ski
from PyQt5 import QtWidgets, uic


if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    window = UI_Interface()
    sys.exit(app.exec_())

"""
class -> UI_Interface( Image_Operations )
    def __init__(self):
    def get_buttons(self):
    def change_buttons_state(self, state = "default", visible = True):
    def sidebar_button_clicked(self):
    def init_buttons(self):
    def edit_full_menu_buttons(self, sender):
    def load_image_button(self):
    def save_output_image(self):
    def save_as_output_image(self):
    def export_output_image(self):
    def export_source_image(self):
    def update_source_image(self):
    def update_output_image(self):
    def conversion_handler(self):
    def segmentation_handler(self):
    def edge_detection_handler(self):
    def image_edit_operations(self):
    def exit_app(self): 
"""
"""
class -> Image_Operations(Image):
    def __init__(self, image:np.ndarray = None):
    def set_source_image(self, image:np.ndarray):
    def set_output_image(self, output:np.ndarray):
    def get_source_image(self) -> np.ndarray:
    def get_output_image(self) -> np.ndarray:
    def undo_output_image(self):
    def redo_output_image(self):
    def conversion_actions(self, method:str='gray') -> np.ndarray:
    def edge_detection_actions(self, method:str='roberts', threshold1:int=100, threshold2:int=200 ) -> np.ndarray:
    def segment_image(self, method:str='multi_otsu', num_classes:int=3) -> np.ndarray:
"""
"""
class -> Image:
    def __init__(self, image:np.ndarray = None):
    def set_image(self, image: np.ndarray):
    def get_nd_image(self) -> np.ndarray:
    def get_image_channels_type(self) -> str:
    def get_QImage(self) -> QImage:
    def save_image(self, path:str):

"""
