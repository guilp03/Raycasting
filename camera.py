import numpy as np
import cv2 as cv
import obj
INF = 9999999999

def normalize(v):
    ''''' NORMALIZAÇÃO DE VETOR (NÃO TEM NO NUMPY) '''''
    v = v/np.linalg.norm(v)
    return v

def intersect_triangle(ray, v0, v1, v2, camera):
    '''''FUNÇÃO DADA NO LIVRO PRA CALCULAR A INTERSECÇÃO COM O TRIANGULO'''''
    a = v0[0] - v1[0]
    b = v0[0] - v2[0]
    c = ray[0]
    d = v0[0] - camera[0]

    e = v0[1] - v1[1]
    f = v0[1] - v2[1]
    g = ray[1]
    h = v0[1] - camera[1]

    i = v0[2] - v1[2]
    j = v0[2] - v2[2]
    k = ray[2]
    l = v0[2] - camera[2]

    m = f*k - g*j
    n = h*k - g*l
    p = f*l - h*j

    q = g*i - e*k
    s = e*j - f*i
######################################
    #evita divisão por 0
    div0 = a*m + b*q + c*s
    if div0 == 0:
        inv_denom = 0
    else:
        inv_denom = 1/div0
    
    e1 = d*m - b*n - c*p
    beta = e1*inv_denom
    if beta < 0:
        return INF
    
    r = e*l - h*i
    e2 = a*n + d*q + c*r
    gamma = e2 * inv_denom
    if gamma < 0:
        return INF  
    if beta + gamma > 1:
        return INF
    
    e3 = a*p - b*r + d*s
    t = e3 * inv_denom
    if t< 0.01:
        return INF
    
    return t

def collor(camera, vetor_atual, objetos):
    ''''' FUNÇÃO PARA CALCULAR A COR DE CADA OBJETO COM BASE NA MENOR DISTANCIA DA CAMERA '''''
    T = INF
    cor = np.array([0,0,0])
    for i in objetos:
        if i[0].lower() == "esfera":
            '''''INTERSECÇÃO COM A ESFERA'''''
            oc = camera - i[3]
            a = np.dot(vetor_atual, vetor_atual)
            b = 2 * np.dot(oc, vetor_atual)
            c = np.dot(oc, oc) - (i[2] ** 2)
            delta = b ** 2 - (4 * a * c)

            if delta < 0:
                continue
            # ENCONTRA OS PONTOS DE INTERSECÇÃO COM BHASKARA
            tmp1 = (-b + np.sqrt(delta))/(2*a)
            tmp2 = (-b - np.sqrt(delta))/(2*a)
            # tratamento de exceções
            if tmp1 < 0 and tmp2 < 0:
                continue
            if tmp1 < 0.01:
                tmp1 = INF
            if tmp2 < 0.01:
                tmp2 = INF
            # current recebe a menor distancia
            if tmp1 < tmp2:
                current = tmp1
            else:
                current = tmp2   

        elif i[0].lower() == "plano":
            '''''INTERSECÇÃO COM O PLANO'''''
            #verifica se o plano não é paralelo com os raios da camera
            tmp = np.dot(i[3],vetor_atual)
            if tmp == 0:
                continue
            #calcula a intersecção dos pontos
            current = (np.dot(i[3], i[2]) - np.dot(i[3], camera)) / tmp
            if current < 0.01:
                current = INF
        
        elif i[0].lower() == "triangulo":
            '''''INTERSECÇÃO COM O TRIANGULO'''
            #verifica se o raio não é paralelo com o triangulo
            tmp = np.dot(i[5],vetor_atual)
            if tmp == 0:
                continue
            current = intersect_triangle(vetor_atual, i[2], i[3], i[4], camera)
        # pega o menor tempo e joga em T
        if current < T:
            T = current
            cor = i[1]
    return cor
#################################################################################
'''''FUNÇÕES PARA ADICIONAR OBJETOS'''''
# att: futuramente vai ser melhor criar uma classe pra cada
def adcionar_plano(cor, ponto, vetor):
    ''''' 0 = TIPO | 1 = COR |  2 = PONTO | 3 = VETOR_NORMAL '''''

    objetos.append(["plano", np.array(cor), np.array(ponto), np.array(vetor)])

def adcionar_esfera(raio, ponto, cor):
    ''''' 0 = TIPO | 1 = COR |2 = RAIO | 3 = CENTRO ''''' 

    objetos.append(["esfera", np.array(cor), raio, np.array(ponto)])

def adcionar_triangulo(cor, p1, p2, p3):
    ''''' 0 = TIPO | 1 = COR | 2,3,4 = PONTO | 5 = VETOR_NORMAL '''''
    # transforma os pontos em array
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)
    # calculo do vetor normal ao triangulo
    v0 = p2 - p1
    v1 = p3 - p1
    vetor = normalize(np.cross(v0,v1))

    objetos.append(["triangulo", np.array(cor), p1, p2, p3, vetor])
#################################################################################
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
w = normalize(centro - camera) 
u = normalize(np.cross(up,w))
v = normalize(np.cross(w,u)) * -1
# gera a imagem
imagem = np.zeros((vres, hres, 3), dtype=np.uint8)
# calculo do deslocamento
desl_h = ((2*tam_x)/(hres-1)) * u
desl_v = ((2*tam_y)/(vres-1)) * v
# vetor no incio da tela
vetor_inicial = w * distancia - u * tam_x - tam_y * v
#################################################################################
''''' INICIALIZAÇÃO DOS OBJETOS PARA CASOS TESTE '''''
objetos = []
## EXEMPLOS
#adcionar_triangulo(cor, ponto1,ponto2,ponto3)
#adcionar_esfera(cor,raio,centro)
#adcionar_plano(cor, ponto, vetor_normal)

#adcionar_esfera(0.5, (1, 0, 0), (0, 255, 0))
#adcionar_plano((0, -1, 0), (0, 1, 1), (0, 0, 139))
## ESFERA E TRIÂNGULO
adcionar_triangulo((255,0,0),(3,1,0),(3,0,1), (3,0,-1))
# adcionar_esfera((0,0,255), 0.1, (1, 0, 0))
# adcionar_esfera((255,0,255), 0.1, (1, 1, 0))
# adcionar_esfera((0,255,255), 0.1, (1, 0, 1))
# adcionar_esfera((0,255,0), 0.1, (1, 0, -1))

## MALHA DE TRIÂNGULOS

# quadrado = obj.read_obj("square.obj", (126,126,126))
# for triangulo in quadrado:
#     adcionar_triangulo(*triangulo)
    
cubo = obj.read_obj("cube.obj", (50,160,50))
for triangulo in cubo:
   adcionar_triangulo(*triangulo)

# for que percorre toda a tela e gera a intesecção com os objetos
# para gerar a imagem final
for i in range(hres):
    for j in range(vres):
        vetor_atual = vetor_inicial + i*desl_h + j*desl_v
        imagem[j,i] = collor(camera, vetor_atual, objetos)

cv.imshow("grupo05", imagem)
cv.waitKey(0)
cv.destroyWindow('i')