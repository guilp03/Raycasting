'''''FUNÇÕES PARA ADICIONAR OBJETOS'''''
import numpy as np
import objeto
OBJETOS_LISTA = []

# att: futuramente vai ser melhor criar uma classe pra cada
def adcionar_plano(cor, ponto, vetor):
    ''''' 0 = TIPO | 1 = COR |  2 = PONTO | 3 = VETOR_NORMAL '''''

    OBJETOS_LISTA.append(["plano", np.array(cor), np.array(ponto), np.array(vetor)])

def adcionar_esfera(raio, centro, cor):
    ''''' 0 = TIPO | 1 = COR |2 = RAIO | 3 = CENTRO ''''' 

    OBJETOS_LISTA.append(objeto.Esfera(np.array(cor),raio,np.array(centro)))

def adcionar_triangulo(cor, p1, p2, p3):
    ''''' 0 = TIPO | 1 = COR | 2,3,4 = PONTO | 5 = VETOR_NORMAL '''''
    # transforma os pontos em array
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)
    cor = np.array(cor)
    tri = objeto.Triangulo(cor, p1, p2, p3)
    OBJETOS_LISTA.append(tri)