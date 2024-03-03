'''DEFINIÇÂO DOS OBJETOS E FUNÇÕES AUXILIARES'''
import numpy as np
# import textura
INF = 9999999999
def normalize(v):
    ''''' NORMALIZAÇÃO DE VETOR (NÃO TEM NO NUMPY) '''''
    v = v/np.linalg.norm(v)
    return v

class Luz:
    ponto: np.ndarray # R³
    intensidade: np.ndarray # [0,1]³
    
    def __init__(self, ponto, intensidade):
        self.ponto = np.array(ponto)
        self.intensidade = np.array(intensidade)

class Material:
    k_difuso: np.ndarray # [0,1]³
    k_especular: np.ndarray # [0,1]³
    k_ambiental: np.ndarray # [0,1]³
    k_reflexão: float # [0,1]
    k_transmissão: float # [0,1]
    k_rugosidade: float # > 0
    o_difuso: np.ndarray # [0,255]³
    ior: float # >= 1
    reflete: bool
    refrata: bool
    
    def __init__(self, kd, ke, ka = (1,1,1), kr = 0.0, kt = 0.0, n: float = 0.0, od = (255,255,255), ior = 1,
                 reflete = False, refrata = False):
        self.k_difuso = np.array(kd)
        self.k_especular = np.array(ke)
        self.k_ambiental = np.array(ka)
        self.k_reflexão = kr
        self.k_transmissão = kt
        self.k_rugosidade = n
        self.o_difuso = np.array(od)
        self.ior = ior
        self.reflete = reflete
        self.refrata = refrata

class Triangulo:
    p1: np.ndarray # R³
    p2: np.ndarray # R³
    p3: np.ndarray # R³
    cor: np.ndarray # [0,255]³
    normal: np.ndarray # R³ normalizado
    t1: np.ndarray # R³
    t2: np.ndarray # R³
    t3: np.ndarray # R³
    text: None #textura.Textura
    material: Material = None
    
    x_max: float
    x_min: float
    y_max: float
    y_min: float
    z_max: float
    z_min: float
    
    def __init__(self, cor, p1, p2, p3, t1 = None, t2 = None, t3 = None, text = None, material = None) -> None:
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
        self.material = material
        
    def set_bb(self):
        self.x_max = max(self.p1[0], self.p2[0], self.p3[0])
        self.x_min = min(self.p1[0], self.p2[0], self.p3[0])
        self.y_max = max(self.p1[1], self.p2[1], self.p3[1])
        self.y_min = min(self.p1[1], self.p2[1], self.p3[1])
        self.z_max = max(self.p1[2], self.p2[2], self.p3[2])
        self.z_min = min(self.p1[2], self.p2[2], self.p3[2])
        
    def __getitem__(self, key):
        ''' 0 = TIPO | 1 = COR | 2,3,4 = PONTO | 5 = VETOR_NORMAL | 6,7,8 = VETOR_TEXTURA | 9 = TEXTURA | 10 = MATERIAL '''
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
            case 10: 
                return self.material
       
            
class Plano:
    cor: np.ndarray # [0,255]³
    normal: np.ndarray # R³ normalizado
    ponto: np.ndarray
    material: Material
    
    def __init__(self, cor, normal, ponto, material = None) -> None:
        self.cor = np.array(cor)
        self.normal = np.array(normal)
        self.ponto = np.array(ponto)
        self.material = material
        
    def __getitem__(self, key):
        ''''' 0 = TIPO | 1 = COR |  2 = PONTO | 3 = VETOR_NORMAL '''''
        match key:
            case 0:
                return "plano"
            case 1:
                return self.cor
            case 2:
                return self.ponto
            case 3:
                return self.normal
    
    
class Esfera:
    cor: np.ndarray # [0,255]³
    raio: float
    centro: np.ndarray # R³
    material: Material
    
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
    
    def __init__(self, cor, raio, centro, material = None):
        self.cor = cor
        self.raio = raio
        self.centro = centro
        self.material = material
        
        self.set_bb()
    
    def __getitem__(self, key):
        ''''' 0 = TIPO | 1 = COR |2 = RAIO | 3 = CENTRO | 10 = MATERIAL ''''' 
        match key:
            case 0:
                return "esfera"
            case 1:
                return self.cor
            case 2:
                return self.raio
            case 3:
                return self.centro
            case 10:
                return self.material
                
            
class Objeto:
    subobjetos: list
    material: Material
    x_max: float
    x_min: float
    y_max: float
    y_min: float
    z_max: float
    z_min: float
    def __init__(self, material = None) -> None:
        self.subobjetos = []
        self.x_max = -INF
        self.x_min = INF
        self.y_max = -INF
        self.y_min = INF
        self.z_max = -INF
        self.z_min = INF
        self.material = material
        
    def __getitem__(self, key):
        ''' 0 = TIPO '''
        match key:
            case 0:
                return "objeto"
            case 1:
                return np.array((0,0,0))
            case 10:
                return self.material
            
    def adcionar_triangulo(self, cor, p1, p2, p3, t1 = None, t2 = None, t3 = None, text = None, _material = None):
        ''''' 0 = TIPO | 1 = COR | 2,3,4 = PONTO | 5 = VETOR_NORMAL | 6,7,8 = VETOR_TEXTURA | 9 = TEXTURA | 10 = MATERIAL '''''
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
        if self.material is not None and _material is None:
            _material = self.material
        self.subobjetos.append(Triangulo(np.array(cor),p1,p2,p3,t1,t2,t3,text, material=_material))