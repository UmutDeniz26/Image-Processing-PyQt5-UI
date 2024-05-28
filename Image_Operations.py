import numpy as np
import cv2
import skimage as ski

from Image import Image

class Image_Operations:
    def __init__(self, image:np.ndarray = None):
        """
        Constructor for image_operator class
        :param image: np.ndarray or str
        """
        
        if image is not None:
            self.set_source_image( image )

        # Initialize the image history for redo and undo operations
        self.source_image_history = {"image_history":[], "current_index":-1}
        self.output_image_history = {"image_history":[], "current_index":-1}
    
    # Set the source image
    def set_source_image(self, image:np.ndarray):
        self.source_image = Image(image)
        self.source_image_history["image_history"].append(self.source_image)

    # Set the output image
    def set_output_image(self, output:np.ndarray):
        if type(output) != Image:
            self.__output_image = Image(output)

        self.output_image_history["current_index"] += 1
        self.output_image_history["image_history"].append(self.__output_image)
    
    # Get the source image
    def get_source_image(self) -> np.ndarray:    
        index = self.source_image_history["current_index"]
        return self.source_image_history["image_history"][index]
    
    # Get the output image
    def get_output_image(self) -> np.ndarray:
        index = self.output_image_history["current_index"]
        return self.output_image_history["image_history"][index] 
    
    def undo_output_image(self):
        self.output_image_history["current_index"] -= 1 if self.output_image_history["current_index"] > 0 else 0

        # I didn't use set function because I don't want to update the history list
        self.__output_image = self.output_image_history["image_history"][self.output_image_history["current_index"]]

    def redo_output_image(self):
        self.output_image_history["current_index"] +=\
            1 if self.output_image_history["current_index"] < len(self.output_image_history["image_history"]) - 1 else 0

        # I didn't use set function because I don't want to update the history list
        self.__output_image = self.output_image_history["image_history"][self.output_image_history["current_index"]]

    def undo_source_image(self):
        self.source_image_history["current_index"] -= 1

        # I didn't use set function because I don't want to update the history list 
        self.source_image = self.source_image_history["image_history"][self.source_image_history["current_index"]]

    # Function to convert the image to a specified color space
    def convesion_actions(self, method:str='gray') -> np.ndarray:
        src_type = self.get_source_image().get_image_channels_type()

        if method == 'gray':
            if src_type == 'BGR':
                cvt_type = cv2.COLOR_BGR2GRAY
            elif src_type == 'GRAY':
                return
            else:
                raise ValueError('Invalid image type') 
        elif method == 'hsv':
            if src_type == 'BGR':
                cvt_type = cv2.COLOR_BGR2HSV
            elif src_type == 'GRAY':
                return
        else:
            raise ValueError('Invalid method for conversion')
        
        return cv2.cvtColor(self.get_source_image().get_nd_image(), cvt_type)

    # Function to detect edges in the image
    def edge_detection_actions(self, method:str='roberts', threshold1:int=100, threshold2:int=200 ) -> np.ndarray:
        
        # Check if the image is in grayscale. If not, convert it to grayscale
        if self.get_source_image().get_image_channels_type() == 'BGR':
            img = self.convesion_actions(method='gray')

        # Detect edges using the specified method
        if method == 'roberts':
            ret = ski.filters.roberts(img)
        elif method == 'sobel':
            ret = ski.filters.sobel(img)
        elif method == 'scharr':
            ret = ski.filters.scharr(img)
        elif method == 'prewitt':
            ret = ski.filters.prewitt(img)
        else:
            raise ValueError('Invalid method for edge detection')
    
        return ret
    # Function to segment the image
    def segment_image(self, method:str='multi_otsu', num_classes:int=3) -> np.ndarray:
    
        # Check if the image is in grayscale. If not, convert it to grayscale
        if self.get_source_image().get_image_channels_type() == 'BGR':
            img = self.convesion_actions(method='gray')

        # Detect segments using the specified method
        if method == 'multi_otsu':
            ret = ski.filters.threshold_multiotsu(img, num_classes)
        elif method == 'chan_vese':
            ret = ski.segmentation.chan_vese(img, num_classes)
        elif method == 'morph_snakes':
            ret = ski.segmentation.morphological_chan_vese(img, num_classes)
        else:
            raise ValueError('Invalid method for segmentation, method: ', method)
        
        return ret
        
if __name__ == '__main__':
    print(" Testing image_operator class: ")    
    image = cv2.imread('src/images/lena.png', cv2.IMREAD_COLOR)
    img_op = Image_Operations(image)
    img_op.convert_to_gray()
    img_op.edge_detection_actions( method='sobel' )
