import numpy as np
import cv2 as cv
import obj
INF = 9999999999

def normalize(v):
    ''''' NORMALIZAÇÃO DE VETOR (NÃO TEM NO NUMPY) '''''
    v = v/np.linalg.norm(v)
    return v

def phong(objeto, lista_luzes, ponto_intersec, n_ponto, camera):
    lamb = objeto.ka * np.array([255,255,255])
    for luz in lista_luzes:
        objeto_luz = ponto_intersec - luz.ponto
        
        # COMPONENTE DIFUSA
        cosln = np.dot(n_ponto, objeto_luz)
        if cosln < 0:
            cosln = 0
        difusa = luz.intensidade * objeto.cor * objeto.kd * cosln
        
        # COMPONENTE ESPECULAR
        #vetor_refletido = ((2*n_ponto) * np.dot(n_ponto, objeto_luz)) - objeto_luz
        #vetor_observador = ponto_intersec - camera
        #cosrvq = np.dot(vetor_refletido, vetor_observador)**objeto.q
        #especular = luz.intensidade * objeto.ks * cosrvq

        return difusa + lamb
    
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
    T = INF
    current_obj = None
    n_ponto = None
    for objeto in objetos:
        if isinstance(objeto, Esfera):
            oc = camera - objeto.centro
            a = np.dot(vetor_atual, vetor_atual)
            b = 2 * np.dot(oc, vetor_atual)
            c = np.dot(oc, oc) - (objeto.raio ** 2)
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
            
            n_ponto 

        elif isinstance(objeto, Plano):
            tmp = np.dot(objeto.vetor_normal, vetor_atual)
            if tmp == 0:
                continue
            current = (np.dot(objeto.vetor_normal, objeto.ponto) - np.dot(objeto.vetor_normal, camera)) / tmp
            if current < 0.01:
                current = INF
        
        elif isinstance(objeto, Triangulo):
            tmp = np.dot(objeto.vetor_normal, vetor_atual)
            if tmp == 0:
                continue
            current = intersect_triangle(vetor_atual, objeto.p1, objeto.p2, objeto.p3, camera)
        
        if current < T:
            T = current
            current_obj = objeto
    if T < INF:
        x = camera[0] + vetor_atual[0] * T
        y = camera[1] + vetor_atual[1] * T
        z = camera[2] + vetor_atual[2] * T
        ponto_intersec = np.array([x,y,z])
        if isinstance (current_obj, Esfera):
            n_ponto = ponto_intersec - current_obj.centro
        elif isinstance (current_obj,Triangulo) or isinstance (current_obj,Plano):
            n_ponto = current_obj.vetor_normal 
        phong_v = phong(current_obj, fonte_luz, ponto_intersec, n_ponto, camera)
        if phong_v[0] > 255:
            phong_v[0] = 255
        if phong_v[1] > 255:
            phong_v[1] = 255
        if phong_v[2] > 255:
            phong_v[2] = 255
        return phong_v
    else:
        return np.array([0,0,0])

'''FUNÇÃO PARA RETIRAR O NP.ARRAY, FACILITANDO COMPOSIÇÃO DE TRANSFORMAÇÕES'''
def nparray_para_tuple(vetor):
    if type(vetor) == list or type(vetor) == tuple or type(vetor) == np.ndarray:
        return tuple(nparray_para_tuple(i) for i in vetor)
    else:
        return vetor

'''DEFININDO MATRIZES DE ROTAÇÃO E REFLEXÃO'''
def translacao(ponto, p1,p2,p3):
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

class Plano:
    def __init__(self, cor, ponto, vetor, kd, ks, ka, q):
        self.cor = np.array(cor)
        self.ponto = np.array(ponto)
        self.vetor_normal = np.array(vetor)
        self.ka = ka
        self.kd = kd
        self.ks = ks
        self.q = q

class Triangulo:
    def __init__(self, cor, p1, p2, p3, kd, ks, ka, q):
        self.cor = np.array(cor)
        self.p1 = np.array(p1)
        self.p2 = np.array(p2)
        self.p3 = np.array(p3)
        self.ka = ka
        self.kd = kd
        self.ks = ks
        self.q = q
        # cálculo do vetor normal ao triângulo
        v0 = self.p2 - self.p1
        v1 = self.p3 - self.p1
        self.vetor_normal = self.normalize(np.cross(v0, v1))

class Esfera:
    def __init__(self, raio, ponto, cor, kd, ks, ka, q):
        self.cor = np.array(cor)
        self.raio = raio
        self.centro = np.array(ponto)
        self.ka = ka
        self.kd = kd
        self.ks = ks
        self.q = q

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
''''' ADICIONANDO FONTES DE LUZ '''''
n = int(input("QUANTIDADE DE FONTES DE LUZ"))
intensidade_ambiente = np.array([255,255,255])
fonte_luz = []

class Fonte_Luz:
    def __init__ (self, x,y,z,i1,i2,i3):
        self.ponto = np.array([x,y,z])
        self.intensidade = np.array([i1,i2,i3])

for i in range(n):
    print("LUZ")
    x = int(input())
    y = int(input())
    z = int(input())
    i1 = int(input())
    i2 = int(input())
    i3 = int(input())
    fonte_luz.append(Fonte_Luz(x,y,z,i1,i2,i3))

#################################################################################
''''' INICIALIZAÇÃO DOS OBJETOS PARA CASOS TESTE '''''
objetos = []
objetos.append(Esfera(0.5,[4,0,0],[255,0,0],0.5,0.3,0.2,200))
# ROSA PINK (127, 0, 255)
# BEGE (152,186, 213)

# for que percorre toda a tela e gera a intesecção com os objetos
# para gerar a imagem final
for i in range(hres):
    for j in range(vres):
        #print(f"[{i}, {j}]")
        vetor_atual = vetor_inicial + i*desl_h + j*desl_v
        imagem[j,i] = collor(camera, vetor_atual, objetos)
print(imagem)
cv.imshow("grupo06", imagem)