import numpy as np
import cv2 as cv
import obj
import triangulo
INF = 9999999999

def test_bounding_box(ponto_reta, vetor_reta, x_max, x_min, y_max, y_min, z_max, z_min):
    c = ponto_reta
    r = vetor_reta
    
    if r[0] == 0:
        if c[0] > x_max or c[0] < x_min:
            return False
        t1_max = INF
        t1_min = 0
    else: 
        t1_max = (x_max - c[0])/r[0]
        t1_min = (x_min  - c[0])/r[0]
        if t1_min > t1_max:
            (t1_max, t1_min) = (t1_min, t1_max)
        if t1_max < 1:
            return False
    
    if r[1] == 0:
        if c[1] > y_max or c[1] < y_min:
            return False
        t2_max = INF
        t2_min = 0
    else: 
        t2_max = (y_max - c[1])/r[1]
        t2_min = (y_min  - c[1])/r[1]
        if t2_min > t2_max:
            (t2_max, t2_min) = (t2_min, t2_max)
        if t2_max < 1:
            return False
    
    if r[2] == 0:
        if c[2] > z_max or c[2] < z_min:
            return False
        t3_max = INF
        t3_min = 0
    else: 
        t3_max = (z_max - c[2])/r[2]
        t3_min = (z_min  - c[2])/r[2]
        if t3_min > t3_max:
            (t3_max, t3_min) = (t3_min, t3_max)
        if t3_max < 1:
            return False
        
    t_min = max(t1_min, t2_min, t3_min)
    t_max = min(t1_max, t2_max, t3_max)
    
    return t_max >= t_min and t_max >= 1
        

def normalize(v):
    ''''' NORMALIZAÇÃO DE VETOR (NÃO TEM NO NUMPY) '''''
    v = v/np.linalg.norm(v)
    return v

def intersect_triangle(ray, camera, triangulo_: triangulo.Triangulo):
    '''''FUNÇÃO DADA NO LIVRO PRA CALCULAR A INTERSECÇÃO COM O TRIANGULO'''''
    v0 = triangulo_[2]
    v1 = triangulo_[3]
    v2 = triangulo_[4]
    cor = triangulo_[1]
    vt0 = triangulo_[6]
    vt1 = triangulo_[7]
    vt2 = triangulo_[8]
    text = triangulo_[9]
    # Faz o teste de bounding box, para economizar processamento
    # Tá muito lento
    x_max = triangulo_.x_max
    x_min = triangulo_.x_min
    y_max = triangulo_.y_max
    y_min = triangulo_.y_min
    z_max = triangulo_.z_max
    z_min = triangulo_.z_min
    if not test_bounding_box(camera, ray, x_max, x_min, y_max, y_min, z_max, z_min):
        return (INF, None)
    
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
        return (INF, None)
    
    r = e*l - h*i
    e2 = a*n + d*q + c*r
    gamma = e2 * inv_denom
    if gamma < 0:
        return (INF, None) 
    if beta + gamma > 1:
        return (INF, None)
    
    e3 = a*p - b*r + d*s
    t = e3 * inv_denom
    if t< 0.01:
        return (INF, None)
    
    return (t, cor)

def collor(camera, vetor_atual, objetos):
    ''''' FUNÇÃO PARA CALCULAR A COR DE CADA OBJETO COM BASE NA MENOR DISTANCIA DA CAMERA '''''
    t = INF
    cor = np.array([0,0,0])
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
            (current, cor_t) = intersect_triangle(vetor_atual, camera, i)
        # pega o menor tempo e joga em T
        if current < t:
            t = current
            cor = cor_t
    return (t, cor)

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

def adcionar_triangulo(cor, p1, p2, p3):
    ''''' 0 = TIPO | 1 = COR | 2,3,4 = PONTO | 5 = VETOR_NORMAL '''''
    # transforma os pontos em array
    p1 = np.array(p1)
    p2 = np.array(p2)
    p3 = np.array(p3)
    cor = np.array(cor)
    tri = triangulo.Triangulo(cor, p1, p2, p3)
    objetos.append(tri)
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

quadrado = obj.read_obj("square.obj", (126,126,126))
for triangulo_ in quadrado:
    adcionar_triangulo(*triangulo_)


cubo = obj.read_obj("cube.obj", (50,160,50))

for triangulo_ in cubo:
    adcionar_triangulo(*triangulo_)
# for que percorre toda a tela e gera a intesecção com os objetos
# para gerar a imagem final
for i in range(hres):
    for j in range(vres):
        vetor_atual = vetor_inicial + i*desl_h + j*desl_v
        imagem[j,i] = collor(camera, vetor_atual, objetos)[1]

cv.imshow("grupo06 - ANTES", imagem)

# LIMPAR
objetos = []


## EXEMPLOS APÓS TRANSFORMAÇÃO
    
for triangulo_ in cubo:
    cor = triangulo_[0]
    pontos = (triangulo_[1], triangulo_[2], triangulo_[3])
    pontos = tuple(map(lambda x: translacao(x, -4, 0, 0), pontos))
    pontos = tuple(map(lambda x: expandir(x, 2), pontos))
    pontos = tuple(map(lambda x: rotacao_x(x, 20), pontos))
    pontos = tuple(map(lambda x: rotacao_y(x, 20), pontos))
    pontos = tuple(map(lambda x: rotacao_z(x, 20), pontos))
    pontos = tuple(map(lambda x: translacao(x, 4, 0, 0), pontos))
        
    adcionar_triangulo(cor, *pontos)
 #for que percorre toda a tela e gera a intesecção com os objetos
# para gerar a imagem final
for i in range(hres):
    for j in range(vres):
        vetor_atual = vetor_inicial + i*desl_h + j*desl_v
        imagem[j,i] = collor(camera, vetor_atual, objetos)[1]

cv.imshow("grupo06 - DEPOIS", imagem)
cv.waitKey(0)
cv.destroyWindow('i')