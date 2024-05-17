import numpy as np
import cv2
import skimage as ski

import Image

class Image_Operations:
    def __init__(self, image:np.ndarray = None):
        """
        Constructor for image_operator class
        :param image: np.ndarray or str
        """
        
        if image is not None:
            self.set_source_image( image )
    

    def set_source_image(self, image:np.ndarray):
        self.source_image = Image.Image(image)
        print("Image type src: ", self.source_image.get_image_channels_type())

        self.__set_output_image( self.get_source_image().get_nd_image() )

    def __set_output_image(self, output:np.ndarray):
        self.__output_image = Image.Image(output)
        print("Image type out: ", self.__output_image.get_image_channels_type())
    
    def get_source_image(self) -> np.ndarray:    
        return self.source_image
    
    def get_output_image(self) -> np.ndarray:
        return self.__output_image    


    def convert_to_gray(self) -> np.ndarray:
        """
        Function to convert the image to grayscale
        :return: np.ndarray
        """

        """
        cv2.imshow('source', self.source_image)
        cv2.waitKey(1000)
        cv2.destroyAllWindows()
        """

        src_type = self.get_source_image().get_image_channels_type()
        if src_type == 'BGR':
            cvt_type = cv2.COLOR_BGR2GRAY
        elif src_type == 'GRAY':
            return
        else:
            raise ValueError('Invalid image type')
          
        self.__set_output_image(cv2.cvtColor(self.get_source_image().get_nd_image(), cvt_type))
        return self.get_output_image().get_nd_image()
    
    def convert_to_hsv(self) -> np.ndarray:
        """
        Function to convert the image to HSV
        :return: np.ndarray
        """
        src_type = self.get_source_image().get_image_channels_type()
        
        if src_type == 'BGR':
            cvt_type = cv2.COLOR_BGR2HSV
        elif src_type == 'GRAY':
            return
        else:
            raise ValueError('Invalid image type')
        
        self.__set_output_image(cv2.cvtColor(self.get_source_image().get_nd_image(), cvt_type))
        return self.get_output_image().get_nd_image()
    
    def edge_detection(self, method:str='roberts', threshold1:int=100, threshold2:int=200 ) -> np.ndarray:
        """
        Function to detect edges in the image
        :param method: str
        :param threshold1: int
        :param threshold2: int
        :return: np.ndarray
        """
        
        if self.get_source_image().get_image_channels_type() == 'BGR':
            self.set_source_image(self.convert_to_gray())

        if method == 'roberts':
            self.__set_output_image(ski.filters.roberts(self.get_source_image().get_nd_image()))
        elif method == 'sobel':
            self.__set_output_image(ski.filters.sobel(self.get_source_image().get_nd_image()))
        elif method == 'scharr':
            self.__set_output_image(ski.filters.scharr(self.get_source_image().get_nd_image()))
        elif method == 'prewitt':
            self.__set_output_image(ski.filters.prewitt(self.get_source_image().get_nd_image()))
        else:
            raise ValueError('Invalid method for edge detection')
    
    def segment_image(self, method:str='multi_otsu', num_classes:int=3) -> np.ndarray:
        """
        Function to segment the image
        :param method: str
        :param num_classes: int
        :return: np.ndarray
        """
        if self.get_source_image().get_image_channels_type() == 'BGR':
            self.set_source_image(self.convert_to_gray())

        if method == 'multi_otsu':
            self.__set_output_image(ski.filters.threshold_multiotsu(self.get_source_image().get_nd_image(), num_classes))
        elif method == 'chan_vese':
            self.__set_output_image(ski.segmentation.chan_vese(self.get_source_image().get_nd_image(), num_classes))
        elif method == 'morphological_snakes':
            self.__set_output_image(ski.segmentation.morphological_chan_vese(self.get_source_image().get_nd_image(), num_classes))
        else:
            raise ValueError('Invalid method for segmentation')
        
    def show_output_image(self):
        """
        Function to display the output image
        """
        try:
            cv2.imshow('output', self.get_output_image().get_nd_image())
            cv2.waitKey(1000)
            cv2.destroyAllWindows()
        except:
            self.__set_output_image(self.get_output_image().get_nd_image().astype(np.uint8))
            cv2.imshow('output', self.get_output_image().get_nd_image())
            cv2.waitKey(1000)
            cv2.destroyAllWindows()
            
if __name__ == '__main__':
    print(" Testing image_operator class: ")    
    image = cv2.imread('src/images/lena.png', cv2.IMREAD_COLOR)
    img_op = Image_Operations(image)

    img_op.convert_to_gray()

    img_op.show_output_image()

    img_op.edge_detection( method='sobel' )

    img_op.show_output_image()