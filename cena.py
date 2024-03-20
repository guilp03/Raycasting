'''''FUNÇÕES PARA ADICIONAR OBJETOS'''''
import numpy as np
import objeto
OBJETOS_LISTA = []
LUZES_LISTA = []
COR_AMBIENTE: np.ndarray # [0,255]³

# att: futuramente vai ser melhor criar uma classe pra cada
def adcionar_plano(cor, ponto, vetor, _material = None):
    ''''' 0 = TIPO | 1 = COR |  2 = PONTO | 3 = VETOR_NORMAL '''''

    OBJETOS_LISTA.append(objeto.Plano(cor, vetor, ponto, material=_material))

def adcionar_esfera(raio, centro, cor, _material = None):
    ''''' 0 = TIPO | 1 = COR |2 = RAIO | 3 = CENTRO ''''' 

    OBJETOS_LISTA.append(objeto.Esfera(np.array(cor),raio,np.array(centro), material=_material))

def adcionar_triangulo(cor, p1, p2, p3, t1 = None, t2 = None, t3 = None, text = None, _material = None):
    ''''' 0 = TIPO | 1 = COR | 2,3,4 = PONTO | 5 = VETOR_NORMAL '''''
    # transforma os pontos em array
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)
    t1 = np.array(t1)
    t2 = np.array(t2)
    t3 = np.array(t3)
    cor = np.array(cor)
    tri = objeto.Triangulo(cor, p1, p2, p3, t1, t2, t3, text, material=_material)
    OBJETOS_LISTA.append(tri)

def adicionar_luz(luz: objeto.Luz):
    LUZES_LISTA.append(luz)