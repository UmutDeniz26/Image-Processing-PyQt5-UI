import numpy as np
import cv2
import skimage as ski

class image_operator:
    def __init__(self, image:np.ndarray = None):
        """
        Constructor for image_operator class
        :param image: np.ndarray or str
        """
        
        if image is not None:
            self.set_source_image( image )
            self.__set_output_image( self.get_source_image() )
    

    def set_source_image(self, image:np.ndarray):
        if type(image) == str:
            self.source_image = cv2.imread(image, cv2.IMREAD_COLOR)
        elif type(image) == np.ndarray:
            self.source_image = image
        else:
            raise ValueError('Invalid input')
            
        self.__set_output_image(self.get_source_image())
        self.__set_source_image_type(self.get_image_channels_type(image))
        
    def __set_output_image(self, output:np.ndarray):
        self.output_image = output
        self.__set_output_image_type(self.get_image_channels_type(output))
        
    
    def __set_output_image_type(self, output_type:str):
        self.output_image_type = output_type
    
    def __set_source_image_type(self, source_type:str):
        self.source_image_type = source_type
    
    def get_output_image_type(self) -> str:
        return self.output_image_type
    
    def get_source_image_type(self) -> str:
        return self.source_image_type
    
    
    def get_source_image(self) -> np.ndarray:    
        return self.source_image
    
    def get_output_image(self) -> np.ndarray:
        return self.output_image    


    def get_image_channels_type(self, image:np.ndarray) -> str:
        """
        Function to get the type of the image channels like RGB, BGR, HSV, GRAY etc.
        :return: str
        """
        if type(image) == str:
            image = cv2.imread(image, cv2.IMREAD_COLOR)


        channels = image.shape[2] if len(image.shape) > 2  else 1
        
        if channels == 3:
            return 'RGB'
        elif channels == 1:
            return 'GRAY'
        else:
            raise ValueError('Invalid number of channels')

    def convert_to_gray(self) -> np.ndarray:
        """
        Function to convert the image to grayscale
        :return: np.ndarray
        """
        
        if self.get_source_image_type() == 'RGB':
            cvt_type = cv2.COLOR_RGB2GRAY
        elif self.get_source_image_type() == 'GRAY':
            return
        else:
            raise ValueError('Invalid image type')
          
        self.__set_output_image(cv2.cvtColor(self.source_image, cvt_type))
        return self.get_output_image()
    
    def convert_to_hsv(self) -> np.ndarray:
        """
        Function to convert the image to HSV
        :return: np.ndarray
        """
        src_type = self.get_source_image_type()
        
        if src_type == 'RGB':
            cvt_type = cv2.COLOR_RGB2HSV
        elif src_type == 'GRAY':
            self.__set_output_image(cv2.cvtColor(self.source_image, cv2.COLOR_GRAY2BGR))
            cvt_type = cv2.COLOR_BGR2HSV
        else:
            raise ValueError('Invalid image type')
          
        self.__set_output_image(cv2.cvtColor(self.source_image, cvt_type))
        return self.get_output_image()
    
    def edge_detection(self, method:str='roberts', threshold1:int=100, threshold2:int=200 ) -> np.ndarray:
        """
        Function to detect edges in the image
        :param method: str
        :param threshold1: int
        :param threshold2: int
        :return: np.ndarray
        """
        if self.get_source_image_type() == 'RGB':
            self.set_source_image(self.convert_to_gray())


        if method == 'roberts':
            self.__set_output_image(ski.filters.roberts(self.source_image))
        elif method == 'sobel':
            self.__set_output_image(ski.filters.sobel(self.source_image))
        elif method == 'scharr':
            self.__set_output_image(ski.filters.scharr(self.source_image))
        elif method == 'prewitt':
            self.__set_output_image(ski.filters.prewitt(self.source_image))
        else:
            raise ValueError('Invalid method for edge detection')
    
    def segment_image(self, method:str='multi_otsu', num_classes:int=3) -> np.ndarray:
        """
        Function to segment the image
        :param method: str
        :param num_classes: int
        :return: np.ndarray
        """
        if self.get_source_image_type() == 'RGB':
            self.set_source_image(self.convert_to_gray())

        if method == 'multi_otsu':
            self.__set_output_image(ski.filters.threshold_multiotsu(self.source_image, num_classes))
        elif method == 'chan_vese':
            self.__set_output_image(ski.segmentation.chan_vese(self.source_image, num_classes))
        elif method == 'morphological_snakes':
            self.__set_output_image(ski.segmentation.morphological_chan_vese(self.source_image, num_classes))
        else:
            raise ValueError('Invalid method for segmentation')
        
    def show_output_image(self):
        """
        Function to display the output image
        """
        try:
            cv2.imshow('output', self.get_output_image())
            cv2.waitKey(1000)
            cv2.destroyAllWindows()
        except:
            self.__set_output_image(self.get_output_image().astype(np.uint8))
            cv2.imshow('output', self.get_output_image())
            cv2.waitKey(1000)
            cv2.destroyAllWindows()
            
if __name__ == '__main__':
    print(" Testing image_operator class: ")    
    image = cv2.imread('lena.png', cv2.IMREAD_COLOR)
    img_op = image_operator(image)

    img_op.convert_to_gray()

    img_op.show_output_image()

    img_op.edge_detection( method='sobel' )

    img_op.show_output_image()