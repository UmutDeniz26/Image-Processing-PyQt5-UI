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

    def set_image(self, image: np.ndarray):
        if isinstance(image, str):
            self.image = cv2.imread(image, cv2.IMREAD_COLOR)
        elif isinstance(image, np.ndarray):
            self.image = image
        else:
            raise ValueError('Invalid input, type: ', type(image))
            
    def get_nd_image(self) -> np.ndarray:
        if not isinstance(self.image, np.ndarray):
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
        """
        Function to get the QImage object from the numpy array
    
        Arguments:
            None
        
        Returns:
            QImage: QImage object - The image object to be displayed in the UI
        """


        img = self.get_nd_image()

        # Convert the image to 8-bit unsigned integer if it's not already
        if img.dtype != np.uint8:
            img = (img * 255).astype(np.uint8)

        # Convert grayscale to RGB
        if len(img.shape) == 2:  # Grayscale image
            img = cv2.cvtColor(img, cv2.COLOR_GRAY2RGB)
        else:  # Color image
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Get the shape of the image
        h, w, ch = img.shape

        # Convert the image to QImage
        bytes_per_line = ch * w

        # self.image_operator.get_output_image().get_nd_image() => array([ 92, 150], dtype=uint8)
        # Convert this to cv image
        if len(img.shape) == 1:
            img = img.reshape(img.shape[0], 1)

        return QImage(
            img.data, 
            w, 
            h, 
            bytes_per_line, 
            QImage.Format_RGB888
            )
    
    def save_image(self, path:str):
        """
        Function to save the image to the specified path
        :param path: str
        :return: None
        """

        nd_img = self.get_nd_image()

        # Convert the image to 8-bit unsigned integer if it's not already
        if nd_img.dtype != np.uint8 or nd_img.max() < 2:
            nd_img = (nd_img * 255).astype(np.uint8)

        cv2.imwrite(path, nd_img)
    
if __name__ == '__main__':
    image = Image('src/images/lena.png')
    
