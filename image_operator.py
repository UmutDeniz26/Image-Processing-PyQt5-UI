import numpy as np

class image_operator:
    def __init__(self, image:np.ndarray):
        """
        Constructor for image_operator class
        :param image: np.ndarray
        """
        self.image = image
        