import pyqtUi
import Image_Operations

import cv2
import numpy as np
import sys
import skimage as ski
from PyQt5 import QtWidgets, uic


if __name__ == '__main__':
    
    app = QtWidgets.QApplication(sys.argv)
    window = pyqtUi.PyqtUI()
    sys.exit(app.exec_())
