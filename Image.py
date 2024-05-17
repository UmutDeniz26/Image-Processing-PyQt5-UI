import numpy as np
import cv2
from PyQt5.QtGui import QPixmap, QImage


class Image:
    def __init__(self, image:np.ndarray = None):
        """
        Constructor for image_operator class
        :param image: np.ndarray or str
        """
        
        if image is not None:
            self.set_image( image )

    def set_image(self, image:np.ndarray):
        if type(image) == str:
            self.image = cv2.imread(image, cv2.IMREAD_COLOR)
        elif type(image) == np.ndarray:
            self.image = image
        else:
            raise ValueError('Invalid input, type: ', type(image))
            
    def get_nd_image(self) -> np.ndarray:
        if type(self.image) != np.ndarray:
            raise ValueError('Invalid image type')    
        return self.image
    
    def get_image_channels_type(self) -> str:
        """
        Function to get the type of the image channels like RGB, BGR, HSV, GRAY etc.
        :return: str
        """
        channels = self.get_nd_image().shape[2] if len(self.get_nd_image().shape) > 2  else 1
        return 'BGR' if channels == 3 else 'GRAY' 
    
    def get_QImage(self) -> QImage:
        img = self.get_nd_image()
        return QImage(
            img.data, 
            img.shape[1],
            img.shape[0],
            img.strides[0],
            QImage.Format_BGR888 if self.get_image_channels_type() == 'BGR' else QImage.Format_Grayscale8
        )
    
if __name__ == '__main__':
    image = Image('src/images/lena.png')
    
