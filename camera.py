import numpy as np
import cv2 as cv
INF = 9999999999
def normalize(v):
    v = v/np.linalg.norm(v)
    return v

def collor(camera, vetor_atual, objetos):
    T = INF
    cor = np.array([0,0,0])
    for i in objetos:
        if i[0].lower() == "esfera":
            '''''INTERSECÇÃO COM A ESFERA'''''
            oc = camera - i[2]
            a = np.dot(vetor_atual, vetor_atual)
            b = 2 * np.dot(oc, vetor_atual)
            c = np.dot(oc, oc) - i[1] ** 2
            delta = b ** 2 - (4 * a * c)

            if delta < 0:
                continue
            
            tmp1 = (-b + np.sqrt(delta))/(2*a)
            tmp2 = (-b - np.sqrt(delta))/(2*a)
            
            if tmp1 < 0 and tmp2 < 0:
                continue
            if tmp1 < 0.01:
                tmp1 = INF
            if tmp2 < 0.01:
                tmp2 = INF
            if tmp1 < tmp2:
                current = tmp1
            else:
                current = tmp2   
                     
        elif i[0].lower() == "plano":
            '''''INTERSECÇÃO COM O PLANO'''''
            tmp = np.dot(i[2],vetor_atual)
            if tmp == 0:
                continue
            current = (np.dot(i[2], i[1]) - np.dot(i[2], camera)) / tmp
            #print(current)
            if current < 0.01:
                current = INF
        if current < T:
            T = current
            cor = i[3]
    return cor

def adcionar_plano(ponto, vetor, cor):
    '''''0 = TIPO |  1 = PONTO |  2 = VETOR |  3 = COR'''''
    objetos.append(["plano",np.array(ponto),np.array(vetor), np.array(cor)])

def adcionar_esfera(raio, ponto, cor):
    '''''0 = TIPO | 1 = RAIO | 2 = CENTRO | 3 = COR''''' 
    objetos.append(["esfera", raio, np.array(ponto), np.array(cor)])

camera = np.array([0,0,0])
centro = np.array([1,0,0])
up = np.array([0,1,0])
distancia = 1
hres = 500
vres = 500
tam_x = 0.5
tam_y = 0.5

w = normalize(centro - camera) # vetor normal
u = normalize(np.cross(up,w))
v = normalize(np.cross(w,u)) * -1

imagem = np.zeros((vres, hres, 3), dtype=np.uint8)

desl_h = ((2*tam_x)/(hres-1)) * u
desl_v = ((2*tam_y)/(vres-1)) * v

vetor_inicial = w * distancia - u * tam_x - tam_y * v

objetos = []

for i in range(hres):
    for j in range(vres):
        vetor_atual = vetor_inicial + i*desl_h + j*desl_v
        imagem[j,i] = collor(camera, vetor_atual, objetos)
        #checar a intersecao

cv.imshow("grupo05", imagem)
cv.waitKey(0)
cv.destroyWindow('i')
