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
    adicionar_luz(objeto.Luz((-4.0,3.0,0.0), (0.3,0.3,0.3)))
    #adicionar_luz(objeto.Luz((0.0,3.0,5.0), (0.5,0.5,0.5)))
    #adicionar_luz(objeto.Luz((0.0,3.0,-5.0), (0.5,0.5,0.5)))
    cena.COR_AMBIENTE = np.array((255,255,255))

    # quadrado = readobj.read_obj("square.obj", (255,255,255))
    # for triangulo_ in quadrado:
    #     adcionar_triangulo(
    #         *triangulo_, 
    #         _material = objeto.Material(
    #             kd=(0.0,0.0,0.0),
    #             ke=(0.5,0.5,0.5),
    #             ka=(0.1,0.1,0.1),
    #             kr= 0.5,
    #             kt = 0.5,
    #             n = 1
    #             )
    #         )


    #cubo = readobj.read_obj("cube.obj", (255,255,255))
    #cubo_objeto = objeto.Objeto()
    #for triangulo_ in cubo:
    #    cubo_objeto.adcionar_triangulo(
    #        *triangulo_,
    #        _material = objeto.Material(
    #            kd=(0.0,0.0,0.0),
    #            ke=(0.5,0.5,0.5),
    #            ka=(0.2,0.1,0.0),
    #            kr=0.5,
    #            kt = 0.5,
    #            n = 3,
    #            od = (160,70,0),
    #            reflete=False
    #        )
    #    )
    #OBJETOS_LISTA.append(cubo_objeto)
    adcionar_plano((0,0,0), (0,5,0), (-1,-1,0), _material = objeto.Material(
               kd=(0.4,0.4,0.4),
               ke=(0.0,0.0,0.0),
               ka=(0.0,0.0,0.0),
               kr = 0.4,
               kt = 0.9,
               n = 2,
               ior = 1.1,
               od = (255,255,255),
               reflete=False,
               refrata=True))

    #adcionar_esfera(0.4, (2,0,0), (255,255,255),
    #        _material = objeto.Material(
    #            kd=(0.0,0.0,0.0),
    #            ke=(0.0,0.0,0.0),
    #            ka=(0.0,0.0,0.0),
    #            kr = 0.4,
    #            kt = 0.9,
    #            n = 2,
    #            ior = 1.1,
    #            od = (255,255,255),
    #            reflete=False,
    #            refrata=True
    #        )
    #)
    #adcionar_esfera(0.4, (2,1,0), (255,255,255),
    #       _material = objeto.Material(
    #            kd=(0.0,0.0,0.0),
    #            ke=(0.0,0.0,0.0),
    #           ka=(0.0,0.0,0.0),
    #            kr = 0.4,
    #            kt = 0.9,
    #            n = 2,
    #            ior = 1.1,
    #            od = (255,255,255),
    #            reflete=False,
    #            refrata=True
    #        )
    #)
    #adcionar_esfera(0.4, (2,-1,0), (255,255,255),
    #        _material = objeto.Material(
    #            kd=(0.0,0.0,0.0),
    #            ke=(0.0,0.0,0.0),
    #            ka=(0.0,0.0,0.0),
    #            kr = 0.4,
    #            kt = 0.9,
    #            n = 2,
    #            ior = 1.1,
    #            od = (255,255,255),
    #            reflete=False,
    #            refrata=True
    #        )
    #)

    adicionar_luz(objeto.Luz((0,5,0),(0.5,0.5,0.5)))
    adcionar_esfera(1,(5,2,0), (255, 0, 0),
            objeto.Material(kd=(0.0,0.0,0.0),
            ke=(1,0,0.5),
            ka=(0.2,0.1,0.0),
            kr=0.5,
            kt=0.5,
            n=3,
            od=(255,0,127),
            reflete=False,
            refrata=False))
    
    adcionar_esfera(1,(5,2,2), (255, 255, 0),
            objeto.Material(kd=(0.5,0.3,0.3),
            ke=(1,0,0.5),
            ka=(0.2,0.1,0.0),
            kr=0.5,
            kt=0.5,
            n=3,
            od=(255,0,127),
            reflete=False,
            refrata=False))
    
    adcionar_esfera(1,(5,0,2), (0, 0, 255),
            objeto.Material(kd=(0.0,0.0,0.0),
            ke=(1,0,0.5),
            ka=(0.2,0.1,0.0),
            kr=0.5,
            kt=0.5,
            n=3,
            od=(255,0,127),
            reflete=False,
            refrata=False))

    
    #adcionar_triangulo((255, 0, 127), (0,3,-3), (3,0,3), (0,3,0), 
    #        objeto.Material(kd=(0.0,0.0,0.0),
    #        ke=(0.5,0.5,0.5),
    #        ka=(0.2,0.1,0.0),
    #        kr=0.5,
    #        kt = 0.5,
    #        n = 3,
    #        od = (160,70,0),
    #        reflete=False,
    #        refrata=True))
    # for que percorre toda a tela e gera a intesecção com os objetos
    # para gerar a imagem final
    for i in range(hres):
        for j in range(vres):
            vetor_atual = vetor_inicial + i*desl_h + j*desl_v
            imagem[j,i] = phong(camera, vetor_atual, OBJETOS_LISTA, LUZES_LISTA, 3)
            print(f"{'{:.2f}'.format(i*100/hres)}%", end='\r')
    print("100.00%", end='\r')

    cv.imshow("grupo06 - phong", imagem)
    
    # for i in range(hres):
    #     for j in range(vres):
    #         vetor_atual = vetor_inicial + i*desl_h + j*desl_v
    #         imagem[j,i] = collor(camera, vetor_atual, OBJETOS_LISTA)[1]
    #         print(f"{'{:.2f}'.format(i*100/hres)}%", end='\r')
    # print("100.00%", end='\r')

    # cv.imshow("grupo06 - collor", imagem)

    cv.waitKey(0)
    cv.destroyWindow('i')

if __name__ == "__main__":
    main()