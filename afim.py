'''DEFINIÇÂO DAS TRANSFORMAÇÕES AFIMS SOBRE PONTOS'''
import numpy as np

'''FUNÇÃO PARA RETIRAR O NP.ARRAY, FACILITANDO COMPOSIÇÃO DE TRANSFORMAÇÕES'''
def nparray_para_tuple(vetor):
    if type(vetor) == list or type(vetor) == tuple or type(vetor) == np.ndarray:
        return tuple(nparray_para_tuple(i) for i in vetor)
    else:
        return vetor

'''DEFININDO MATRIZES DE ROTAÇÃO E REFLEXÃO'''
def translacao (ponto, p1,p2,p3):
    ponto = ponto + (1,)
    ponto = np.array(ponto)
    matriz_translacao = np.array([
        [1, 0, 0, p1],
        [0, 1, 0, p2], 
        [0, 0, 1, p3], 
        [0, 0, 0, 1]
    ])
    value = matriz_translacao @ ponto
    value = np.delete(value, 3)
    return nparray_para_tuple(value)

def rotacao_x(ponto, t):
    t = np.radians(t)
    ponto = ponto + (1,)
    ponto = np.array(ponto)
    matriz_rotacao = np.array([
        [1, 0, 0, 0], 
        [0, np.cos(t), -np.sin(t), 0], 
        [0,np.sin(t), np.cos(t), 0], 
        [0, 0, 0, 1]
    ])
    value = matriz_rotacao @ ponto
    value = np.delete(value, 3)
    return nparray_para_tuple(value)

def rotacao_y(ponto, t):
    t = np.radians(t)
    ponto = ponto + (1,)
    ponto = np.array(ponto)
    matriz_rotacao = np.array([
        [np.cos(t), 0, np.sin(t), 0], 
        [0, 1, 0, 0], 
        [-np.sin(t), 0, np.cos(t), 0], 
        [0, 0, 0, 1]
    ])
    value = matriz_rotacao @ ponto
    value = np.delete(value, 3)
    return nparray_para_tuple(value)

def rotacao_z(ponto, t):
    t = np.radians(t)
    ponto = ponto + (1,)
    ponto = np.array(ponto)
    matriz_rotacao = np.array([
        [np.cos(t), -np.sin(t), 0, 0],
        [np.sin(t), np.cos(t), 0, 0], 
        [0, 0, 1, 0], 
        [0, 0, 0, 1]
    ])
    value = matriz_rotacao @ ponto
    value = np.delete(value, 3)
    return nparray_para_tuple(value)

def expandir(ponto, t):
    ponto = ponto + (1,)
    ponto = np.array(ponto)
    ponto = ponto + (1,)
    ponto = np.array(ponto)
    matriz_rotacao = np.array([
        [t, 0, 0, 0],
        [0, t, 0, 0], 
        [0, 0, t, 0], 
        [0, 0, 0, 1]
    ])
    value = matriz_rotacao @ ponto
    value = np.delete(value, 3)
    return nparray_para_tuple(value)