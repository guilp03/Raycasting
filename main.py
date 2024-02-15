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
from phong import normalize, collor
from cena import adcionar_esfera, adcionar_plano, adcionar_triangulo, adicionar_luz, OBJETOS_LISTA, LUZES_LISTA

def main():
    ''''' INICIALIZAÇÃO DO QUE É NECESSÁRIO PARA O RAYCASTING/RAYTRACING '''''
    camera = np.array([0,0,0])
    centro = np.array([1,0,0])
    up = np.array([0,1,0])
    distancia = 1
    hres = 700
    vres = 700
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
    adicionar_luz(objeto.Luz((5,0,0), (255,255,255), (0,0,0)))

    quadrado = readobj.read_obj("square.obj", (126,126,126))
    for triangulo_ in quadrado:
        adcionar_triangulo(
            *triangulo_, 
            _material = objeto.Material(
                kd=(0.5,0.5,0.5),
                ke=(0.5,0.5,0.5),
                ka=(0.5,0.5,0.5),
                kr=(0.5,0.5,0.5),
                kt = (0.5,0.5,0.5),
                n = 1
                )
            )


    cubo = readobj.read_obj("cube.obj", (50,160,50))
    cubo_objeto = objeto.Objeto()
    for triangulo_ in cubo:
        cubo_objeto.adcionar_triangulo(*triangulo_)
    OBJETOS_LISTA.append(cubo_objeto)

    adcionar_esfera(0.5, (2,0,0), (255,255,255))

    # for que percorre toda a tela e gera a intesecção com os objetos
    # para gerar a imagem final
    for i in range(hres):
        for j in range(vres):
            vetor_atual = vetor_inicial + i*desl_h + j*desl_v
            imagem[j,i] = collor(camera, vetor_atual, OBJETOS_LISTA)[1]
            print(f"{'{:.2f}'.format(i*100/hres)}%", end='\r')
    print("100.00%", end='\r')

    cv.imshow("grupo06", imagem)

    cv.waitKey(0)
    cv.destroyWindow('i')

if __name__ == "__main__":
    main()