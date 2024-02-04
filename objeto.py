'''DEFINIÇÂO DOS OBJETOS E FUNÇÕES AUXILIARES'''
import numpy as np
# import textura
INF = 9999999999
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
    text: None#textura.Textura
    
    x_max: float
    x_min: float
    y_max: float
    y_min: float
    z_max: float
    z_min: float
    
    def __init__(self, cor, p1, p2, p3, t1 = None, t2 = None, t3 = None, text = None) -> None:
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.cor = cor
        self.t1 = t1
        self.t2 = t2
        self.t3 = t3
        self.normal = normalize(np.cross(p2-p1,p3-p1))
        self.text = text
        self.set_bb()
        
    def set_bb(self):
        self.x_max = max(self.p1[0], self.p2[0], self.p3[0])
        self.x_min = min(self.p1[0], self.p2[0], self.p3[0])
        self.y_max = max(self.p1[1], self.p2[1], self.p3[1])
        self.y_min = min(self.p1[1], self.p2[1], self.p3[1])
        self.z_max = max(self.p1[2], self.p2[2], self.p3[2])
        self.z_min = min(self.p1[2], self.p2[2], self.p3[2])
        
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

class Esfera:
    cor: np.ndarray
    raio: float
    centro: np.ndarray
    
    x_max: float
    x_min: float
    y_max: float
    y_min: float
    z_max: float
    z_min: float
        
    def set_bb(self):
        self.x_max = self.centro[0] + self.raio
        self.x_min = self.centro[0] - self.raio
        self.y_max = self.centro[1] + self.raio
        self.y_min = self.centro[1] - self.raio
        self.z_max = self.centro[2] + self.raio
        self.z_min = self.centro[2] - self.raio
    
    def __init__(self, cor, raio, centro):
        self.cor = cor
        self.raio = raio
        self.centro = centro
        
        self.set_bb()
    
    def __getitem__(self, key):
        ''''' 0 = TIPO | 1 = COR |2 = RAIO | 3 = CENTRO ''''' 
        match key:
            case 0:
                return "esfera"
            case 1:
                return self.cor
            case 2:
                return self.raio
            case 3:
                return self.centro
                
            
class Objeto:
    subobjetos: list
    x_max: float
    x_min: float
    y_max: float
    y_min: float
    z_max: float
    z_min: float
    def __init__(self) -> None:
        self.subobjetos = []
        self.x_max = -INF
        self.x_min = INF
        self.y_max = -INF
        self.y_min = INF
        self.z_max = -INF
        self.z_min = INF
        
    def __getitem__(self, key):
        ''' 0 = TIPO '''
        match key:
            case 0:
                return "objeto"
            case 1:
                return np.array((0,0,0))
            
    def adcionar_triangulo(self, cor, p1, p2, p3, t1 = None, t2 = None, t3 = None, text = None):
        ''''' 0 = TIPO | 1 = COR | 2,3,4 = PONTO | 5 = VETOR_NORMAL | 6,7,8 = VETOR_TEXTURA | 9 = TEXTURA '''''
        # transforma os pontos em array
        p1 = np.array(p1)
        p2 = np.array(p2)
        p3 = np.array(p3)
        
        self.x_max = max(self.x_max, p1[0], p2[0], p3[0])
        self.x_min = min(self.x_min, p1[0], p2[0], p3[0])
        self.y_max = max(self.y_max, p1[1], p2[1], p3[1])
        self.y_min = min(self.y_min, p1[1], p2[1], p3[1])
        self.z_max = max(self.z_max, p1[2], p2[2], p3[2])
        self.z_min = min(self.z_min, p1[2], p2[2], p3[2])
        
        if t1 and t2 and t3 and text:
            t1 = np.array(t1)
            t2 = np.array(t2)
            t3 = np.array(t3)
        else:
            t1 = None
            t2 = None
            t3 = None
            text = None
        
        self.subobjetos.append(Triangulo(np.array(cor),p1,p2,p3,t1,t2,t3,text))