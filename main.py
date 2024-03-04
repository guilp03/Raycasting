'''ENTRADA DO PROGRAMA

Define a câmera, as variáveis globais e adiciona os objetos à cena
Depois, chama as funções para fazer a renderização
'''
import numpy as np
import cv2 as cv
import readobj
import objeto
import afim
INF = 9999999999
from phong import normalize, collor, phong_no_recursion, phong
from cena import adcionar_esfera, adcionar_plano, adcionar_triangulo, adicionar_luz, OBJETOS_LISTA, LUZES_LISTA
import cena
import bezier

def main():
    ''''' INICIALIZAÇÃO DO QUE É NECESSÁRIO PARA O RAYCASTING/RAYTRACING '''''
    camera = np.array([0,0,0])
    centro = np.array([1,0,0])
    up = np.array([0,1,0])
    distancia = 1
    hres = 900
    vres = 900
    tam_x = 1
    tam_y = 1
    # criação das coordenadas
    w = normalize(camera - centro) 
    u = normalize(np.cross(up,w))
    v = normalize(np.cross(w,u)) * -1
    # gera a imagem
    imagem = np.zeros((vres, hres, 3), dtype=np.uint8)
    # calculo do deslocamento
    desl_h = ((2*tam_x)/(hres-1)) * u
    desl_v = ((2*tam_y)/(vres-1)) * v
    # vetor no incio da tela
    vetor_inicial = - w * distancia - u * tam_x - tam_y * v
    #################################################################################
    ''''' INICIALIZAÇÃO DOS OBJETOS PARA CASOS TESTE '''''
    
    # Adicionar luz
    adicionar_luz(objeto.Luz((-4.0,3.0,0.0), (0.5,0.5,0.5)))
    adicionar_luz(objeto.Luz((0,-2,0),(0.5,0.5,0.5)))
    cena.COR_AMBIENTE = np.array((255,255,255))

 
    ## CURVAS DE BEZIER
    bez = bezier.BezierCurve(3, 3, 
                             [(7,0,-3.1),(7,1,-3),(7,2,-3),(7,3,-3)],
                             [(7,0,-2),(8,1,-2),(8,2,-2), (7, 3, -2)], 
                             [(7,0,-1),(8,1,-1),(8,2,-1), (7, 3, -1)], 
                             [(7,0,0),(7,1,0),(7,2,0), (7,3,0)])
    malha = bez.criar_malha(resolucao=15, _material = objeto.Material(
            kd=(0.3, 0.0 ,0.15),
            ke=(1.0, 0.0, 0.5),
            ka=(0.2,0.0,0.1),
            kr=0.5,
            kt=0.5,
            n=3,
            od=(255,255,255),
            reflete=False,
            refrata=False))
    cena.OBJETOS_LISTA.append(malha)
    
    bez2 = bezier.BezierCurve(2, 2, 
                             [(7,0,2),(7,1,2),(7,2,2)],
                             [(7,0,3),(7,1,3),(7,2,3)], 
                             [(7,0,4),(7,1,4),(7,2,4)])
    
    malha2 = bez2.criar_malha(resolucao=4, _material = objeto.Material(
            kd=(0,0,0),
            ke=(0.0, 1.0, 0.5),
            ka=(0,0,0),
            kr=0.5,
            kt=0.5,
            n=3,
            od=(255,255,255),
            reflete=False,
            refrata=False))
    cena.OBJETOS_LISTA.append(malha2)
    
    
    
    for i in range(hres):
        for j in range(vres):
            vetor_atual = vetor_inicial + i*desl_h + j*desl_v
            imagem[j,i] = phong(camera, vetor_atual, OBJETOS_LISTA, LUZES_LISTA, 3)
            print(f"{'{:.2f}'.format(i*100/hres)}%", end='\r')
    print("100.00%", end='\r')

    cv.imshow("grupo06 - bezier", imagem)
    cv.waitKey(0)
    cv.destroyWindow('i')

if __name__ == "__main__":
    main()