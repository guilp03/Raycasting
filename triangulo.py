import numpy as np
import textura

def normalize(v):
    ''''' NORMALIZAÇÃO DE VETOR (NÃO TEM NO NUMPY) '''''
    v = v/np.linalg.norm(v)
    return v

class Triangulo:
    p1: np.ndarray
    p2: np.ndarray
    p3: np.ndarray
    cor: np.ndarray
    normal: np.ndarray
    t1: np.ndarray
    t2: np.ndarray
    t3: np.ndarray
    text: textura.Textura
    
    x_max: float
    x_min: float
    y_max: float
    y_min: float
    z_max: float
    z_min: float
    
    def __init__(self, cor, p1, p2, p3, t1 = None, t2 = None, t3 = None, text: textura.Textura = None) -> None:
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.cor = cor
        self.t1 = t1
        self.t2 = t2
        self.t3 = t3
        self.normal = normalize(np.cross(p2-p1,p3-p1))
        self.text = text
        
        self.x_max = max(p1[0], p2[0], p3[0])
        self.x_min = min(p1[0], p2[0], p3[0])
        self.y_max = max(p1[1], p2[1], p3[1])
        self.y_min = min(p1[1], p2[1], p3[1])
        self.z_max = max(p1[2], p2[2], p3[2])
        self.z_min = min(p1[2], p2[2], p3[2])
        
    def __getitem__(self, key):
        ''' 0 = TIPO | 1 = COR | 2,3,4 = PONTO | 5 = VETOR_NORMAL | 6,7,8 = VETOR_TEXTURA | 9 = TEXTURA '''
        match key:
            case 0:
                return "triangulo"
            case 1:
                return self.cor
            case 2:
                return self.p1
            case 3:
                return self.p2
            case 4:
                return self.p3
            case 5:
                return self.normal
            case 6:
                return self.t1
            case 7:
                return self.t2
            case 8:
                return self.t3
            case 9:
                return self.text