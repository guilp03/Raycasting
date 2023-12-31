import numpy as np
import cv2 as cv
import obj
import textura
INF = 9999999999

def normalize(v):
    ''''' NORMALIZAÇÃO DE VETOR (NÃO TEM NO NUMPY) '''''
    v = v/np.linalg.norm(v)
    return v

def intersect_triangle(ray, v0, v1, v2, camera, cor, vt0, vt1, vt2, text: textura.Textura):
    '''
    TROQUEI UMA FUNÇÃO POR UMA MAIS FÁCIL DE ENTENDER
    
    Basicamente, calcula o ponto de intersecção do raio com o plano do triângulo
    Então, verifica suas coordenadas baricentricas com relação a v0, v1 e v2
    Se tiver dentro, então, aplica a textura relativa com base em vt0, vt1 e vt2
    
    Também verifica se o parâmetro do raio é menor que 1, embora seja desnecessário
    
    Consegui piorar a performance disso MUITO! ahhahahahahahah
    '''
    
    # TODO: performance disso está muito ruim
    
    normal = np.cross(v0-v1, v0-v2)
    
    # Restrições: se o triangulo for degenerado ou se o raio for paralelo ao triangulo
    if np.linalg.norm(normal) < 0.01 or abs(np.dot(normal, ray)) < 0.01:
        return (INF, None)
    
    A = np.array([
        [v0[0], v1[0], v2[0], -ray[0]], 
        [v0[1], v1[1], v2[1], -ray[1]], 
        [v0[2], v1[2], v2[2], -ray[2]],
        [1, 1, 1, 0]
    ])
    b = np.array([camera[0], camera[1], camera[2], 1])
    res = np.linalg.solve(A, b)
    alpha = res[0]
    beta = res[1]
    gama = res[2]
    d = res[3]
    
    # Restrições, ponto fora do triangulo ou antes da tela
    if alpha > 1 or alpha < 0 or \
        beta > 1 or beta < 0 or \
        gama > 1 or gama < 0 or \
        d < 1:
            return (INF, None)
    
    
    # P = alpha*v0 + beta*v1 + gama*v2
    
    # Determina a cor
    if type(vt0) is not np.ndarray and vt0 == None:
        cor_res = cor
    else:
        # Encontrar o pixel correspondente na textura
        Ptextura = alpha*vt0 + beta*vt1 + gama*vt2
        cor_res = text.map(Ptextura[0], Ptextura[1])
    
######################################
    
    return (d, cor_res)

def collor(camera, vetor_atual, objetos):
    ''''' FUNÇÃO PARA CALCULAR A COR DE CADA OBJETO COM BASE NA MENOR DISTANCIA DA CAMERA '''''
    T = INF
    cor = np.array([30,30,30])
    for i in objetos:
        cor_t = i[1]
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
            (current, cor_t)= intersect_triangle(vetor_atual, i[2], i[3], i[4], camera, i[1], i[6], i[7], i[8], i[9])
        # pega o menor tempo e joga em T
        if current < T:
            T = current
            cor = cor_t
    return cor

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

#################################################################################
'''''FUNÇÕES PARA ADICIONAR OBJETOS'''''
# att: futuramente vai ser melhor criar uma classe pra cada
def adcionar_plano(cor, ponto, vetor):
    ''''' 0 = TIPO | 1 = COR |  2 = PONTO | 3 = VETOR_NORMAL '''''

    objetos.append(["plano", np.array(cor), np.array(ponto), np.array(vetor)])

def adcionar_esfera(raio, ponto, cor):
    ''''' 0 = TIPO | 1 = COR |2 = RAIO | 3 = CENTRO ''''' 

    objetos.append(["esfera", np.array(cor), raio, np.array(ponto)])

