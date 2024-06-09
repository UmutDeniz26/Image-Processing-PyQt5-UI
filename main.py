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
