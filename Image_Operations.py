import numpy as np
import cv2
import skimage as ski

from Image import Image

class Image_Operations(Image):
    def __init__(self, image:np.ndarray = None):
        """
        Constructor for image_operator class
        :param image: np.ndarray or str
        """
        
        if image is not None:
            self.set_source_image( image )

        # Initialize the image history for redo and undo operations
        self.output_image_history = {"image_history":[], "current_index":0}
    
    # Set the source image
    def set_source_image(self, image:np.ndarray):
        
        # If the input is a ndarray, create an Image object, else use the Image object directly
        self.source_image = Image(image) if type(image) != Image else image

    # Set the output image
    def set_output_image(self, output:np.ndarray):
        
        # If the input is a ndarray, create an Image object, else use the Image object directly
        self.__output_image = Image(output) if type(output) != Image else output

        if self.output_image_history["current_index"] == 0:
            self.output_image_history["image_history"].insert(0, self.__output_image)
        else:
            self.output_image_history["image_history"] = self.output_image_history["image_history"][self.output_image_history["current_index"]:]
            self.output_image_history["image_history"].insert(0, self.__output_image)
            self.output_image_history["current_index"] = 0
    
    # Get the source image
    def get_source_image(self) -> np.ndarray:    
        return self.source_image
    
    # Get the output image
    def get_output_image(self) -> np.ndarray:

        try:
            index = self.output_image_history["current_index"]
            return self.output_image_history["image_history"][index] 
        except:
            print("No output image available")



    ########################################### Undo - Redo Functions ####################################################

    def undo_output_image(self):
        try:
            if self.output_image_history["current_index"] < len(self.output_image_history["image_history"]) - 1 :
                self.output_image_history["current_index"] = (self.output_image_history["current_index"] + 1) 
                                                        
            # I didn't use set function because I don't want to update the history list
            self.__output_image = self.output_image_history["image_history"][self.output_image_history["current_index"]]
        except:
            print("No more undo operations")
    def redo_output_image(self):
        try:
            if self.output_image_history["current_index"] > 0:
                self.output_image_history["current_index"] = (self.output_image_history["current_index"] - 1)
            
            # I didn't use set function because I don't want to update the history list
            self.__output_image = self.output_image_history["image_history"][self.output_image_history["current_index"]]
        except:
            print("No more redo operations")

    #################################################################################################################


    # Function to convert the image to a specified color space
    def conversion_actions(self, method:str='gray') -> np.ndarray:
        src_type = self.get_source_image().get_image_channels_type()

        method = method.replace('_menu', '')

        if method == 'bgr_2_gray':
            if src_type == 'BGR':
                cvt_type = cv2.COLOR_BGR2GRAY
            elif src_type == 'GRAY':
                return
            else:
                raise ValueError('Invalid image type') 
        elif method == 'bgr_2_hsv':
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
            img = self.conversion_actions(method='bgr_2_gray')

        method = method.replace('_menu', '')

        # Detect edges using the specified method
        if method == 'edge_roberts':
            ret = ski.filters.roberts(img)
        elif method == 'edge_sobel':
            ret = ski.filters.sobel(img)
        elif method == 'edge_scharr':
            ret = ski.filters.scharr(img)
        elif method == 'edge_prewitt':
            ret = ski.filters.prewitt(img)
        else:
            raise ValueError('Invalid method for edge detection')
    
        return ret
    # Function to segment the image
    def segment_image(self, method:str='multi_otsu', num_classes:int=3) -> np.ndarray:
    
        # Check if the image is in grayscale. If not, convert it to grayscale
        if self.get_source_image().get_image_channels_type() == 'BGR':
            img = self.conversion_actions(method='bgr_2_gray')

        method = method.replace('_menu', '')

        # Detect segments using the specified method
        if method == 'segment_multi_otsu':
            tresholds = ski.filters.threshold_multiotsu(img, 2)
            ret = np.digitize(img, bins=tresholds)

        elif method == 'segment_chan_vese':
            ret = ski.segmentation.chan_vese(img, num_classes)
        elif method == 'segment_moprh_snakes':
            ret = ski.segmentation.morphological_chan_vese(img, num_classes)
        else:
            raise ValueError('Invalid method for segmentation, method: ', method)
        
        return ret
        
if __name__ == '__main__':
    print(" Testing image_operator class: ")    
    image = cv2.imread('src/images/lena.png', cv2.IMREAD_COLOR)