def adcionar_triangulo(cor, p1, p2, p3, t1 = None, t2 = None, t3 = None, text: textura.Textura = None):
    ''''' 0 = TIPO | 1 = COR | 2,3,4 = PONTO | 5 = VETOR_NORMAL | 6,7,8 = VETOR_TEXTURA | 9 = TEXTURA '''''
    # transforma os pontos em array
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)
    # calculo do vetor normal ao triangulo
    v0 = p2 - p1
    v1 = p3 - p1
    vetor = normalize(np.cross(v0,v1))

    if t1 and t2 and t3 and text:
        t1 = np.array(t1)
        t2 = np.array(t2)
        t3 = np.array(t3)
    else:
        t1 = None
        t2 = None
        t3 = None
        text = None
    
    objetos.append(["triangulo", np.array(cor), p1, p2, p3, vetor, t1, t2, t3, text])
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
objetos = []
## EXEMPLOS
#adcionar_triangulo(cor, ponto1,ponto2,ponto3)
#adcionar_esfera(cor,raio,centro)
#adcionar_plano(cor, ponto, vetor_normal)
#adcionar_triangulo((0,255,0), (4,0,1), (4,0,-1), (4,1,0))
#adcionar_triangulo((255,0,0), translacao([4,0,1], 1, 2, 1), translacao([4,0,-1],1,2,1), translacao([4,1,0],1,2,1))
#adcionar_plano((0,255,0), (4,0,-1), (4,1,0))
#adcionar_plano((255,0,0), rotacao_z([4,0,-1],30), rotacao_z([4,1,0],30))
#adcionar_plano(
#    (152,186, 213),
#    (1,0,-1),
#    (3,2,0)
#)
# adcionar_plano(
#     (127, 0, 255),
#     rotacao_z((4,0,-1), 15),
#     rotacao_z((3,2,0), 15)
# )
# adcionar_triangulo(
#     (127, 0, 255),
#     rotacao_z((4,0,-1), 15),
#     rotacao_z((4,0,1), 15),
#     rotacao_z((4,1,0), 15)
# )

# ROSA PINK (127, 0, 255)
# BEGE (152,186, 213)

textura_quadrado = textura.Textura("square.texture.jpg")

# quadrado = obj.read_obj("square.obj", (126,126,126), texture_on=True)
# for triangulo in quadrado:
#     adcionar_triangulo(*triangulo, textura_quadrado)


cubo = obj.read_obj("cube2.obj", (50,140,70), texture_on=True)
for triangulo in cubo:
    adcionar_triangulo(*triangulo, textura_quadrado)
    
# for que percorre toda a tela e gera a intesecção com os objetos
# para gerar a imagem final
for i in range(hres):
    for j in range(vres):
        vetor_atual = vetor_inicial + i*desl_h + j*desl_v
        imagem[j,i] = collor(camera, vetor_atual, objetos)

cv.imshow("grupo06 - ANTES", imagem)

# LIMPAR
objetos = []


## EXEMPLOS APÓS TRANSFORMAÇÃO
    
# for triangulo in cubo:
#     cor = triangulo[0]
#     pontos = (triangulo[1], triangulo[2], triangulo[3])
#     pontos = tuple(map(lambda x: translacao(x, -4, 0, 0), pontos))
#     pontos = tuple(map(lambda x: expandir(x, 2), pontos))
#     pontos = tuple(map(lambda x: rotacao_x(x, 20), pontos))
#     pontos = tuple(map(lambda x: rotacao_y(x, 20), pontos))
#     pontos = tuple(map(lambda x: rotacao_z(x, 20), pontos))
#     pontos = tuple(map(lambda x: translacao(x, 4, 0, 0), pontos))
        
#     adcionar_triangulo(cor, *pontos)
#  #for que percorre toda a tela e gera a intesecção com os objetos
# # para gerar a imagem final
# for i in range(hres):
#     for j in range(vres):
#         vetor_atual = vetor_inicial + i*desl_h + j*desl_v
#         imagem[j,i] = collor(camera, vetor_atual, objetos)

# cv.imshow("grupo06 - DEPOIS", imagem)
cv.waitKey(0)
cv.destroyWindow('i')