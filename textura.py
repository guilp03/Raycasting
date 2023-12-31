import numpy as np
import cv2 as cv
import math
from cv2.typing import MatLike

class Textura:
    _arquivo: str
    img: MatLike
    width: int
    height: int
    def __init__(self, arquivo: str) -> None:
        self.img = cv.imread(arquivo, cv.IMREAD_COLOR)
        self._arquivo = arquivo
        self.width = self.img.shape[1]
        self.height = self.img.shape[0]
    
    def map(self, vty: float, vtx: float):
        # '1 -' para por na orientação correta
        ty = int((1-math.modf(vty)[0])*self.height)
        tx = int(math.modf(vtx)[0]*self.width)
        return tuple(self.img[ty,tx])
        
        